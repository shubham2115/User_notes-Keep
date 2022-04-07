from .apis import Registration, Login, LogOut, Activate, ChangePassword

user_routes = [
    (Registration, '/registration'),
    (Login, '/login'),
    (LogOut, '/logout'),
    (Activate, '/activate'),
    (ChangePassword, '/changepass')
]
