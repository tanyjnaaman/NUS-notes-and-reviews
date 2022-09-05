# functional
import cv2
import pandas as pd
import PIL.Image
import numpy as np
import os
import time
import torch

from numba import prange
from skimage import io
from skimage import transform
from torch.utils.data import Dataset


# pickle
import pickle

class AnimalDataset(Dataset):
    """
    Custom Animal Dataset.
    """

    def __init__(self, 
                 index_file_path: str, 
                 root_dir_path: str, 
                 file_prefix : str,
                 image_dimension: int, 
                 local_dir_path: str = None, 
                 transform = None,
                 concat_mask = True,
                 random_noise = True,
                 require_init = True,
                 drops = None, 
                 divide_range = (4,6), 
                 file_postfix = [".png", ".jpg", ".jpeg"],
                 seed = None):
        """
        Args:
            index_file_path: Path to the file with indices
            root_dir_path:   Directory with the images
            transform:       Callable that transforms sample
        """

        # save other attributes
        self.root_dir_path = root_dir_path
        self.transform = transform
        self.local_dir_path = local_dir_path
        self.IM_DIMENSIONS = image_dimension
        self.CONCAT_MASK = concat_mask
        self.FILE_PREFIX = file_prefix
        self.INITIALIZED = False
        self.REQUIRE_INIT = require_init
        self.RANDOM_NOISE = random_noise
        if seed is not None:
            np.random.seed(seed)

        # constants
        AnimalDataset.CROP_BOX_SIZES_DIVIDE_RANGE = divide_range
        AnimalDataset.FILE_POSTFIX = file_postfix


        # load file indices, then transform each index to one possibility for each postfix
        self.df_indices = pd.read_csv(index_file_path, usecols = [0], header = 0) # select first column, which should be index
        if drops is not None:
            self.df_indices = self.df_indices.drop(drops, inplace = False)
        
        # get file names
        self.df_filenames = self.df_indices.apply(
            lambda x : [self.FILE_PREFIX + str(int(x)).strip() + postfix for postfix in AnimalDataset.FILE_POSTFIX], 
            axis = 1)  


                
    def _clean(self, verbose = True):
        """
        This is a helper method that clears the text file of corrupted files at startup. 
        Used as a defensive method of ensuring dataset is clean.
        """

        corrupted = []
        start = time.time()
        print("Cleaning ...")

        for idx in prange(len(self.df_filenames)):
            filenames = self.df_filenames.iloc[idx]
            for f in filenames:
                try: 
                    image_name = os.path.join(self.root_dir_path, f)
                    image = io.imread(image_name)   
                
                    # if 4 channels and png, then RGBA -> convert
                    if image.shape[-1] == 4:
                        rgba_image = PIL.Image.open(image_name)
                        image = np.array(rgba_image.convert('RGB'))

                    # sanity check that is an RGB image
                    h, w, c = image.shape
                    assert(c == 3)

                except FileNotFoundError:
                    continue

                except AttributeError: # NoneType -> corrupted file
                    corrupted.append(idx) 

                except: # no idea why it fails, catch all, just remove
                    corrupted.append(idx) 


        # at the end, drop all corrupted rows from df_indices 
        self.df_indices = self.df_indices.drop(corrupted, inplace = False)

        # reload filenames
        self.df_filenames = self.df_indices.apply(
            lambda x : [self.FILE_PREFIX + str(int(x) + 1).strip() + postfix for postfix in AnimalDataset.FILE_POSTFIX], 
            axis = 1)   

        print(f"Cleaning completed. Dropped {len(corrupted)} files. Took {(time.time() - start)/60} min")
        if verbose:
            print(f"The row indices dropped were {corrupted}")
    
    def __len__(self):
        return len(self.df_indices)

    def __getitem__(self, idx):
        """
        Gets a sample.
        """
        if not self.INITIALIZED and self.REQUIRE_INIT:
            print("Not initialized! Please call AnimalDataset::initialize()!")

        assert(self.INITIALIZED or not self.REQUIRE_INIT)

        if torch.is_tensor(idx):
            idx = idx.tolist()

        # retrieve preloaded
        if self.local_dir_path != None:
            try: 
                # load from memory
                sample = self._getsample_local(idx, self.CONCAT_MASK, self.RANDOM_NOISE)
                return sample

            except FileNotFoundError:
                pass

        # no preloaded, preprocess and save
        return self._getsample_loadsave(idx, self.CONCAT_MASK, self.RANDOM_NOISE)

    def initialize(self):
        self._clean()
        self.INITIALIZED = True


    def _getsample_local(self, idx, concat_mask = False, random_noise = False):
        """
        Gets an image stored locally and then processes it into 
        a sample.
        """

        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        # load image from local
        filename = os.path.join(self.local_dir_path, str(int(self.df_indices.iloc[idx])).strip())
        with open(f"{filename}.pickle", "rb") as p:
            image = pickle.load(p)

        with open(f"{filename}.pickle", "rb") as p:
            damaged_image = pickle.load(p)

        with open(f"{filename}.pickle", "rb") as p:
            gray = pickle.load(p)

        # dynamically damage
        damaged_image, mask = self._damage(damaged_image, random_noise)

        # optionally append mask to damaged image
        if concat_mask:
            damaged_image = torch.cat([damaged_image, mask], dim = -1)

        # grayscale
        gray = self._gray(gray)
                
        # return sample as tuples of (tensor, tensor)
        sample = {"image": damaged_image, "reconstructed" : image, "mask" : mask, "gray" : gray}

        # transform if defined as in normal Dataset class
        if self.transform:
            sample = self.transform(sample)

        return sample
        

    def _getsample_loadsave(self, idx, concat_mask = False, random_noise = False):
        """
        Gets a sample from memory, preprocesses it for aspect ratio, then 
        processes it into a sample.
        """
        if torch.is_tensor(idx):
            idx = idx.tolist()
               
        # load pair
        damaged_image, image = self._load_image_pair(self.df_filenames.iloc[idx])
        damaged_image, mask = self._damage(damaged_image, random_noise)
        gray = self._gray(image)
        
        # optionally append mask to damaged image
        if concat_mask:
            damaged_image = torch.cat([damaged_image, mask], dim = -1)
                
        # return sample as dictionaries
        sample = {"image": damaged_image, "reconstructed" : image, "mask" : mask, "gray" : gray}

        # save image as pickle
        if self.local_dir_path != None:
            filename = os.path.join(self.local_dir_path, str(int(self.df_indices.iloc[idx])).strip())
            with open(f"{filename}.pickle", "wb") as p:
                pickle.dump(image, p, protocol = pickle.HIGHEST_PROTOCOL)

        # transform if defined as in normal Dataset class
        if self.transform:
            sample = self.transform(sample)

        return sample
        

    def _load_image_pair(self, filenames: list):
        """
        This is a helper method that loads images from our dataset. Given that 
        the images are saved in different file types, this method tries to find 
        one of each and does a sanity check to make sure the image is RGB.
        """
        for i in filenames:
            try: 
                image_name = os.path.join(self.root_dir_path, i)
                image = io.imread(image_name)   
            
                # if 4 channels and png, then RGBA -> convert
                if image.shape[-1] == 4:
                    rgba_image = PIL.Image.open(image_name)
                    image = np.array(rgba_image.convert('RGB'))

                # aspect ratio preprocessing
                image = self._preprocess_aspectratio(image)

                # sanity check that is an RGB image
                h, w, c = image.shape
                assert(c == 3)

                return torch.tensor(image).float(), torch.tensor(image).float()

            except FileNotFoundError:
                continue

            except AttributeError:
                print("AttributeError!")
                print(image_name)

        raise Exception("Unable to load image! File names are: ", filenames)
        
    def _preprocess_aspectratio(self, image):
        """
        Corrects aspect ratio by resizing according to the smallest dimension
        (by n-dimensional interpolation), followed by cropping out the 
        centre portion of the image.
        """

        # ===== ASPECT RATIO CORRECTION =====
        h, w = image.shape[:2] # first two dimensions

        # interpolate by shorter side
        rotate = False
        if w > h: 
            rotate = True
            image = image.transpose(1, 0, 2)
            h, w = image.shape[:2]

        # width always shorter 
        ratio = h/w
        dim =  self.IM_DIMENSIONS
        h = int(dim * ratio)
        image = transform.resize(image, (h, dim))

        # crop
        centre = h//2
        image = image[centre - dim//2:centre + dim//2,:,:]

        # rotate back when done
        if rotate:
            image = image.transpose(1, 0, 2)
        
        return image

    def _damage(self, image, random_noise = True):
        """
        This helper method damages the image for later reconstruction. 
        I have wrapped the methods into local helper methods. This way, reading and 
        debugging is easier in future.
        """
        def random_squares(image):

            # randomly choose size of crop
            low, high = AnimalDataset.CROP_BOX_SIZES_DIVIDE_RANGE
            h, w = np.random.random(size = 2) * (high - low) + low
            h, w = int(self.IM_DIMENSIONS//h), int(self.IM_DIMENSIONS//w)

            # randomly choose location of crop
            h_lower, h_higher = 0 + h//2, self.IM_DIMENSIONS - h//2
            w_lower, w_higher = 0 + w//2, self.IM_DIMENSIONS - w//2
            h_centre = np.random.randint(h_lower, h_higher + 1)
            w_centre = np.random.randint(w_lower, w_higher + 1)

            # create mask
            height, width, c = image.shape
            mask  = torch.ones(height, width, 1)
            mask[h_centre - h//2:h_centre + h//2,
                 w_centre - w//2:w_centre + w//2,:] = 0

            # crop
            image = torch.mul(mask, image)

            # add random noise
            if random_noise:
                image[h_centre - h//2:h_centre + h//2,
                    w_centre - w//2:w_centre + w//2,:]  = torch.rand((h//2 * 2), (w//2 * 2),c) 

            return image, mask

        image, mask = random_squares(image)
        
        return image, mask

    def _reshape_channelFirst(self, image):
        h, w, c = image.size()
        return image.reshape(c, h, w)

    def _gray(self, image):
        image = (image.numpy()*255).astype(np.uint8) # to numpy 255
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return torch.from_numpy(gray)/255

    def _edge(self, image):

        def canny(image):
            image = (image.numpy()*255).astype(np.uint8) # to numpy 255
            high = np.percentile(image, 99)
            low = np.percentile(image, 97.5)
            canny = torch.from_numpy(cv2.Canny(image, threshold1 = low, threshold2 = high)/255)
            return canny

        def gray(image):
            image = (image.numpy()*255).astype(np.uint8) # to numpy 255
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray

        edge = gray(image)

        return edge
