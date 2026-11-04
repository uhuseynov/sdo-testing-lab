# SDO Testing Lab

Practice files for the Software Testing tutorial (Software Development and Operations, Constructor University).

| Folder | What you practise |
| --- | --- |
| `task1-inside/` | Tests **inside** the file: doctest (we do it together) |
| `task2-separate/` | Tests in a **separate** file: pytest, find 2 bugs |
| `task3-break-it/` | Be the tester: borders, `parametrize`, `pytest.raises` |

## Run the tests (Windows, macOS and Linux)

Inside a task folder:

```
docker build -t task1 .
docker run --rm task1
```

Change the code or the tests, then build and run again.
Windows: use PowerShell.

## Plan B: no Docker? Use Python 3.10+ directly

Run once, in the `sdo-testing-lab` folder:

| | Windows (PowerShell) | macOS / Linux |
| --- | --- | --- |
| Create a virtual environment | `py -m venv .venv` | `python3 -m venv .venv` |
| Activate it | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Install pytest | `python -m pip install pytest` | `python -m pip install pytest` |

Then, inside a task folder:

- Task 1: `python -m doctest -v converter.py`
- Task 2 and 3: `python -m pytest -v`
