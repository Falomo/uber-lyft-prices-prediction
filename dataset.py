
import pandas as pd
import numpy as np

class Dataset:

    def __init__(self, dataset):
        dataset = dataset.sample(frac=0.02).copy()

        # Setting the time_stamp as the dataset index
        dataset['time_stamp'] = pd.to_datetime(dataset['time_stamp'], unit = 'ms')
        dataset = dataset.set_index('time_stamp').sort_index()

        # Making price the last column on our dataset
        dataset = dataset.drop(["id","product_id"], axis=1)
        price = dataset.pop('price')
        self.dataset = pd.concat([dataset, price], axis = 1)
        self.__compute_outliers()
      
      
    # methods
    def getDataset(self):
        return self.dataset

    def __compute_outliers(self):
        # Calculating quantile range for outliers
        surge_quantiles = self.dataset[['surge_multiplier']].quantile([.05, .99])
        price_quantiles = self.dataset[['price']].quantile([.05, .95])

        # Getting all outliers
        surge_multiplier_outliers = self.dataset[(self.dataset['surge_multiplier'] < surge_quantiles['surge_multiplier'].iloc[0]) | (self.dataset['surge_multiplier'] >= surge_quantiles['surge_multiplier'].iloc[1])]
        price_outliers =  self.dataset[(self.dataset['price'] <= price_quantiles['price'].iloc[0]) | (self.dataset['price'] >= price_quantiles['price'].iloc[1])]
        self.surge_multiplier_outliers = surge_multiplier_outliers
        self.price_outliers = price_outliers

    def get_outliers(self):
        return [self.surge_multiplier_outliers, self.price_outliers]

    def set_outliers_to_nan(self):
        self.dataset.loc[self.surge_multiplier_outliers.index, "surge_multiplier"] = np.nan 
        self.dataset.loc[self.price_outliers.index, "price"] = np.nan 


  
# explicit function      
def method():
    print("GFG")