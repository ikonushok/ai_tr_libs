class Super_Dooper():
  def __init__(self, remove_additional_data=True, convert_date_time_to_index=True):
    '''
    Если нужны дополнительные параметры, которые вычисляются при определении значений y,
    нужно поставить remove_additional_data=False
    
    По умолчанию колонки Дата-Время будут преобразованы в индекс DataFrame.
    Если не нужно преобразовывать Дату-Время в индекс, то указать convert_date_time_to_index=False
    '''
    self.prev = 0
    self.remove_additional_data = remove_additional_data
    self.convert_date_time_to_index = convert_date_time_to_index

  def __filter_orders(self, item):
    self.prev
    if item == 0:
      return None
    elif item != 0 and item != self.prev:
      self.prev = item
      return item
    elif item != 0 and item == self.prev:
      self.prev = item
      return None

  def mark_y(self, data):
    '''
    На вход подается dataset в виде pandas DataFrame с колонками (минимально):
    'Close'
    Если необходимо конвертировать в индекс дату и время, то должны быть еще колонки:
    'Date', 'Time' в формате %Y%m%d и %H%M%S, пример, 20210228 и 113000
    '''

    if self.convert_date_time_to_index:
      data['datetime'] = data[['Date','Time']].apply(lambda x: f'{x["Date"]}-{x["Time"]}', axis=1)
      date = pd.to_datetime(data['datetime'], format='%Y%m%d-%H%M%S')
      data.drop('datetime', axis=1, inplace=True)
      data.index = date

    data['min_sh'] = data['Close'].rolling(1, closed='left').min()
    data['max_sh'] = data['Close'].rolling(1, closed='left').max()
    data['min_long'] = data['Close'].rolling(5, closed='left').min()
    data['max_long'] = data['Close'].rolling(5, closed='left').max()
    data['min'] = data.apply(lambda x: (0,1)[int(x['min_sh'] == x['min_long'])], axis=1)
    data['max'] = data.apply(lambda x: (0,1)[int(x['max_sh'] == x['max_long'])], axis=1)
    data['Order'] = data['min'] - data['max']

    self.prev = 0
    data['Order'] = data['Order'][::-1].apply(self.__filter_orders)[::-1]
    data['Order'] = data['Order'].fillna(method='ffill')
    
    if self.remove_additional_data:
      data.drop(['min_sh','max_sh','min_long','max_long','min', 'max'], axis=1, inplace=True)

    return data
