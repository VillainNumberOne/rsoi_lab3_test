FROM python:3
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

EXPOSE 8080
ENV PORT=8080

CMD ["sh", "./entrypoint.sh"]