FROM python:3.10
WORKDIR /chat_bot
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "chat_bot_app.py"]