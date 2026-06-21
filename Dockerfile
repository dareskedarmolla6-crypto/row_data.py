# ==================================================
# FSE CRYPTO TRADING BOT - DOCKER CONFIGURATION
# ==================================================

# 1. Official Python lightweight image
FROM python:3.9-slim

# 2. Python logs ወዲያውኑ እንዲታዩ
ENV PYTHONUNBUFFERED=1

# 3. የስራ ፎልደር
WORKDIR /app

# 4. pip ማዘመን
RUN pip install --upgrade pip

# 5. Requirements በመጀመሪያ መቅዳት
COPY requirements.txt .

# 6. የሚያስፈልጉ ላይብረሪዎችን መጫን
RUN pip install --no-cache-dir -r requirements.txt

# 7. የተቀረውን FSE project መቅዳት
COPY . .

# 8. ኮንቴይነሩ ሲነሳ FSE እንዲጀምር
CMD ["python", "main.py"]
