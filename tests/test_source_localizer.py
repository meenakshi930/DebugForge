from pathlib import Path

from debugforge.failure import TestFailure
from debugforge.source_localizer import find_source_frame


def test_find_source_frame(tmp_path):
    source_file = tmp_path / "app.py"
    source_file.write_text(
        "def calculate_discount(price, discount):\n"
        "    return price / discount\n"
    )

    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="app.py:2: in calculate_discount\n",
        stderr=""
    )

    found = find_source_frame(
        result=result,
        workspace=tmp_path
    )

    assert found is not None
    assert found["file_path"] == "app.py"
    assert found["line_number"] == 2
    assert found["function_name"] == "calculate_discount"

def test_find_source_frame_ignores_test_file(tmp_path):
    test_file = tmp_path / "tests" / "test_app.py"
    source_file = tmp_path / "app.py"

    test_file.parent.mkdir()

    test_file.write_text(
        "def test_calculate_discount():\n"
        "    assert True\n"
    )

    source_file.write_text(
        "def calculate_discount(price, discount):\n"
        "    return price / discount\n"
    )

    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout=(
            "tests/test_app.py:5: in test_calculate_discount\n"
            "app.py:2: in calculate_discount\n"
        ),
        stderr=""
    )

    found = find_source_frame(
        result=result,
        workspace=tmp_path,
        test_file="tests/test_app.py"
    )

    assert found is not None
    assert found["file_path"] == "app.py"
    assert found["line_number"] == 2
    assert found["function_name"] == "calculate_discount"

def test_find_source_frame_from_module_import(tmp_path):
    test_file = tmp_path / "test_app.py"
    source_file = tmp_path / "app.py"

    test_file.write_text(
        "import app\n\n"
        "def test_calculate_discount():\n"
        "    assert app.calculate_discount(3500, 10) == 3150\n"
    )

    source_file.write_text(
        "def calculate_discount(price, discount):\n"
        "    return price / discount\n"
    )

    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="test_app.py:4: AssertionError\n",
        stderr=""
    )

    found = find_source_frame(
        result=result,
        workspace=tmp_path,
        test_file="test_app.py"
    )

    assert found is not None
    assert found["file_path"] == "app.py"
    assert found["function_name"] == "calculate_discount"