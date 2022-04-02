### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ikuz57/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Отдельно можно импортировать тестовые данные:

```
python3 manage.py import_csv
```

Запустить проект:

```
python3 manage.py runserver
```

