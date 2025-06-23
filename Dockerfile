FROM python:3.12-slim

WORKDIR /app

COPY Bazario.Moderation/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

COPY Bazario.Moderation/ .
COPY Bazario.Docker/scripts/wait-for-it.sh ./scripts/wait-for-it.sh
COPY Bazario.Docker/scripts/entrypoints/bazario-moderation-entrypoint.sh ./scripts/entrypoints/bazario-moderation-entrypoint.sh
COPY Bazario.Moderation/SSL ./SSL

RUN chmod +x ./scripts/entrypoints/bazario-moderation-entrypoint.sh ./scripts/wait-for-it.sh
RUN sed -i 's/\r$//' ./scripts/wait-for-it.sh
RUN sed -i 's/\r$//' ./scripts/entrypoints/bazario-moderation-entrypoint.sh

EXPOSE 5009
EXPOSE 5010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5009"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5010", "--ssl-keyfile","/app/SSL/key.pem","--ssl-certfile","/app/SSL/cert.pem"]

 