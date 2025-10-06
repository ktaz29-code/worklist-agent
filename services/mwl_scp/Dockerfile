FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dicom_utils.py scp.py ./
EXPOSE 2762
CMD ["python", "scp.py"]
