import os


def find_root() -> str:
    result = os.path.abspath(os.path.dirname(__file__))
    while result != "/":
        result = os.path.abspath(os.path.dirname(result))
        if os.path.exists(os.path.join(result, "setup.py")):
            return result
    return None
