FROM python:3.9.0rc1-buster

#make a directory for our application
WORKDIR /app


#install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy source code
COPY / .

#run application
CMD ["python","app.py"]