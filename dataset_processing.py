
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn import preprocessing

class DatasetProcessing:

    cols_to_predict = ["surge_multiplier", "price"]
    cols_to_fill = ["price", "surge_multiplier"]

    surge_predict = []
    price_predict = []

    def __init__(self, dataset):
        self.dataset = dataset
        self.__pre_processing()
      
      
    # methods
    def getDataset(self):
        return self.dataset

    def __pre_processing(self):
        cat_columns = self.dataset.select_dtypes('object').columns.tolist()
        dddataset = self.dataset.copy()

        # Transforming the categorical values in the dataset to numerical values
        for col in dddataset[cat_columns]:
            le = LabelEncoder()
            dddataset[col] = le.fit_transform(dddataset[col])
        self.processed_dataset = dddataset
       

        

    def predict_price_and_surge(self):
        for i in range(len(self.cols_to_predict)):
            # Creating a new dataset to work with at each iteration
            fill = self.processed_dataset.copy()

            # Filling the none values of the opposite missing column e.g to predict surge 
            # multiplier, we fill all missing values for price and vice versa
            fill[self.cols_to_fill[i]].fillna(fill[self.cols_to_fill[i]].mean(), inplace=True)

            # Making the column to predict the last column for easy selection
            popped_column = fill.pop(self.cols_to_predict[i])
            fill = pd.concat([fill, popped_column], axis = 1)
            
            # Selecting the missing rows of the column to predict
            missing = fill[fill[self.cols_to_predict[i]].isnull()]

            # Dropping the missing rows on the column to predict
            fill = fill.dropna()

            # Selecting the features (X) and the target (Y)
            X = fill.iloc[:, :-1].values
            Y = fill.iloc[:, -1].values

            # Using our preferred scaler to fit_transform the features
            X_scaled = Normalizer().fit_transform(X)
            regressor = KNeighborsRegressor()
            regressor.fit(X_scaled, Y)

            # Selecting the feature columns to predict the target in the current iteration
            X_test = missing.iloc[:, :-1].values

            # Fitting the features
            X_test_scaled = Normalizer().fit_transform(X_test)

            # Finally predicting the missing values
            predicted = regressor.predict(X_test_scaled)

            if i == 0:
                surge_predict = predicted
            else:
                price_predict = predicted
        # Filling the missing and outlier data from the original dataset
        final_dataset = self.dataset.copy()

        # Selecting the index of the missing surge_multiplier values
        missing_surge = final_dataset['surge_multiplier'].isna()

        # Adding the predicted surge_multiplier values to the dataset
        final_dataset.loc[missing_surge, "surge_multiplier"] = surge_predict

        # Selecting the index of the missing price values
        missing_price = final_dataset['price'].isna()

        # Adding the predicted price values to the dataset
        final_dataset.loc[missing_price, "price"] = price_predict

        self.price_predictions = final_dataset.loc[missing_price]
        self.surge_predictions = final_dataset.loc[missing_surge]

    def getResult(self):
        return [self.price_predictions, self.surge_predictions]
