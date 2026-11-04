# Task 1: run the tests that live INSIDE leap_year.py
FROM python:3.13-slim
WORKDIR /app
COPY leap_year.py .
# doctest is built into Python - nothing to install
CMD ["python", "-m", "doctest", "-v", "leap_year.py"]
