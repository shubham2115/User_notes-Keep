class NoteNotExist(Exception):
    def __init__(self, note, message="Note not Exists"):
        self.note = note
        self.message = message
        super().__init__(self.message)

