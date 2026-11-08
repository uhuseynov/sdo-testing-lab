# SDO Testing Lab: find the bugs before your users do

Practice files for the Software Testing tutorial (Software Development and Operations, Constructor University).

You already know Git and Docker. Today you use them for one purpose: **running a program on purpose, with the
intent of finding errors**, before a user finds them.

You write tests in two places, and then you try to break the code:

```
  Task 3   BREAK IT          borders and bad input: try to make the code fail
  Task 2   SEPARATE FILE     the tests live in their own file test_refund.py
  Task 1   INSIDE THE FILE   the tests live in the docstring of the function
```

**The big idea of today:** a developer tests "gently". A tester tries to **break** the code. Today you are the tester.

| Task | Where do the tests live? | Tool |
|------|--------------------------|------|
| 1 | inside `leap_year.py` | `doctest` (built into Python) |
| 2 | in a separate file, `test_refund.py` | `pytest` |
| 3 | in a separate file, many cases at once | `pytest` |

**We do every task together.** I type on the big screen, you type the same on your laptop. Every step and every
line of code is also written here: if you can't see the screen or you fall behind, follow this README.

## Time plan (60 minutes, after the intro)

| Time | Step | Topic |
|------|------|-------|
| 0:00 | [Before you start](#before-you-start-8-min) | Check your setup, get the code |
| 0:08 | [Task 1](#task-1---tests-inside-the-file-12-min) | Tests inside the file |
| 0:20 | [Task 2](#task-2---tests-in-a-separate-file-17-min) | Tests in a separate file |
| 0:37 | [Task 3](#task-3---break-it-15-min) | Break it! |
| 0:52 | [Wrap-up](#wrap-up) | What you practised |

## What is in this repository

| File | What it is |
|------|------------|
| `task1-inside/leap_year.py` | A leap year check. The rule is at the top of the file, the tests live in the docstring. |
| `task2-separate/refund.py` | A train delay refund calculator. The rules are at the top of the file. |
| `task2-separate/test_refund.py` | The tests for `refund.py`, with blanks `____` for you to fill in. |
| `task3-break-it/refund.py` | The same calculator, with the Task 2 fixes and one new rule. |
| `task3-break-it/test_refund.py` | Border tests and bad-input tests, with blanks. |
| `*/Dockerfile` | Every task folder has one. It packs Python and runs the tests of that folder. |

The files start with the bugs and the blanks. During the tutorial we fill and fix them together.

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

Type the same things as on the big screen, step by step.

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

### 1c. Add a second test (3 min)

Quick question before you type: **is 1900 a leap year?** Guess first, then check it with the rule.

Add these two lines **right under `True`** and **above the closing `"""`**, with the same indentation as the
first test. Type them, or paste them at the very start of the line:

```python
    >>> is_leap_year(1900)
    False
```

Save the file (**Ctrl + S**), then build and run again. You should see:

```
Failed example:
    is_leap_year(1900)
Expected:
    False
Got:
    True
...
1 passed and 1 failed.
```

**Questions**

1. Which part of the rule does the code forget?
2. The first test (2024) passed, although the bug was already there. Why?

### 1d. Fix it, and test the fix (3 min)

Most people fix it like this. Change the last line of the function:

```python
    return year % 4 == 0 and year % 100 != 0
```

Save, build and run: `2 passed.` All green. Are we done?

Add one more test under the others: 2000 is divisible by 100, but also by 400.

```python
    >>> is_leap_year(2000)
    True
```

Save, build and run: `Expected: True`, `Got: False`. The new test caught a fix that was only half right.
Now the full rule:

```python
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

Save, build and run. You should see `3 passed.` and `Test passed.`

### Commit

```bash
git add .
git commit -m "Task 1 done"
```

> **Task 1 done.** Your tests live next to the code, and they also show how to use the function.

---

## Task 2 - Tests in a separate file (17 min)

```bash
cd ../task2-separate
```

### 2a. Read the rules, not the code (2 min)

A tester starts from the **rules** (the specification), not from the code. The rules are at the top of `refund.py`:

```
  * delay of at least  60 minutes -> 25 % of the ticket price back
  * delay of at least 120 minutes -> 50 % of the ticket price back
  * a refund below 4.00 euro is not paid out -> 0.0
```

Do **not** read the code of `refund()` yet!

### 2b. Run the tests with the blanks (2 min)

Open `test_refund.py`. The first test is complete, every other test has a blank `____`:

```python
from refund import refund


# Example - already done for you
def test_short_delay_gives_nothing():
    assert refund(80.0, 30) == 0.0
```

pytest finds every file whose name starts with `test_`, and every function in it that starts with `test_`.
`assert` is plain Python: if the comparison is false, the test fails. Run it once like this:

```bash
docker build -t task2 .
docker run --rm task2
```

The first build takes a bit longer (it installs pytest). You should see `5 failed, 1 passed`, and for each blank:

```
E       NameError: name '____' is not defined
```

A blank is not a value yet. Let's fill them.

### 2c. Fill in the blanks (5 min)

For every test, first work out from the rules what the refund **must** be. Then write it in:

```python
def test_delay_90_minutes():
    assert refund(80.0, 90) == 20.0


def test_delay_exactly_60_minutes():
    assert refund(80.0, 60) == 20.0


def test_delay_150_minutes():
    assert refund(80.0, 150) == 40.0


def test_small_refund_is_not_paid():
    assert refund(12.0, 90) == 0.0


# Your own test: a refund of exactly 4.00 euro IS paid out.
# Pick a ticket price and a delay that give exactly 4.00.
def test_exactly_4_euro_is_paid():
    assert refund(16.0, 90) == 4.0
```

| Test | Why |
|------|-----|
| 90 min | 90 ≥ 60, so 25 % of 80.00 € = 20.00 € |
| exactly 60 min | "at least 60" includes 60, so 20.00 € |
| 150 min | 150 ≥ 120, so 50 % of 80.00 € = 40.00 € |
| 12.00 €, 90 min | 25 % of 12.00 € = 3.00 €, below 4.00 €, so 0.00 € |
| 16.00 €, 90 min | 25 % of 16.00 € = exactly 4.00 €, so it is paid |

### 2d. Run again: the tests find bugs (2 min)

Save, build and run. You should see:

```
FAILED test_refund.py::test_delay_exactly_60_minutes - assert 0.0 == 20.0
FAILED test_refund.py::test_delay_150_minutes - assert 20.0 == 40.0
========================= 2 failed, 4 passed =========================
```

Read one failure. pytest shows both sides of the `==`, and even where the left value came from:

```
E       assert 0.0 == 20.0
E        +  where 0.0 = refund(80.0, 60)
```

Left: what the code returned. Right: what you expected.

**Questions**

1. Which delays made the tests fail? Why are exactly these values dangerous?
2. 4 tests passed although both bugs were in the code. Look at `test_delay_90_minutes`: it tests a delay, but it did
   not find the delay bugs. Why?

### 2e. Fix the two bugs (6 min)

Now open the code of `refund()` in `refund.py`.

**Bug 1:** the rule says "at least 60", but the code says "more than 60". Change

```python
    if delay_minutes > 60:
```

to

```python
    if delay_minutes >= 60:
```

Save, build and run: `1 failed, 5 passed`. 60 minutes works now, 150 minutes still fails.

**Bug 2:** 150 > 60 is already true, so the first `if` wins and the 50 % branch is never reached.
Check the bigger limit first:

```python
    if delay_minutes >= 120:
        amount = ticket_price * 0.50
    elif delay_minutes >= 60:
        amount = ticket_price * 0.25
    else:
        amount = 0.0
```

Save, build and run. You should see `6 passed`.

### Commit

```bash
git add .
git commit -m "Task 2 done"
```

> **Task 2 done.** The tests live in their own file, so they can grow without making the code longer.

---

## Task 3 - Break it! (15 min)

You are the independent tester now: think about the borders, and about input that "should never happen".

```bash
cd ../task3-break-it
```

`refund.py` here already has the Task 2 fixes, and one new rule:

```
  * a negative ticket price or delay is invalid -> raise ValueError
```

The code does **not** follow this rule yet.

### 3a. Run it once (1 min)

```bash
docker build -t task3 .
docker run --rm task3
```

You should see:

```
ERROR test_refund.py - NameError: name '____' is not defined
Interrupted: 1 error during collection
```

In Task 2 each test failed on its own. Here a blank sits in a table that Python reads while it loads the file,
so one blank stops the whole file.

### 3b. One test, many cases (4 min)

`test_borders` is **one** test function with a table of 4 rows. pytest runs it once per row. We test just below
and exactly at every limit. Fill in the 2 blanks:

```python
@pytest.mark.parametrize("delay, expected", [
    (59, 0.0),
    (60, 20.0),
    (119, 20.0),
    (120, 40.0),
])
def test_borders(delay, expected):
    assert refund(80.0, delay) == expected
```

### 3c. Bad input must fail (5 min)

What does `refund(-80.0, 90)` return right now? A negative price makes no sense, so the rule says: raise a
`ValueError`. The first bad-input test checks exactly this:

```python
def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        refund(-80.0, 90)
```

`pytest.raises(ValueError)` means: the code inside this block **must** raise a `ValueError`, otherwise the test fails.

Now the same kind of test for a **negative delay**. The `def` line is already there: replace only the line
`____  # write this test yourself` with the two lines below it, so that the whole function looks like this:

```python
def test_negative_delay_is_rejected():
    with pytest.raises(ValueError):
        refund(80.0, -30)
```

Save, build and run. You should see `2 failed, 4 passed` and twice:

```
E       Failed: DID NOT RAISE ValueError
```

The code did not refuse the bad input. It quietly returned `0.0`.

### 3d. Make the tests pass (5 min)

In `refund.py`, add these two lines at the **top** of `refund()`, right under the docstring:

```python
    if ticket_price < 0 or delay_minutes < 0:
        raise ValueError("negative input")
```

Save, build and run. You should see `6 passed`. Look at the names pytest gives each row:

```
test_refund.py::test_borders[59-0.0] PASSED
test_refund.py::test_borders[60-20.0] PASSED
test_refund.py::test_borders[119-20.0] PASSED
test_refund.py::test_borders[120-40.0] PASSED
test_refund.py::test_negative_price_is_rejected PASSED
test_refund.py::test_negative_delay_is_rejected PASSED
```

**Questions**

1. Why do we test 59 and 60, and not 30 and 90?
2. Why is an error better than quietly returning `0.0`?
3. Why does the check go at the top of the function?

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

### Play at home: the QA simulation

**[Your first day as a Junior QA Tester](https://uhuseynov.github.io/sdo-qa-simulation/)**: one release day in a
small QA workspace, about 10 minutes, works on your phone. You test a new build, report bugs to the developer,
check her fixes and tell the product manager if the release can go out at 17:00.

### More practice

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
| Task 3: `1 failed, 5 passed` instead of `2 failed, 4 passed` | The `def test_negative_delay_is_rejected():` line is there twice (a function inside a function). Keep only one. |
| The result does not change after you edit a file | Save the file (**Ctrl + S**) and run `docker build` again: the image holds a copy of your code. If the build shows `CACHED` on the `COPY` line, the file was not saved. |
| Task 1: `Expected:` shows extra spaces | You pasted into a line that was already indented. `>>>` and the expected result must start in the same column. |
| Task 1: `SyntaxError` | The test lines are below the closing `"""`. Move them inside the docstring. |
| Task 1: a test fails although the answer looks right | doctest compares **text**: write `True` / `False` exactly like Python prints them (not `true`). Check the indentation, too. |
| Plan B: strange import errors | Run the command inside the task folder, not in `sdo-testing-lab` |
| PowerShell: `running scripts is disabled` (Plan B) | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again |
| `git commit` asks "Please tell me who you are" | `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"` |
