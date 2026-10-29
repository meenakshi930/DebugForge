from debugforge.source_context import extract_function


def test_extract_function():
    source = """
def calculate_discount(total, discount):
    percentage = discount / 100
    return total - (total * percentage)


def add(a, b):
    return a + b
"""

    result = extract_function(
        source_code=source,
        function_name="calculate_discount"
    )

    assert result is not None
    assert "def calculate_discount" in result
    assert "percentage = discount / 100" in result
    assert "def add" not in result

def test_extract_method():
    source = """
class Calculator:

    def calculate_discount(self, total, discount):
        percentage = discount / 100
        return total - (total * percentage)

    def add(self, a, b):
        return a + b
"""

    result = extract_function(
        source_code=source,
        function_name="calculate_discount"
    )

    assert result is not None
    assert "def calculate_discount" in result
    assert "percentage = discount / 100" in result
    assert "def add" not in result