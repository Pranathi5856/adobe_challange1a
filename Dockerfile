FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pdfminer.six==20221105 numpy 

COPY process_pdfs.py .

ENTRYPOINT ["python", "process_pdfs.py"]
