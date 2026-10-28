from demo_target.app import checkout


def test_checkout_with_discount():
    result = checkout([100, 200, 50], 10)

    assert result == 315.0