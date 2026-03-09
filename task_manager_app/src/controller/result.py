class Result:
    """result of a conroller function to send to views"""
    def __init__(self, success: bool, error: str | None = None, task_id: int | None = None):
        self.success = success
        self.error = error
        self.task_id = task_id
