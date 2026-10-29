from debugforge.patch_response import (
    PatchResponse,
    create_patch_response
)


def test_create_patch_response():

    response = create_patch_response(
        diagnosis="Addition uses subtraction.",
        file_path="app.py",
        old_code="return a - b",
        new_code="return a + b"
    )

    assert isinstance(response, PatchResponse)
    assert response.diagnosis == "Addition uses subtraction."
    assert response.file_path == "app.py"
    assert response.old_code == "return a - b"
    assert response.new_code == "return a + b"