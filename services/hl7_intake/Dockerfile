FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY hl7_utils.py mllp_server.py watcher.py start.sh ./
RUN chmod +x start.sh
EXPOSE 2575
CMD ["/bin/sh", "/app/start.sh"]
