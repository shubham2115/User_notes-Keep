from .apis import AddNote, NotesOperation, Home, NoteLabel, GetByLabel, PinNote,GetPinNote

notes_routes = [
    (AddNote, '/notes'),
    (NotesOperation, '/notes/<id>'),
    (Home, '/'),
    (NoteLabel, '/label/<id>'),
    (GetByLabel, '/getbylabel/<label>'),
    (PinNote, '/pin/<id>'),
    (GetPinNote,'/pinnote')

]
