FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Tell Koyeb we expose port 8000
EXPOSE 8000

CMD ["python", "bot.py"]
