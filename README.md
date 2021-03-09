#### ai_tr_libs
Additional libs for AI and algorithmic trading scripts


#### Вставить в ноутбук строку для скачивания библиотеки из Github
!curl --remote-name --location https://raw.githubusercontent.com/chekh/ai_tr_libs/main/dataloader.py

#### Пример использования библиотеки для загрузки данных

from dataloader import Dataloader as dl
data = dl('ABRD', start_date='01-01-2021')
data.get_data()
