# SDO Testing Lab: find the bugs before your users do

Practice files for the Software Testing tutorial (Software Development and Operations, Constructor University).

You already know Git and Docker. Today you use them for one purpose: **running a program on purpose, with the
intent of finding errors**, before a user finds them.

You write tests in two places, and then you try to break the code:

```
  Task 3   BREAK IT          borders and bad input: try to make the code fail   (you, alone first)
  Task 2   SEPARATE FILE     the tests live in their own file test_refund.py     (you, alone first)
  Task 1   INSIDE THE FILE   the tests live in the docstring of the function     (together)
```

**The big idea of today:** a developer tests "gently". A tester tries to **break** the code. Today you are the tester.

| Task | Where do the tests live? | Tool | Who |
|------|--------------------------|------|-----|
| 1 | inside `leap_year.py` | `doctest` (built into Python) | we do it together |
| 2 | in a separate file, `test_refund.py` | `pytest` | you try alone first |
| 3 | in a separate file, many cases at once | `pytest` | you try alone first |

## Time plan (60 minutes, after the intro)

| Time | Step | Topic |
|------|------|-------|
| 0:00 | [Before you start](#before-you-start-8-min) | Check your setup, get the code |
| 0:08 | [Task 1](#task-1---tests-inside-the-file-12-min) | Tests inside the file |
| 0:20 | [Task 2](#task-2---tests-in-a-separate-file-20-min) | Tests in a separate file |
| 0:40 | [Task 3](#task-3---break-it-15-min) | Break it! |
| 0:55 | [Wrap-up](#wrap-up) | What you practised |

## What is in this repository

| File | What it is |
|------|------------|
| `task1-inside/leap_year.py` | A leap year check. The rule is at the top of the file, the tests live in the docstring. |
| `task2-separate/refund.py` | A train delay refund calculator. The rules are at the top of the file. |
| `task2-separate/test_refund.py` | The tests for `refund.py`, with blanks `____` for you to fill in. |
| `task3-break-it/refund.py` | The same calculator, with the Task 2 fixes and one new rule. |
| `task3-break-it/test_refund.py` | Border tests and bad-input tests, with blanks. |
| `*/Dockerfile` | Every task folder has one. It packs Python and runs the tests of that folder. |

The solutions are **not** in this repository. They are shown on the slides after each task.

## Before you start (8 min)

Check that your tools work (you installed them for the Docker tutorial):

```bash
docker --version
docker ps
git --version
docker pull python:3.13-slim
```

Start the last command **right now**. All three tasks need this image, and 30 laptops on one Wi-Fi take a while.

|  | Windows | macOS | Linux |
|--|---------|-------|-------|
| Terminal | PowerShell (not Git Bash) | Terminal app | any terminal |
| Start Docker | open the Docker Desktop app | `open -a Docker` | `sudo systemctl start docker` |

**Get the code:**

```bash
git clone https://github.com/uhuseynov/sdo-testing-lab.git
cd sdo-testing-lab
```

You commit after every task, but you do **not** push. The commits are your local practice.

**The loop for every task:**

```
  edit the test or the code  ->  docker build  ->  docker run  ->  read the result
             ^                                                            |
             +------------------- something FAILED? ----------------------+
```

Inside a task folder (use `task1`, `task2` or `task3` as the name):

```bash
docker build -t task1 .
docker run --rm task1
```

`--rm` deletes the container after the run, because you will run the tests many times.
**Always build again after you change a file:** the image holds a copy of your code.

### Plan B: no Docker? Use Python 3.10+ directly

Run once, in the `sdo-testing-lab` folder:

|  | Windows (PowerShell) | macOS / Linux |
|--|----------------------|---------------|
| Create a virtual environment | `py -m venv .venv` | `python3 -m venv .venv` |
| Activate it | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Install pytest | `python -m pip install pytest` | `python -m pip install pytest` |

Then, inside a task folder, use these commands instead of `docker build` + `docker run`:

- Task 1: `python -m doctest -v leap_year.py`
- Task 2 and 3: `python -m pytest -v`

---

## Task 1 - Tests inside the file (12 min)

**We do this one together, step by step.** Type the same things on your laptop.

### 1a. Read the two files (4 min)

```bash
cd task1-inside
```

Open `leap_year.py`. At the top you find the **rule** (the specification):

```
  * a year divisible by 4 is a leap year,
  * except a year divisible by 100: that is NOT a leap year,
  * except a year divisible by 400: that IS a leap year again.
```

Below it is the function:

```python
def is_leap_year(year):
    """Return True if the year has 366 days.

    Each >>> line is a test. Python runs it and
    checks the result on the next line.

    >>> is_leap_year(2024)
    True
    """
    return year % 4 == 0
```

The text between the `"""` is the **docstring**. Every line that starts with `>>>` is a test: Python runs it and
compares the result with the line under it. The tests live **inside** the file, next to the code.

Now open the `Dockerfile`.

1. Which line runs the tests?
2. Why does this `Dockerfile` not install anything extra for the tests?

### 1b. Run the first test (2 min)

```bash
docker build -t task1 .
docker run --rm task1
```

At the end of the output you should see:

```
1 passed.
Test passed.
```

> **Think:** one test passed. Does that mean the function is correct?

### 1c. Add a second test (4 min)

Quick question before you type: **is 1900 a leap year?** Guess first, then check it with the rule.

Add these two lines **right under `True`**, with the same indentation:

```python
    >>> is_leap_year(1900)
    False
```

Build and run again. Read the output: which example failed, what was **Expected**, and what did you **Get**?

**Questions**

1. Which part of the rule does the code forget?
2. The first test (2024) passed, although the bug was already there. Why?

Fix the last line of the function so it follows the rule. Build and run until you see `Test passed.` again.

### 1d. One more test (2 min)

2000 is divisible by 100, but also by 400. Use the rule to decide what `is_leap_year(2000)` must return, and write
this test yourself, under the others. Build and run.

Does your fix from 1c still pass? If not, the new test just caught a fix that was only half right. Fix it again.

### Commit

```bash
git add .
git commit -m "Task 1 done"
```

> **Task 1 done.** Your tests live next to the code, and they also show how to use the function.

---

## Task 2 - Tests in a separate file (20 min)

**Try it yourself first!** After about 15 minutes the solution is shown on the slides.

```bash
cd ../task2-separate
```

### 2a. Read the rules, not the code (3 min)

A tester starts from the **rules** (the specification), not from the code. The rules are at the top of `refund.py`:

```
  * delay of at least  60 minutes -> 25 % of the ticket price back
  * delay of at least 120 minutes -> 50 % of the ticket price back
  * a refund below 4.00 euro is not paid out -> 0.0
```

Do **not** read the code of `refund()` yet!

### 2b. Fill in the blanks (5 min)

Open `test_refund.py`. The first test is already done for you:

```python
from refund import refund


# Example - already done for you
def test_short_delay_gives_nothing():
    assert refund(80.0, 30) == 0.0
```

Every other test has a blank `____`. Replace each blank with the refund you **expect**, calculated from the rules.
For the last test, pick your own ticket price and delay that give exactly 4.00 euro.

pytest finds every file whose name starts with `test_`, and every function in it that starts with `test_`.
`assert` is plain Python: if the comparison is false, the test fails.

### 2c. Run the tests (2 min)

```bash
docker build -t task2 .
docker run --rm task2
```

If you see this, you still have a blank to fill in:

```
E       NameError: name '____' is not defined
```

When all blanks are filled, **some tests FAIL. Great: you found bugs!** There are 2 bugs in `refund.py`.

Read one failure. pytest shows both sides of the `==`:

```
assert <what the code returned> == <what you expected>
```

### 2d. Find and fix the bugs (8 min)

Now open the code of `refund()`. Look at the delays of the failing tests and compare them with the `if` lines.
Fix both bugs. Build and run until every test says `PASSED`.

**Questions**

1. Which delays made the tests fail? Why are exactly these values dangerous?
2. One of your tests passed although both bugs were in the code. Which one? Why did it not find them?

### Commit

```bash
git add .
git commit -m "Task 2 done"
```

> **Task 2 done.** The tests live in their own file, so they can grow without making the code longer.

---

## Task 3 - Break it! (15 min)

**Try it yourself first!** You are the independent tester now: think about the borders, and about input that
"should never happen".

```bash
cd ../task3-break-it
```

`refund.py` here already has the Task 2 fixes, and one new rule:

```
  * a negative ticket price or delay is invalid -> raise ValueError
```

The code does **not** follow this rule yet.

### 3a. One test, many cases (5 min)

`test_borders` is **one** test function with a table of 4 rows. pytest runs it once per row:

```python
@pytest.mark.parametrize("delay, expected", [
    (59, 0.0),
    (60, 20.0),
    (119, ____),
    (120, ____),
])
def test_borders(delay, expected):
    assert refund(80.0, delay) == expected
```

Fill in the 2 blanks. (Until you do, pytest cannot even load the file: you get a `NameError` during collection.)
Want more? Add a row of your own.

### 3b. Bad input must fail (5 min)

What does `refund(-80.0, 90)` return right now? A negative price makes no sense, so the rule says: raise a
`ValueError`. The first bad-input test checks this:

```python
def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        refund(-80.0, 90)
```

`pytest.raises(ValueError)` means: the code inside this block **must** raise a `ValueError`, otherwise the test fails.

Replace the `____` in `test_negative_delay_is_rejected` with your own test for a **negative delay**.
Build and run:

```bash
docker build -t task3 .
docker run --rm task3
```

You should see:

```
E       Failed: DID NOT RAISE ValueError
```

### 3c. Make the tests pass (5 min)

In `refund.py`, raise a `ValueError` when the price or the delay is negative. In Python, raising an error looks like this:

```python
raise ValueError("a short message")
```

Where in the function should this check go? Build and run until every test says `PASSED`.
Look at the names pytest gives each row, for example `test_borders[59-0.0]`.

**Questions**

1. Why do we test 59 and 60, and not 30 and 90?
2. Why is an error better than quietly returning `0.0`?

### Commit

```bash
git add .
git commit -m "Task 3 done"
```

> **Task 3 done.** You tested like a tester: the borders, and the input nobody expects.

---

## Wrap-up

You practised three ways to test:

```
  Task 1   INSIDE THE FILE   >>> lines in a docstring       python -m doctest -v leap_year.py
  Task 2   SEPARATE FILE     def test_...(): assert ...     python -m pytest -v
  Task 3   BREAK IT          parametrize + pytest.raises    python -m pytest -v
```

| You write | It means |
|-----------|----------|
| `>>> f(x)` and the result under it, in a docstring | a test inside the file (doctest) |
| `def test_x(): assert ...` | a test in a separate file (pytest) |
| `@pytest.mark.parametrize` | one test, many cases |
| `with pytest.raises(ValueError):` | this code must raise an error |
| `docker run --rm NAME` | the same tests on every laptop |

**Remember three things:**

1. **Start from the rules, not from the code.** Write down what you expect before you look at how it is done.
2. **Be the tester, not the developer.** Look for the inputs that can break the code, not the ones that make it look good.
3. **Run the tests after every change.** Build, run, read. Later, let CI do it for you.

### Finished early? Try these

1. Run only some tests. What does `-k` do?

   ```bash
   docker run --rm task3 pytest -v -k borders
   ```

   (Plan B: `python -m pytest -v -k borders`)

2. **Be the bug:** in `task3-break-it/refund.py`, change `0.25` to `0.2`. Build and run. Which tests notice?
   Then undo it. (This is called *mutation testing*: it tests your tests.)

3. **Test first:** cancelled trains give the full price back. Write this test first, watch it fail, then add a
   `cancelled` parameter to `refund()`:

   ```python
   assert refund(80.0, 0, cancelled=True) == 80.0
   ```

### Where to go next

- Let CI (GitHub Actions) run `python -m pytest -v` on every push, like in the GitHub Actions tutorial.
- Find out what *test coverage* means, and which lines of `refund.py` your tests never run.

### Common problems

| Problem | Fix |
|---------|-----|
| `Cannot connect to the Docker daemon` | Start Docker (see the table in [Before you start](#before-you-start-8-min)) |
| Linux: `permission denied ... docker.sock` | `sudo usermod -aG docker $USER`, then log out and log in again |
| `NameError: name '____' is not defined` | You still have a blank `____` to fill in |
| The result does not change after you edit a file | Run `docker build` again: the image holds a copy of your code |
| Task 1: a test fails although the answer looks right | doctest compares **text**: write `True` / `False` exactly like Python prints them (not `true`). Check the indentation, too. |
| Plan B: strange import errors | Run the command inside the task folder, not in `sdo-testing-lab` |
| PowerShell: `running scripts is disabled` (Plan B) | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again |
| `git commit` asks "Please tell me who you are" | `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"` |
