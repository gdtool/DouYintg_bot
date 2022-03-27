#pip install pipreqs
#pipreqs requirements.txt
FROM python:3.10.2-slim-buster

RUN apt-get update && apt-get -y install  gcc
COPY . /app
RUN pip3 --no-cache-dir install --user -r /app/requirements.txt
WORKDIR /app
# -u print打印出来
CMD ["python3", "-u", "bot.py"]
