from dataclasses import dataclass


@dataclass
class PatchResponse:
    diagnosis: str
    file_path: str
    old_code: str
    new_code: str


def create_patch_response(
    diagnosis: str,
    file_path: str,
    old_code: str,
    new_code: str
) -> PatchResponse:

    return PatchResponse(
        diagnosis=diagnosis,
        file_path=file_path,
        old_code=old_code,
        new_code=new_code
    )