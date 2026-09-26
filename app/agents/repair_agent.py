from pathlib import Path


def repair_calculator(target_file: Path) -> str:
    source = target_file.read_text()

    broken = "return a - b"
    fixed = "return a + b"

    if broken not in source:
        raise RuntimeError("Expected broken implementation was not found.")

    target_file.write_text(source.replace(broken, fixed))

    return "Changed add() from subtraction to addition."
