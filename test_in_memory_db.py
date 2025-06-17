import subprocess
import sys

TEST_INPUT = """
GET A
SET A 10
GET A
COUNTS 10
SET B 20
SET C 10
COUNTS 10
UNSET B
GET B
BEGIN
SET A 20
BEGIN
SET A 30
GET A
ROLLBACK
GET A
COMMIT
GET A
FIND 10
FIND 20
FIND 30
# --- Дополнительные тесты ---
SET X 100
BEGIN
SET X 200
BEGIN
UNSET X
GET X
ROLLBACK
GET X
COMMIT
GET X
# Проверка ROLLBACK без транзакции
ROLLBACK
# Проверка COMMIT без транзакции
COMMIT
# Проверка UNSET без SET
UNSET Z
GET Z
END
"""

EXPECTED_OUTPUT = [
    "NULL",
    "10",
    "1",
    "2",
    "NULL",
    "30",
    "20",
    "20",
    "A",
    "A",
    "NULL",
    "NULL",  # GET X after UNSET in nested BEGIN
    "200",   # GET X after ROLLBACK
    "200",   # GET X after COMMIT
    "NO TRANSACTION",  # ROLLBACK without BEGIN
    "NO TRANSACTION",  # COMMIT without BEGIN
    "NULL"  # GET Z after UNSET (never set)
]

def run_test():
    proc = subprocess.Popen(
        [sys.executable, "in_memory_db_console.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(TEST_INPUT)

    output_lines = [line.strip() for line in stdout.split("\n") if line.strip() and not line.startswith(" > ")]
    passed = True

    for expected, actual in zip(EXPECTED_OUTPUT, output_lines):
        if expected != actual:
            print(f"FAIL: expected '{expected}' but got '{actual}'")
            passed = False

    if passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")

if __name__ == '__main__':
    run_test()
