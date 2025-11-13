from features import load_dataset, clean_features, split_X_y, scale_features

path = 'data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'
df = load_dataset(path)
df = clean_features(df)

X, y, numeric_columns = split_X_y(df)
print("Shape before scaling:", X.shape)

X_scaled, scaler = scale_features(X)
print("Shape after scaling:", X_scaled.shape)
print("Example scaled values:", X_scaled[0][:5])
print("Labels:", y.unique()[:5])

