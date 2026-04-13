from datetime import date, datetime


def update_dashboard(self):
    try:
        tasks = self.controller.load_tasks()

        if "stat_total_tasks" in self.ids:
            self.ids.stat_total_tasks.text = str(len(tasks))

        today = date.today()
        due_today = []

        for t in tasks:
            if getattr(t, "deadline", None):
                try:
                    d = datetime.strptime(t.deadline, "%m/%d/%Y").date()
                    if d == today:
                        due_today.append(t)
                except Exception:
                    pass

        if "stat_due_today_header" in self.ids:
            if due_today:
                self.ids.stat_due_today_header.text = f"{len(due_today)} due today"
            else:
                self.ids.stat_due_today_header.text = "No tasks due today"

    except Exception as e:
        self.show_error(f"Dashboard update failed: {e}")
