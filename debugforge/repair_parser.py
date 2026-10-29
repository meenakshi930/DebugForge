from .patch_response import PatchResponse


SECTIONS = [
    "DIAGNOSIS:",
    "FILE:",
    "OLD_CODE:",
    "NEW_CODE:"
]


def parse_repair_response(response: str) -> PatchResponse:

    sections = {}

    current_section = None

    for line in response.splitlines():

        stripped_line = line.strip()

        if stripped_line in SECTIONS:
            current_section = stripped_line[:-1]
            sections[current_section] = ""
            continue

        if current_section is not None:

            if sections[current_section]:
                sections[current_section] += "\n"

            sections[current_section] += line

    for section in [
        "DIAGNOSIS",
        "FILE",
        "OLD_CODE",
        "NEW_CODE"
    ]:
        if section not in sections or not sections[section].strip():
            raise ValueError(
                f"Missing section: {section}"
            )

    return PatchResponse(
        diagnosis=sections["DIAGNOSIS"].strip(),
        file_path=sections["FILE"].strip(),
        old_code=sections["OLD_CODE"].strip(),
        new_code=sections["NEW_CODE"].strip()
    )