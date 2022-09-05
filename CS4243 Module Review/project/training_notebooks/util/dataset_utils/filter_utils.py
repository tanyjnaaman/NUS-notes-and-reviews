import matplotlib.pyplot as plt
import numpy as np
import ntpath
import os
import requests


from easyimages import EasyImageList
from numba import prange
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ===== VISUALIZATION =====

def visualize_images_from_df(df, samples = 128):
    """
    This method takes in a dataframe containing links to the image
    and the source and visualizes them. The required keys are:
        * "image_url" -> url where image can be pulled from
        * "url" -> url of the sample
    """
    urls = df['image_url'].tolist()
    observation_urls = df['url'].tolist()
    easy_list = EasyImageList.from_list_of_urls(urls, lazy = True)
    
    # Add observation url into label, which is displayed as alt text
    for i in prange(len(easy_list)):
        easy_list[i].label = observation_urls[i]
        
    _ = easy_list.visualize_grid_html(np.random.choice(easy_list.images, min(len(easy_list), samples), replace = False))

def visualize_images_from_url(urls: list, samples = 128):
    easy_list = EasyImageList.from_list_of_urls(urls, lazy = True)
    easy_list.html(sample = min(len(easy_list), samples))


# ===== FILTERING =====
def retrieve_word_embeddings(words: list):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(words, convert_to_tensor = True)
    return embeddings

def compute_similarity_score(seed_embeddings: list, all_embeddings: list) -> list:
    """
    Takes in a [n x d] list of seed_embeddings, and for each one, computes a similarity score
    with all embeddings in the list of all_embeddings [w x d] to get an output of [n x w].
    """
    scores = cosine_similarity(seed_embeddings.cpu(), all_embeddings.cpu())
    return scores

def print_topk_words(query_words: list, scores: list, key_words: list, k = 10, threshold = 0.5):
    """
    Takes in a n x w list of scores, and a list of w words, and finds the top k 
    similar words for each of the n words.
    """
    indices = np.argpartition(scores, -k)[:,-k:] # sort then take top k, for each word
    topk_words = np.take(np.array(key_words), indices)
    topk_scores = scores[np.arange(scores.shape[0])[:, None], indices]

    # print top k word, score for each word
    out_list = []
    for i, row in enumerate(range(topk_words.shape[0])):
        print(f"Word {i+1}: {query_words[i]}")
        sorted_list = sorted(list(zip(topk_words[row], topk_scores[row])), key=lambda t: t[1], reverse=True)
        for word, score in sorted_list:
            print("[{:.5f}] - {}".format(score, word))
        print()

        out_list.extend(list(filter(lambda wordscore : wordscore[1] > threshold, sorted_list)))

    return out_list

def groupby_plot_hist(df, column_name, count_threshold = 100):
    frequent = df[df.groupby(column_name)[column_name].transform("size") > count_threshold]
    counts = frequent[column_name].value_counts()
    counts.plot(kind = "bar")
    print(counts)
    print(len(counts), "categories above threshold. Total is", counts.sum())
    plt.show()
    return

def filter_by_threshold_counts(df, column_names: list, count_threshold = 100):
    out_df = df
    prev_size = len(df)
    redo = True
    while redo:
        for column in column_names:
            out_df = out_df[out_df.groupby(column)[column].transform("size") > count_threshold]
            if len(out_df) < prev_size: # had change, need to recheck previous
                prev_size = len(out_df)
                redo = True
                continue
            redo = False

    print("After filtering, left with", len(out_df), "samples.")
    return out_df

# ===== DOWNLOADING =====
def download_image(id_url: tuple, save_dir: str):

    EXTENSIONS = [".jpeg", ".png", ".jpg"]

    try:
        idx, img_url = id_url
        
        # check if exists
        exists = [os.path.join(save_dir, "frogs_" + str(idx) + ext) for ext in EXTENSIONS]
        exists = list(filter(lambda file : os.path.exists(file), exists))
        if len(exists) > 0: # exists
            return

        # get file
        img_bytes = requests.get(img_url).content
        _, file_name = ntpath.split(img_url)
        file_id, file_ext = os.path.splitext(file_name)

        # name
        FILENAME = "frogs_" + str(idx) + file_ext
        SAVE_PATH = os.path.join(save_dir, FILENAME)

        # save
        with open(SAVE_PATH, 'wb') as img_file:
            img_file.write(img_bytes)
            print(f'\r{FILENAME} was downloaded...', end = '', flush = True)
    except Exception as e:
        print(e)