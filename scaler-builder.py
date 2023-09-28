import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd
df = pd.read_csv('data_0529.csv')


# Separating X and y
X = df.drop('Disease', axis=1)
Y = df['Disease']
# Assume that you have your input data stored in a numpy array called 'X'

# Create an instance of StandardScaler
scaler = StandardScaler()
scaler.fit(X)
# Save the scaler to a pickle file called 'scaler.pkl'
with open('scaler_0529.pkl', 'wb') as f:
    pickle.dump(scaler, f)
