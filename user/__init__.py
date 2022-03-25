from .apis import Registration, Login, LogOut, Activate

user_routes = [
    (Registration, '/registration'),
    (Login, '/login'),
    (LogOut, '/logout'),
    (Activate, '/activate'),
]
