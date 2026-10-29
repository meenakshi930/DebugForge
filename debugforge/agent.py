from .ai_agent import ask_model
from .repair_parser import parse_repair_response
from .patch_response import PatchResponse


def generate_repair(prompt: str) -> PatchResponse:
    response = ask_model(prompt)

    return parse_repair_response(response)