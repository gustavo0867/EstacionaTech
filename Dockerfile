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

# Exponha a porta do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando pra rodar
CMD ["flask", "run"]
