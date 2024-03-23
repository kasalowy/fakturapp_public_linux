import pandas as pd

# Function performing data transformation
def transform_data_1(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.iloc[:, :50]
    return df