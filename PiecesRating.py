import pandas as pd
import requests
from keys import KEY_TWO
from data_clean import drop_columns

# API Call to get list of LEGO themes and convert to dataframe
themes = requests.get(f'https://brickset.com/api/v3.asmx/getThemes?apiKey={KEY_TWO}') 
data = themes.json()
theme_df = pd.json_normalize(data, 'themes')

# Drop themes older than 1999, themes with less than 50 sets, sets that aren't currently in production, minifig theme, and miscellaneous theme
mask = theme_df[(theme_df['yearFrom'] < 1999) | (theme_df['setCount'] < 50) | (theme_df['yearTo'] < 2022) |
         (theme_df['theme'] == 'Collectable Minifigures') | (theme_df['theme'] == 'Miscellaneous')].index
theme_df.drop(mask, inplace=True)


# Generate sample theme list to use in 2nd API call. Convert list to string for API parameters.
theme_list = []
for item in theme_df['theme'].sample(3):
    theme_list.append(item)
param_string = ", ".join(theme_list)


# 2nd API call to get a full set list for themes in the theme list generated by first API call. Convert to a data frame
parameters = {'theme' : f'{param_string}', 'pageSize' : 2500}
set_list = requests.get(f"https://brickset.com/api/v3.asmx/getSets?apiKey={KEY_TWO}&userHash=&params={parameters}")
set_data = set_list.json()
set_df = pd.json_normalize(set_data,'sets')


# Drop columns using helper function
drop_columns(set_df)

# Drop rows where there is no rating for the set.
mask_two = set_df[set_df['rating'] == 0].index
set_df.drop(mask_two, inplace=True)


# Drop any rows if they have a NaN value in the pieces column
pieces_null = set_df['pieces'].isnull().values.any()
if pieces_null == True:
    set_df.dropna(subset=['pieces'], inplace=True)


#Convert pieces, minimum age range, and maximum age range from floats to ints.
set_df['pieces'] = set_df['pieces'].astype(pd.Int64Dtype())
set_df['ageRange.min'] = set_df['ageRange.min'].astype(pd.Int64Dtype())
set_df['ageRange.max'] = set_df['ageRange.max'].astype(pd.Int64Dtype())

rename_dict = {
               'setID' : 'Set ID',
               'number' : 'Set Number',
               'name' : 'Set Name',
               'year' : 'Release Year',
               'theme' : 'Theme',
               'themeGroup' : 'Theme Group',
               'subtheme' : 'Subtheme',
               'pieces' : 'Number of Pieces',
               'rating' : 'Brickset Rating',
               'ageRange.min' : 'Min Age Range',
               'ageRange.max' : 'Max Age Range',
                }
                

set_df.rename(columns=rename_dict, inplace=True)

set_df = set_df.sample(100)

# Save data to CSV for visualization in Tableau
set_df.to_csv('./set_list.csv')

