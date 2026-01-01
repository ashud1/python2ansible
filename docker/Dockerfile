FROM cytopia/ansible:latest

# switch to work directory in docker image
WORKDIR /app

#Copy all from app folder to app folder 
COPY app /app

# installing requirements
RUN pip install -r /app/requirement.txt

# expose docker port
EXPOSE 5000

# executed application
CMD [ "python" ,"app.py" ]