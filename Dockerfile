# Use uma imagem Python oficial como imagem base
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Impede o Python de gravar arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE 1
# Garante que a saída do Python seja enviada diretamente para o terminal (sem buffer)
ENV PYTHONUNBUFFERED 1

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Baixa o modelo de linguagem do spaCy para português
RUN python -m spacy download pt_core_news_sm

# Copia o restante do código da aplicação para o diretório de trabalho
# Copiando as pastas 'backend' e 'docs' para dentro do /app
COPY ./backend/ /app/backend/
COPY ./docs/ /app/docs/

# Define o PYTHONPATH para que os módulos sejam encontrados
ENV PYTHONPATH=/app

# Executa o script para construir o índice FAISS
# O script está em backend/rag/build_index.py e precisa acessar ../docs/base_conhecimento.txt
# Como copiamos backend -> /app/backend e docs -> /app/docs, o caminho relativo funciona.
RUN python backend/rag/build_index.py

# Expõe a porta em que o app estará rodando
EXPOSE 8000

# Comando para iniciar a aplicação usando Uvicorn
# O host 0.0.0.0 torna o servidor acessível de fora do container
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
