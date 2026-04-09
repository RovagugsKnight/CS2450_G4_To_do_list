from kivymd.uix.pickers import MDDatePicker


class DeadlineSelector:
    """
    Calendar-based deadline selector.
    Calls the provided callback with a formatted date string (MM/DD/YYYY).
    """

    def __init__(self, callback):
        """
        callback: function that receives the formatted date string.
        """
        self.callback = callback

    def open(self):
        picker = MDDatePicker()
        picker.bind(on_save=self._on_save)
        picker.open()

    def _on_save(self, instance, value, date_range):
        # value is a datetime.date
        date_str = value.strftime("%m/%d/%Y")
        self.callback(date_str)
