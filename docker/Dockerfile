FROM cytopia/ansible:latest

WORKDIR /app

COPY app /app

RUN pip install flask

EXPOSE 5000

CMD [ "python" ,"app.py" ]