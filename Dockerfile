FROM --platform=linux/amd64 python
COPY Gemini.py /app/
COPY requirements.txt /app/
COPY static /app/static/

WORKDIR /app
RUN pip install -r requirements.txt

ENV GOOGLE_API_KEY="AIzaSyC4zNFcHmJuIrKMHz6bFGHscjejbVKr06A"

ENTRYPOINT ["python","Gemini.py"]