FROM python:3.10-slim
WORKDIR /usr/src/app
COPY ./app/ /usr/src/app/
COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./WarrantyClaimOrchestrator.py"]
EXPOSE 5000