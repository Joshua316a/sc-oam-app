FROM python:3.13-slim

# ─── Python Dependencies ───
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── App Source ───
COPY app.py .

# ─── Expose Ports ───
EXPOSE 8000

# ─── Entry Point ───
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]