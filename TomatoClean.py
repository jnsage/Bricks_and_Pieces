import pandas as pd
import requests
from keys import KEY_TWO
from data_clean import drop_columns


# Configure URL for pd.read_csv
# Full sheet URL == https://docs.google.com/spreadsheets/d/1xw7y9yawF6i35BTfP9M1uUawJvwpacz01Xq4MEZszBs/edit#gid=0
# workbook_id = "1xw7y9yawF6i35BTfP9M1uUawJvwpacz01Xq4MEZszBs"
# sheet_name = "Sheet1"
# url = f"https://docs.google.com/spreadsheets/d/{workbook_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


# Read Google Sheet and convert to a Dataframe
#year_df = pd.read_csv(url, parse_dates=['Release_Date'])
year_df = pd.read_csv('year_df.csv', parse_dates=['Release_Date'])
# year_df.to_csv('./year_df.csv')


# Format Date column to display as the year
year_df['Release_Date'] = year_df['Release_Date'].dt.strftime('%Y')
year_df


# Clean extra text out the Title column
for item, str in year_df['Title'].items():
        head, sep, tail = str.partition(' – ')
        year_df['Title'].replace(to_replace=str, value = head, inplace=True)


# Function for cleaning a series by partition
def part_colon(column_label: pd.Series) -> pd.Series:
        for item, value in column_label.items():
           if ': ' in value:
                head, sep, tail = value.partition(': ')
                column_label.replace(to_replace=value, value = tail, inplace=True)
        return pd.Series



# Run cleaning function on Title column
part_colon(year_df['Title'])

year_df.drop(index=9, inplace=True)
# Remove Clone Wars movie which was kick off of Star Wars TV Show
# mask_three = year_df[(year_df['Title'] == "The Clone Wars")].index
# year_df.drop(mask_three, inplace=True)
# year_df

#& (year_df['Is_Movie'] == 'Y')

# API call for information for sets in Star Wars theme and convert to dataframe. 
# parameters = {'theme' : 'Star Wars', 'pageSize' : 900}
# sw_set_list = requests.get(f"https://brickset.com/api/v3.asmx/getSets?apiKey={KEY_TWO}&userHash=&params={parameters}")
# sw_data = sw_set_list.json()
# sw_df = pd.json_normalize(sw_data,'sets')
# sw_df.to_csv('./sw_set_list.csv')

sw_df = pd.read_csv('sw_set_list.csv')

drop_columns(sw_df)


# Replace certain values with values matching first data frame
sw_df['subtheme'].replace(to_replace={'The Clone Wars' : 'Star Wars: The Clone Wars', 
                                       'The Force Awakens' : 'Episode VII', 
                                       'The Last Jedi' : 'Episode VIII', 
                                       'The Rise of Skywalker' : 'Episode IX' }, inplace=True)

# Drop any rows where the set has not been rated and where there is NaN for number of pieces.
mask_two = sw_df[sw_df['rating'] == 0].index
sw_df.drop(mask_two, inplace=True)
pieces_null = sw_df.isnull().values.any()
if pieces_null == True:
    sw_df.dropna(subset=['pieces'], inplace=True)

# Convert columns with numeric columns to Int64 Type 
sw_df['pieces'] = sw_df['pieces'].astype(pd.Int64Dtype())
sw_df['ageRange.min'] = sw_df['ageRange.min'].astype(pd.Int64Dtype())
sw_df['ageRange.max'] = sw_df['ageRange.max'].astype(pd.Int64Dtype())

# Run clean via partition function on the subtheme column of the second dataframe
part_colon(sw_df['subtheme'])


# Create a data frame that is the count of sets and average rating of each subtheme 
lego_set_count = sw_df.groupby(['subtheme'])['number'].count()
rating_avg=sw_df.groupby(['subtheme'])['rating'].mean().round(2)
agg_df = pd.concat([lego_set_count, rating_avg], axis=1)

# Create third data frame that is a combination of the first two cleaned dataframes, based on subtheme
merged_df = year_df.merge(agg_df, how='left', left_on='Title', right_on='subtheme')

merged_df.to_csv('./sw_set_list2.csv')
