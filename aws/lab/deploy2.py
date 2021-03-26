import pandas as pd      
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
import warnings
warnings.filterwarnings('ignore')
import xgboost


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    mse = mean_squared_error(actual, pred)
    score = r2_score(actual, pred)
    return print("r2_score:", score, "\n","mae:", mae, "\n","mse:",mse, "\n","rmse:",rmse)



df=pd.read_pickle("golden_data_not_dummy.pkl")
pd.set_option('display.max_columns', None)

new_list=["age", "hp", "km", "model"]


X=df[new_list]
y=df['price']
X=pd.get_dummies(X)

# X.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


model = xgboost.XGBRegressor()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
# eval_metrics(y_test, y_pred)


from sklearn.ensemble import RandomForestRegressor
rf_reg=RandomForestRegressor()
rf_reg.fit(X_train, y_train)

y_pred2 = rf_reg.predict(X_test)


# eval_metrics(y_test,y_pred2)


import pickle
import pandas as pd
pickle.dump(rf_reg, open('rf_model', 'wb'))
pickle.dump(model, open('xgb_model', 'wb'))


richard_model = pickle.load(open('xgb_model', 'rb'))

import streamlit as st
age = int(st.slider("Age...",0,20,2))
hp = int(st.text_input("HP...",value="105"))
km = int(st.text_input("km", value="100000"))
model = st.selectbox("model",('A1', 'A2',	'A3', 'Astra', 'Clio', 	'Corsa', 'Espace','Insignia'))
my_dict = {
    "age":  int(age),
    "hp": int(hp), 
    "km": int(km),
    "model": model
}
# my_dict = {
#     "age": 2,
#     "hp": 105,
#     "km": 100000,
#     "model": 'Astra'
# }

df = pd.DataFrame.from_dict([my_dict])



columns=list(X.columns)
df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)

prediction = richard_model.predict(df)
button = st.button("P R E D I C T")
x = f"€ {prediction[0]:,.2f}"
if button:
    st.write(x)


# print("The estimated price of your car is €{}. ".format(int(prediction[0])))



