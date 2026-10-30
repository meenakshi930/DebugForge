def validate_patch(
    source_code: str,
    old_code: str,
    new_code: str
) -> dict:

    if not old_code.strip():
        return {
            "valid": False,
            "reason": "OLD_CODE is empty"
        }

    if not new_code.strip():
        return {
            "valid": False,
            "reason": "NEW_CODE is empty"
        }

    occurrences = source_code.count(old_code)

    if occurrences == 0:
        return {
            "valid": False,
            "reason": "OLD_CODE was not found in source"
        }

    if occurrences > 1:
        return {
            "valid": False,
            "reason": "OLD_CODE matches multiple locations"
        }

    if old_code == new_code:
        return {
            "valid": False,
            "reason": "OLD_CODE and NEW_CODE are identical"
        }

    return {
        "valid": True,
        "reason": "Patch is valid"
    }