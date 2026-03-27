from typing import Any

class Result:
    """result of a conroller function to send to views"""
    def __init__(self, success: bool, error: str | None = None, return_val: Any = None):
        self.success = success
        self.error = error
        self.return_val = return_val
