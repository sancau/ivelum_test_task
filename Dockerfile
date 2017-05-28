FROM python:3-onbuild
ENV PYTHONPATH $PYTHONPATH:/usr/src/app/src
EXPOSE 8080
CMD [ "python", "./src/proxyhttp.py", "--host", "0.0.0.0", "--port", "8080", "--target", "habrahabr.ru" ]
