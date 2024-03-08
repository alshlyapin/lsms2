FROM python:3.10
WORKDIR /backend_engine
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=backend_llm.py
ENV FLASK_RUN_HOST=0.0.0.0
ENTRYPOINT ["flask", "run"]