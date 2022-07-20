
import os
import pandas as pd 
import requests
from PythonScripts.keys import KEY_ONE
from PIL import Image
import os
import PythonScripts.resize

# import theme df, join merged_df_three with theme to get star wars theme. 
#add code to not include first columns

inv_df = pd.read_csv('./CSVs/inventories.csv', usecols=['id','set_num'])
inv_parts_df = pd.read_csv('./CSVs/inventory_parts.csv', usecols=['inventory_id', 'part_num', 'color_id', 'quantity'])
set_df = pd.read_csv('./CSVs/sets.csv', usecols=['set_num', 'name', 'year', 'theme_id', 'num_parts'])
parts_df = pd.read_csv('./CSVs/parts.csv', usecols=['part_num', 'name'])


# Rename columns for easier joining
inv_rename_dict = {'id' : 'inventory_id',
                   'set_num' : 'set_num'}
inv_df.rename(columns=inv_rename_dict, inplace=True)

parts_rename_dict = {'part_num' : 'part_num',
                     'name' : 'part_name'}
parts_df.rename(columns=parts_rename_dict, inplace=True)


# Merge all Dataframes into one larger dataframe with all data points
all_merged_df = inv_df.merge(inv_parts_df, how='inner', left_on='inventory_id', right_on='inventory_id')
all_merged_df = all_merged_df.merge(set_df, how='inner', left_on='set_num', right_on='set_num')
all_merged_df = all_merged_df.merge(parts_df, how='inner', left_on='part_num', right_on='part_num')
all_merged_df.head()

# Remove all non-Star Wars themes from the Dataframe
sw_theme_ids = [18, 158, 171, 209, 261]
all_merged_df = all_merged_df[all_merged_df['theme_id'].isin(sw_theme_ids)]



# find set number with the most pieces
piece_count = all_merged_df.groupby(['set_num'])['quantity'].sum()
max_count = piece_count.idxmax()

# drop all rows but set with most pieces
mask = all_merged_df[all_merged_df['set_num'] != max_count].index
all_merged_df.drop(mask, inplace=True)

# Make a new df with just top 10 parts with highest quantity. Save as CSV to use in Tableau dashboard 
top_ten_parts = all_merged_df['quantity'].nlargest(n=10, keep='first')
top_ten_df = all_merged_df[all_merged_df['quantity'].isin(top_ten_parts)]
top_ten_df.reset_index(drop=True, inplace=True)
top_ten_df.to_csv('./CSVs/top_ten_parts.csv')


# initialize new lists for color id and part number of top 10 piece quantities. Zip to tuple to lock in for API calls
# API call to find part specs for each part/color combination and save the image URL to a list
# add the URLs to the top ten Dataframe
part_num_list =[]
part_color_list = []

for item in top_ten_df['part_num']:
    part_num_list.append(item)
for item in top_ten_df['color_id']:
    part_color_list.append(str(item))
num_color_zip = zip(part_num_list,part_color_list)

url_list = []
for num, color in num_color_zip:
    response = requests.get(f'https://rebrickable.com/api/v3/lego/parts/{num}/colors/{color}?key={KEY_ONE}')
    data = response.json()
    url_list.append(str(data['part_img_url']))

url_df = pd.DataFrame({'part_num' : part_num_list,
                       'URL' : url_list})

url_df['part_num'] = url_df['part_num'].astype(str)
url_df['URL'] = url_df['URL'].astype(str)

top_ten_df = top_ten_df.merge(url_df, how='left', left_on='part_num', right_on='part_num')

url_df.to_csv('./CSVs/url_list.csv')

# # Save images and resize for Tableau
# PythonScripts.resize.write_image(url_list)
# PythonScripts.resize.resize_files('../JPGs/')