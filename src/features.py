import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

LABEL_COLUMN = 'Label'

def load_dataset(path):
    # Load CSV and Clean Headers
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    return df

def clean_features(df):
    # Drop columns not useful for ML
    drop_columns = [
        ' Flow ID',
        ' Source IP',
        ' Source Port',
        ' Destination IP',
        ' Destination Port',
        ' Timestamp'
    ]
    for c in drop_columns:
        if c in df.columns:
            df = df.drop(columns=[c])

    # Drop rows with missing values
    df = df.dropna()

    # Convert categorical labels to strings
    df.loc[:, LABEL_COLUMN] = df[LABEL_COLUMN].astype(str).str.strip() # loc is used to select a single column by name and assign a new value to it


    return df

def split_X_y(df):
    X = df.drop(columns=[LABEL_COLUMN])
    y = df[LABEL_COLUMN]
    numeric_columns = X.select_dtypes(include=[np.number]).columns.tolist()
    return X[numeric_columns], y, numeric_columns

def scale_features(X):
    # --- New: handle infinities and large values ---
    # Replace infinities (∞) with NaN so we can handle them
    X = X.replace([np.inf, -np.inf], np.nan)
    
    # Fill NaN with median values (so we don't lose data)
    X = X.fillna(X.median(numeric_only=True))
    
    # Optional: clip extreme outliers to a safe range
    X = X.clip(lower=-1e6, upper=1e6)
    
    # --- Now scale safely ---
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    return X_scaled, scaler
