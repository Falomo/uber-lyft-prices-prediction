
import pandas as pd
import numpy as np

class DatasetOutput:

    def __init__(self, dataset):
        self.dataset = dataset
      
    # methods
    def csvOutput(self, name):
        return self.dataset.to_csv(name)

    def hd5Output(self, name, key):
        return self.dataset.to_hdf(name,  key, mode='w')
