# 1 
FROM python:3.7

# 2
RUN pip install Flask gunicorn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# 3
COPY src/ /app
WORKDIR /app

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app








# FROM python:3.8-slim-buster
# WORKDIR /app
# ENV FLASK_APP=app.py
# # ENV FLASK_RUN_HOST=0.0.0.0
# # #erver will reload itself on file changes if in dev mode
# # ENV FLASK_ENV=production 
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# COPY companyblog companyblog /app/
# COPY migrations migrations /app/
# COPY model model /app/
# COPY app.py /app/
# RUN pip install Flask gunicorn
# ENV PORT 8080
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
# ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
# 1 
# FROM python:3.7

# 2


# 3
# COPY src/ /app
# WORKDIR /app

# 4


# 5
