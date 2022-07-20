# GZip to CSV converter
import pandas as pd
import gzip
import os

def convert_gz_to_csv(gz: gzip.GzipFile):
     
    filename = os.path.splitext(gz)[0]
    filename_two = os.path.split(filename)[1]
    df = pd.read_csv(gz, compression='gzip', on_bad_lines='skip')
    df.to_csv(f'.\CSVs\{filename_two}')
    
def main():
    gz = input('Input your file path: ')
    convert_gz_to_csv(gz)
    # example '.\GZIPS\inventories.csv.gz'


if __name__ == "__main__":
    main()      

