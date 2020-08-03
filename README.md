Backend of Vimanasahti is build on Python and is deployed on AWS cloud.

1. Install your virtual Environment

pip3 install virtualenv


2. Install Django

pip3 install django


3.Install requirements

pip install -r requirements.txt 


4.Migrate the database

python manage.py migrate

5. Runserver

python manage.py runserver

6. Run Celery Server

celery -P solo -A vimanathi --loglevel=info
