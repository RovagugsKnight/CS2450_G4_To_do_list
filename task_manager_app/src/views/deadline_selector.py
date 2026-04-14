# views/deadline_selector.py
from kivy.logger import Logger
from kivy.uix.widget import Widget

# Use the import you confirmed works
from kivymd.uix.pickers import MDDatePicker

class DeadlineSelector(Widget):
    """
    Wrapper that opens an MDDatePicker and calls the provided callback
    with a single string argument in format MM/DD/YYYY when the user confirms.
    """

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        Logger.info("DeadlineSelector: created with callback %s", repr(callback))

    def open(self):
        """
        Open the MDDatePicker. Try to bind on_save/on_cancel; fallback if API differs.
        """
        try:
            picker = MDDatePicker()
            try:
                picker.bind(on_save=self._on_save, on_cancel=self._on_cancel)
                Logger.info("DeadlineSelector: bound on_save/on_cancel handlers")
            except Exception:
                try:
                    # Some older variants accept a callback kwarg
                    picker = MDDatePicker(callback=self._on_save)
                    Logger.info("DeadlineSelector: constructed MDDatePicker with callback kwarg")
                except Exception:
                    Logger.warning("DeadlineSelector: could not bind on_save; opening picker without explicit binding")
            picker.open()
            Logger.info("DeadlineSelector: MDDatePicker opened")
        except Exception as e:
            Logger.exception("DeadlineSelector: failed to open MDDatePicker: %s", e)
            raise

    def _on_save(self, instance, value, date_range=None):
        """
        Handler for MDDatePicker save. Coerce value to MM/DD/YYYY string when possible.
        """
        try:
            try:
                date_str = value.strftime("%m/%d/%Y")
            except Exception:
                date_str = str(value)
            Logger.info("DeadlineSelector: on_save fired with %s", date_str)
        except Exception as e:
            Logger.exception("DeadlineSelector: error formatting date value: %s", e)
            date_str = str(value)

        try:
            if callable(self.callback):
                try:
                    self.callback(date_str)
                    Logger.info("DeadlineSelector: callback invoked successfully")
                except Exception as cb_e:
                    Logger.exception("DeadlineSelector: callback raised an exception: %s", cb_e)
        except Exception as e:
            Logger.exception("DeadlineSelector: unexpected error invoking callback: %s", e)

    def _on_cancel(self, *args):
        Logger.info("DeadlineSelector: user cancelled date picker")
