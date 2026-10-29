from debugforge.localizer import read_file, read_file_with_lines


def test_read_file():
    content = read_file("demo_target/app.py")

    assert "def checkout" in content


def test_read_file_with_lines():
    lines = read_file_with_lines("demo_target/app.py")

    assert any("def checkout" in line for line in lines)
    assert any("apply_discount" in line for line in lines)