FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY wait-for-it.sh /app/wait-for-it.sh  # Adicionado

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/wait-for-it.sh  # Garantir permissão de execução

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]
