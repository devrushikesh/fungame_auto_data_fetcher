# index.py - Entrypoint for Appwrite Cloud Function

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

# Import the main function
from main import main as main_function

# Entrypoint for Appwrite Cloud Function
def main(req, res):
    return main_function(req, res)
