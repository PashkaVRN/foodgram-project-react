Foodgram - проект позволяет:

- Просматривать рецепты
- Добавлять рецепты в избранное
- Публикование рецепты
- Удалять собственные рецепты или редактировать их
- Скачивать список покупок

## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone git@github.com:PashkaVRN/foodgram-project-react.git
```

***- Установите и активируйте виртуальное окружение:***
- для MacOS
```
python3 -m venv venv
```
- для Windows
```
python -m venv venv
source venv/bin/activate
source venv/Scripts/activate
```

***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python manage.py migrate
```

***- В папке с файлом manage.py выполните команду:***
```
python manage.py runserver
```
***- Документация доступна по адресу:***
```
http://127.0.0.1/api/docs/
```

