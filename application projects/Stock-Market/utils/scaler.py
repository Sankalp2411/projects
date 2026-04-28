from sklearn.preprocessing import MinMaxScaler

def get_scaler():
    return MinMaxScaler(feature_range=(0, 1))