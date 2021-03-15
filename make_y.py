f_name = 'Extremum_marked_SBER_MIN60.txt'
path = '/content/drive/MyDrive/Colab Notebooks/Трейдинг/data/marked_data'
data = pd.read_csv(f'{path}/{f_name}', sep=',', index_col=0)
data.columns = ['Open', 'High', 'Low', 'Close', 'Date', 'Time', 'Order']

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

prev = 0
def filter_orders(item):
  global prev
  if item == 0:
    return None
  elif item != 0 and item != prev:
    prev = item
    return item
  elif item != 0 and item == prev:
    prev = item
    return None

data['Order'] = data['Order'][::-1].apply(filter_orders)[::-1]
data['Order'] = data['Order'].fillna(method='ffill')

data
