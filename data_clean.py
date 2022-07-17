import pandas as pd

# List of columns to drop. Columns are not used in this project. 
def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    drop_list = [
             'numberVariant',
                'released',
                'category',
                'bricksetURL',
                'reviewCount',
                'packagingType',
                'availability',
                'instructionsCount',
                'additionalImageCount',
                'lastUpdated',
                'image.thumbnailURL',
                'image.imageURL',
                'collections.ownedBy',
                'collections.wantedBy',
                'dimensions.height',
                'dimensions.width',
                'dimensions.depth',
                'LEGOCom.US.retailPrice',
                'LEGOCom.US.dateFirstAvailable',
                'LEGOCom.US.dateLastAvailable',
                'LEGOCom.UK.retailPrice',
                'LEGOCom.UK.dateFirstAvailable',
                'LEGOCom.UK.dateLastAvailable',
                'LEGOCom.CA.retailPrice',
                'LEGOCom.CA.dateFirstAvailable',
                'LEGOCom.CA.dateLastAvailable',
                'dimensions.weight',
                'barcode.EAN',
                'barcode.UPC',
                'minifigs',
                'LEGOCom.DE.retailPrice',
                'LEGOCom.DE.dateFirstAvailable',
                'LEGOCom.DE.dateLastAvailable'
                ]
    df.drop(columns=drop_list, inplace=True)

def convert_to_int(column: pd.Series) -> pd.Series:
    column = column.astype(pd.Int64Dtype())
    return column