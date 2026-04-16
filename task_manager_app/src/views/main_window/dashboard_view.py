import sqlite3
from datetime import date, datetime


def _parse_deadline(deadline: str):
    """Parse app deadline format (MM/DD/YYYY) into a date."""
    if not deadline:
        return None
    try:
        return datetime.strptime(deadline, "%m/%d/%Y").date()
    except (TypeError, ValueError):
        return None


def update_dashboard(self):
    try:
        tasks = self.controller.load_tasks()

        if "stat_total_tasks" in self.ids:
            self.ids.stat_total_tasks.text = str(len(tasks))

        today = date.today()
        due_today = []

        for t in tasks:
            d = _parse_deadline(getattr(t, "deadline", None))
            if d == today:
                due_today.append(t)

        if "stat_due_today_header" in self.ids:
            if due_today:
                self.ids.stat_due_today_header.text = f"{len(due_today)} due today"
            else:
                self.ids.stat_due_today_header.text = "No tasks due today"

        # Progress bars fill using completion ratios from task status.
        if "progress_today" in self.ids:
            if due_today:
                done_today = sum(1 for t in due_today if getattr(t, "done", False))
                self.ids.progress_today.value = (done_today / len(due_today)) * 100
            else:
                self.ids.progress_today.value = 0

        if "progress_week" in self.ids:
            if tasks:
                done_total = sum(1 for t in tasks if getattr(t, "done", False))
                self.ids.progress_week.value = (done_total / len(tasks)) * 100
            else:
                self.ids.progress_week.value = 0

    except (sqlite3.Error, AttributeError, KeyError, TypeError, ValueError) as e:
        self.show_error(f"Dashboard update failed: {e}")
