from .apis import AddNote, NotesOperation, Home
notes_routes = [
    (AddNote, '/addnotes'),
    (NotesOperation, '/notes/<topic>'),
    (Home, '/')
]