class Task:
    def __init__(self, task_id:int, task_name:str, text, done=False):
        self.task_name = task_name
        self.task_id = task_id
        self.text = text
        self.done = done