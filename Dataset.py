
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, LabelEncoder, OneHotEncoder 
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
import pandas as pd
import numpy as np
from pandas import DataFrame as df


class Dataset():
  def __init__(self, dataset, batch_size, ensemble, one_hot_enc=True, dropna=False, **kwargs):
    self.featurized = False
    self.data = dataset
    self.batch_size = batch_size
    self.ensemble = ensemble
    self.dropna = dropna
    self.one_hot_enc = one_hot_enc
    self.shape = self.data.shape

    self.training_start_index = 0 if 'training_start_index' not in kwargs.keys() else kwargs['training_start_index']
    self.val_start_index = 0 if 'val_start_index' not in kwargs.keys() else kwargs['val_start_index']
    self.test_start_index = 0 if 'test_start_index' not in kwargs.keys() else kwargs['test_start_index']
    self.training_end_index = self.shape[0] - 1 if 'training_end_index' not in kwargs.keys() else kwargs['training_end_index']
    self.val_end_index = self.shape[0] - 1 if 'val_end_index' not in kwargs.keys() else kwargs['val_end_index']
    self.test_end_index = self.shape[0] - 1 if 'test_end_index' not in kwargs.keys() else kwargs['test_end_index']

    self.featurize()


  def featurize(self):
    if self.one_hot_enc:
      self.one_hot_encode_y()

    temp = self.data.copy()
    temp.drop(['Ticker', 'Per', 'Date', 'Time'], axis=1, inplace=True)
    temp['sin'] = temp['Close'].apply(lambda x: np.sin(x))
    
    if self.dropna:
      temp.dropna(axis=0, inplace=True)

    xScaler = RobustScaler()
    self.X = xScaler.fit_transform(temp)

    self.input_shape = (self.ensemble, self.X.shape[1])

    self.featurized = True


  def one_hot_encode_y(self):
    self.y = self.data['Signal'].copy().to_numpy().reshape(-1,1)
    self.y_encoder = OneHotEncoder().fit(self.y)
    self.y = self.y_encoder.transform(self.y).toarray()


  def __ts(self, start_index, end_index):
    assert self.featurized, 'Dataset is not featuarized yet, perform Dataset.featurize()!'
    return TimeseriesGenerator(self.X, self.y, length=self.ensemble, sampling_rate=1, 
                              start_index=start_index, end_index=end_index, 
                              batch_size=self.batch_size)


  def train(self, start_index=None, end_index=None):
    start = (self.training_start_index, start_index)[start_index != None]
    end = (self.training_end_index, end_index)[end_index != None]
    assert self.featurized, 'Dataset is not featuarized yet, perform Dataset.featurize()!'
    return self.__ts(start, end)


  def val(self, start_index=None, end_index=None):
    start = (self.val_start_index, start_index)[start_index != None]
    end = (self.val_end_index, end_index)[end_index != None]
    assert self.featurized, 'Dataset is not featuarized yet, perform Dataset.featurize()!'
    return self.__ts(start, end)


  def test(self, start_index=None, end_index=None):
    start = (self.test_start_index, start_index)[start_index != None]
    end = (self.test_end_index, end_index)[end_index != None]
    assert self.featurized, 'Dataset is not featuarized yet, perform Dataset.featurize()!'
    return self.__ts(start, end)


  def test_prep_dec(self, prep):
    assert self.featurized, 'Dataset is not featuarized yet, perform Dataset.featurize()!'
    assert self.test_end_index + 1 - self.test_start_index - self.ensemble == prep.shape[0], 'Length of prediction is not equal length of source data.'
    if self.one_hot_enc:
      prep = self.y_encoder.inverse_transform(prep)
    else:
      assert prep.shape[1] == 1, 'Wrong shape dimension of predicted data.'
    res = df() 
    res = self.data[['Open', 'High', 'Low', 'Close']][self.test_start_index + self.ensemble: self.test_end_index + 1].copy()
    res['Signal'] = prep
    return res


# Пример использования
#ds = Dataset(data, 1, 10, test_start_index=14900)
#ds.test_end_index - 14900
#ds.featurize()
#ds.train(0,20)[0]
#ds.one_hot_encode_y()
#ddd = ds.test_prep_dec(np.array(np.random.randint(-1,2,(40,2))))
#ds.y_encoder.inverse_transform([[1.,0.]])
#ds.test()[0]
