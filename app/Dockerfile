FROM python:3.10-slim

WORKDIR /app

# Copiar apenas o arquivo requirements.txt
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código-fonte
COPY . /app/

# Copiar o script wait-for-it.sh e garantir permissão de execução
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Definir o comando de inicialização
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]
