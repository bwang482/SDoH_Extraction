"""
Utility functions for SDoH extraction pipeline.
"""
import os
import json
import pickle
from thefuzz import fuzz


def _create_folder_if_not_exist(filename):
    """ Makes a folder if the folder component of the filename does not already exist. """
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def save_pickle(obj, filename, protocol=4, create_folder=True):
    """ 
    Save a Python object to a pickle file.

    Args:
        obj (python object): The object to be saved.
        filename (str): Location to save the file.
        protocol (int): Pickling protocol.
    """
    if create_folder:
        _create_folder_if_not_exist(filename)

    with open(filename, 'wb') as file:
        pickle.dump(obj, file, protocol=protocol)


def load_pickle(filename):
    """ 
    Load a Python object from a pickle file.
    
    Args:
        filename (str): Path to the pickle file
        
    Returns:
        python object: The loaded object.
    """
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
    return obj


def save_json(obj, filename, create_folder=True):
    """ Save file with json. """
    if create_folder:
        _create_folder_if_not_exist(filename)

    with open(filename, 'wb') as file:
        json.dump(obj, file)


def load_json(filename):
    """ Load file with json. """
    with open(filename) as file:
        obj = json.load(file)
    return obj


def deduplicate_by_similarity(items, key_field='sent', similarity_threshold=90):
    """
    Remove duplicates based on string similarity.
    
    Args:
        items: List of dictionaries to deduplicate
        key_field: Field to use for similarity comparison
        similarity_threshold: Minimum similarity score to consider as duplicate
        
    Returns:
        Deduplicated list of items
    """
    if not items:
        return []
    
    unique_items = []
    seen_texts = []
    
    for item in items:
        text = item.get(key_field, '')
        
        if not seen_texts:
            unique_items.append(item)
            seen_texts.append(text)
        else:
            # Check similarity with all seen texts
            max_similarity = max(fuzz.ratio(text, seen) for seen in seen_texts)
            
            if max_similarity < similarity_threshold:
                unique_items.append(item)
                seen_texts.append(text)
    
    return unique_items



