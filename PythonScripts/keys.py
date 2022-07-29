# Script to read API keys off local drive instead of hosting API keys in a public repo. 
# API key is saved as a .txt and then saved for use across this repo.
from pathlib import Path

# Function for generating API key out of a text file where key is first line and only content of the .txt
def get_file_contents(filename: str):
    cwd = Path.cwd().absolute()
    key_path = Path.joinpath(cwd,'Keys',filename)
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


# Key for Rebrickable API
KEY_ONE = get_file_contents('rebrickable.txt')

#Key for Brickset API
KEY_TWO = get_file_contents('brickset.txt')

if __name__ == "__main__":
    main()      
