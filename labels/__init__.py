from .apis import AddLabel, DeleteLabel

label_routes = [
    (AddLabel, '/add/label'),
    (DeleteLabel, '/delete/label/<label>')
]