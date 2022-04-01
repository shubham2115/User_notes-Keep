from .apis import AddNote, NotesOperation, Home ,NoteLabel,GetByLabel
notes_routes = [
    (AddNote, '/notes'),
    (NotesOperation, '/notes/<id>'),
    (Home, '/'),
    (NoteLabel, '/label/<id>'),
    (GetByLabel, '/getbylabel/<label>'),

]