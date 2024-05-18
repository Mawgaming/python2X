import sys
import pdb

class DebuggingTool:
    def __init__(self):
        self.original_excepthook = sys.excepthook

    def __enter__(self):
        sys.excepthook = self.excepthook

    def __exit__(self, exc_type, exc_value, traceback):
        sys.excepthook = self.original_excepthook

    def excepthook(self, exc_type, exc_value, traceback):
        print(f"Exception: {exc_value}")
        pdb.post_mortem(traceback)

