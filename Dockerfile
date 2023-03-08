FROM python

RUN pip install -- upgrade pip

Workdir /Semabox

ADD . /Semabox

RUN pip install -r requirements.txt 

CMD ["python","Site.py"]

HEALTHCHECK --interval=1m --timeout=30s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

