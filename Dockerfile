FROM python:3.8
WORKDIR /bac-kend-python
COPY ./requirements.txt /bac-kend-python/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /bac-kend-python
CMD ["python3", "app.py"]
