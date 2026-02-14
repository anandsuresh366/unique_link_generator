FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn","unique_link_generator.wsgi:application","--bind","0.0.0.0:8000"]
