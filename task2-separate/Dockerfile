# Task 2: run the tests in test_refund.py with pytest
FROM python:3.13-slim
RUN pip install pytest==9.2.0
WORKDIR /app
COPY . .
CMD ["python", "-m", "pytest", "-v"]
