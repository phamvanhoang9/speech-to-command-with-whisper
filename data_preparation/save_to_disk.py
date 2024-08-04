"""This module contains the function to save the data to disk."""
import pickle # used to save the data to disk
from typing import Any, Dict


# Define the function to save the data to disk
def save_to_disk(data: Dict[str, Any], path: str) -> None:
    """Save the data to disk.

    Args:
    - data: the data to be saved
    - path: the path to save the data to
    """
    with open(path, 'wb') as file:
        pickle.dump(data, file)
    print(f"Data saved to {path}") 
    return None

