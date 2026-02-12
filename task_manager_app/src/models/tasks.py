class Task:
    def __init__(self, task_id, text, done=False):
        self.id = task_id
        self.text = text
        self.done = done