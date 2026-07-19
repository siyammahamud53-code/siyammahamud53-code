FROM python:3.11-slim

# ফিউচার প্রুফ এবং সব ফিচারের জন্য মিনিমালিস্টিক সিস্টেম ডিপেন্ডেন্সি
RUN apt-get update && apt-get install -y \
    gcc \
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

# অ্যাপ্লিকেশন রান করার ফাইনাল কমান্ড
CMD ["uvicorn", "src.orchestrator:app", "--host", "0.0.0.0", "--port", "10000"]
