FROM python:3.10-slim
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./app/WarrantyValidation.py"]
EXPOSE 5000