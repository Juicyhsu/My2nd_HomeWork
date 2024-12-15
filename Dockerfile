FROM --platform=linux/amd64 python
COPY Gemini.py /app/
COPY requirements.txt /app/
COPY static /app/static/

WORKDIR /app
RUN pip install -r requirements.txt

ENV GOOGLE_API_KEY="我的金鑰(密)"

ENTRYPOINT ["python","Gemini.py"]