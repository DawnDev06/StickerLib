import os
import uuid

class Sticker:
    def __init__(self, original_path):
        self.id = str(uuid.uuid4())
        self.original_path = original_path
        self.filename = os.path.basename(original_path)
        self.processed_path = None
        self.is_processed = False
        self.error = None

    def __repr__(self):
        return f"<Sticker {self.filename} (Processed: {self.is_processed})>"