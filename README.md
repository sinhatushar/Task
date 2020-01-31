# Task

Requirements : 

> Python > 3.6

> Django 3.0.2

> Postman API (to test REST APIs)

> Swagger tool (to display swagger documentation in UI)

> Running internet connection.

Steps :

Go to Processing/config.py and edit these variables : JSON_FILE_URL, LOG_FILE_URL and STORAGE_DIR. STORAGE_DIR is the path of the directory where you want to store the files. This folder needs to be made on the local computer. The program doesn't itself create the 'Storage' folder.

Go inside TCProject folder(inside project_path/TCProject and not inside project_path/TCProject/TCProject)and type the following command:

> python manage.py runserver

Go to any web broswer and type http://127.0.0.1:8000/. The website will open and then the UI is self explanatory.
