import pandas as pd
df = pd.read_csv('data_0529.csv')


# Separating X and y
X = df.drop('Disease', axis=1)
Y = df['Disease']



# The hyperparameters
xgb_best_params = [{'learning_rate': 0.01, 'max_depth': 7, 'min_child_weight': 3, 'n_estimators': 300}]


import xgboost as xgb

# Use the best hyperparameters to create the XGBoost model
model = xgb.XGBClassifier(learning_rate=xgb_best_params[0]['learning_rate'],
                          max_depth=xgb_best_params[0]['max_depth'],
                          min_child_weight=xgb_best_params[0]['min_child_weight'],
                          n_estimators=xgb_best_params[0]['n_estimators'])


model.fit(X, Y)

# Saving the model
import pickle
pickle.dump(model, open('model_0529.pkl', 'wb'))
