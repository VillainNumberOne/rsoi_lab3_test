FROM python:3
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

EXPOSE 8060
ENV PORT=8060

CMD ["sh", "entrypoint.sh"]