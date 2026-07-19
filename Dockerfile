FROM python:3.11-slim

# সার্ভারের জন্য প্রয়োজনীয় সিস্টেম লাইব্রেরি (hnswlib কম্পাইল করার জন্য g++ সহ)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    portaudio19-dev \
    libasound-dev \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# পাইথন ডিপেন্ডেন্সি ইনস্টল প্রক্রিয়া
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# মেইন অ্যাপ্লিকেশন রান করার ফাইনাল কমান্ড
CMD ["uvicorn", "src.orchestrator:app", "--host", "0.0.0.0", "--port", "10000"]
