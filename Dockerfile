FROM python:3.11-slim

# প্রয়োজনীয় বেসিক সিস্টেম প্যাকেজ ইনস্টল করা
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound-dev \
    libportaudio2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# পাইথন প্যাকেজ ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# অ্যাপ্লিকেশন রান করা
CMD ["uvicorn", "src.orchestrator:app", "--host", "0.0.0.0", "--port", "10000"]
