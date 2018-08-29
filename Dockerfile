FROM python:3
ADD main.py /
RUN pip install requests
ENTRYPOINT ["python", "./main.py"]