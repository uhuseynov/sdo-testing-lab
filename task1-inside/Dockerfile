# Task 1: run the tests that live INSIDE converter.py
FROM python:3.13-slim
WORKDIR /app
COPY converter.py .
# doctest is built into Python - nothing to install
CMD ["python", "-m", "doctest", "-v", "converter.py"]
