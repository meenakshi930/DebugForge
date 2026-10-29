from debugforge.failure import TestFailure
from debugforge.pytest_parser import parse_failure


def test_parse_failure():
    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="""
        demo_target/tests/test_app.py::test_checkout_with_discount FAILED
        E       assert -3150 == 315.0
        """,
        stderr=""
    )

    evidence = parse_failure(result)

    assert evidence["status"] == "FAILED"
    assert evidence["test_name"] == "test_checkout_with_discount"
    assert evidence["actual"] == "-3150"
    assert evidence["expected"] == "315.0"