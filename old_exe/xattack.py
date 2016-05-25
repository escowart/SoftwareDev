import json
import sys
from evo_json.convert_py_json.convert_situation import convert_from_py_situation

def main():
    process_json_situation(sys.stdin, sys.stdout)


def process_json_situation(file_in, file_out) -> None:
    py_json_sit = json.load(file_in)

    try:
        # Convert PyJSON Situation -> Situation
        situation = convert_from_py_situation(py_json_sit)
    except Exception as e:
        # Error forming the Situation => Invalid input Situation
        return

    is_attackable = situation.is_defender_attackable()
    json.dump(is_attackable, file_out)


if __name__ == "__main__":
    main()
