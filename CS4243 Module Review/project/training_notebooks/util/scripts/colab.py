# ====== 1. GET FILES =====
# get files from github
!rm -rf github_clone
!git clone -l -s https://github.com/tanyjnaaman/CS4243-project.git github_clone

# mount gdrive
from google.colab import drive
drive.mount('/gdrive')

# make a local data directory
!rm -r /content/data
!mkdir /content/data
!mkdir /content/data/images
!mkdir /content/data/preprocessed

# get images
file_id = "13Iz_lnqIeanJxmgy2ccgh-1HkHKPOH3G"
file_name = '/content/data/frog_images.zip'
! wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={file_id}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={file_id}" -O {file_name} && rm -rf /tmp/cookies.txt

# get preprocessed files
file_id = "1Gg71wbvkAMiVv0dyyvOs-YJSBIjrq7I2"
file_name = '/content/data/preprocessed_64.zip'
! wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={file_id}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={file_id}" -O {file_name} && rm -rf /tmp/cookies.txt

# unzip files
!unzip /content/data/frog_images.zip -d /content/data/images
!unzip /content/data/preprocessed_64.zip -d /content/data/preprocessed

# ====== 2. INSTALLS =====
!pip install lpips
!pip install wandb
!pip install torchmetrics

# ====== 3. IMPORTS =====
import lpips
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import time
import torch
import torch.nn as nn
import torchmetrics
import torchvision
import wandb

from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader, Subset
from skimage import io
from skimage import transform

# ====== 4. CUSTOM IMPORTS =====
import sys
sys.path.append("/content/github_clone/")
from utils.dataset_utils.AnimalDataset import AnimalDataset
from utils.train_utils.train_utils import visualize_results, sample_batch, summary
from utils.train_utils.model_utils import Conv2dBlock, GatedConv2dBlock, GatedUpConv2dBlock

# ===== 5. SET UP DATASETS =====
# set up
train_dataset = AnimalDataset(index_file_path = "/content/github_clone/dataset/frogs_train.txt",
    root_dir_path = "/content/data/images/frog_images",
    local_dir_path = "/content/data/preprocessed",
    file_prefix = "frogs_",
    image_dimension = 64,
    concat_mask = True,
    random_noise = True,
    require_init = False,
    drops = [])

valid_dataset = AnimalDataset(index_file_path = "/content/github_clone/dataset/frogs_val.txt",
    root_dir_path = "/content/data/images/frog_images",
    local_dir_path = "/content/data/preprocessed",
    file_prefix = "frogs_",
    image_dimension = 64,
    concat_mask = True,
    random_noise = True,
    require_init = False,
    drops = [])

test_dataset = AnimalDataset(index_file_path = "/content/github_clone/dataset/frogs_test.txt",
    root_dir_path = "/content/data/images/frog_images",
    local_dir_path = "/content/data/preprocessed",
    file_prefix = "frogs_",
    image_dimension = 64,
    concat_mask = True,
    random_noise = True,
    require_init = False,
    drops = [])

# sanity check 
sample_batch(train_dataset, sample_size = 6)
sample_batch(valid_dataset, sample_size = 6)
sample_batch(test_dataset, sample_size = 6)

