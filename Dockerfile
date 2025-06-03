# Imagem base
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Copia as dependências primeiro
COPY requirements.txt .

# Instala dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Porta exposta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Comando para rodar
CMD ["python", "app.py"]