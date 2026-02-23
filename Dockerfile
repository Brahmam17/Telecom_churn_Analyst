<<<<<<< HEAD
From python:3.15.5-slim
copy . /app
workdir /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app

=======
From python:3.15.5-slim
copy . /app
workdir /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app

>>>>>>> 7a81fbc1ce43f410089e7467e638ff5a4aa2f226
