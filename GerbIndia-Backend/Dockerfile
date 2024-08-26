FROM python:3.7.5


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV IP_ADDRESS="172.18.100.240"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6969"]