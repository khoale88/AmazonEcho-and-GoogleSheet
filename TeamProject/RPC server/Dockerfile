#A simple Flask app container
FROM python:3.5.2
MAINTAINER khoale88 "lenguyenkhoa1988@gmail.com"

#Place app in container
COPY . /app
WORKDIR /app

#Install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]