FROM python:3

# Change the WORKDIR to the directory where this repository has been cloned
WORKDIR /home/ahamshubham/Downloads/Personal/Jobs/Ansys

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python application.py

# CMD pytest testing.py -s --verbose