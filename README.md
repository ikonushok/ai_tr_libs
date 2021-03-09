# ai_tr_libs
# Additional libs for AI and algorithmic trading scripts


Вставить в ноутбук строку для скачивания библиотеки из Github
```
!curl --remote-name --location https://raw.githubusercontent.com/chekh/ai_tr_libs/main/dataloader.py
```

Пример использования библиотеки для загрузки данных
```
from dataloader import Dataloader as dl
data = dl('ABRD', start_date='01-01-2021')
data.get_data()
```

API:

**Class Dataloader(ticker, period='hour', start_date='01-01-2014', end_date=None, save_to_file=False, data_path=None, overwrite=True, capitalize=False)**

```
ticker - код акции 
period - период, доступные значения: 'tick', 'min', '5min', '10min', '15min', '30min', 'hour', 'daily', 'week', 'month'
start_date - дата начала периода для скачивания истории в формате "ДД-ММ-ГГГГ" (должна быть не раньше 01-01-2014)
end_date - дата окончания периода для скачивания истории в формате "ДД-ММ-ГГГГ"
data_path - путь к папке куда должен быть сохранен файл с данными
overwrite - перезаписывать файл, если файл с таким именем уже существует.
```

**def get_all_ticker(self)**
```
Возвращает все доступные тикеры 
```

**def get_ticker(self)**
```
Возвращает установленный тикер 
```

**def set_ticker(self, ticker)**
```
Устанавливает тикер
```

**def get_periods(self)**
```
Возвращает установленный период 
```

**def set_period(self, period)**
```
Устанавливает период period, 
доступные значения: 
'tick', 'min', '5min', '10min', '15min', '30min', 'hour', 'daily', 'week', 'month'
```

**def set_data_path(self, data_path)**
```
Устанавливает директорию для сохранения файла
```

**def get_data(self)**
```
Возвращает данные, либо сохраняет данные в файл, который был указан при создании объекта
```
