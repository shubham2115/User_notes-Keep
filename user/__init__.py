from .apis import Registration, Login, LogOut, Activate, ChangePassword,ForgotPassword

user_routes = [
    (Registration, '/registration'),
    (Login, '/login'),
    (LogOut, '/logout'),
    (Activate, '/activate'),
    (ChangePassword, '/changepass'),
    (ForgotPassword,'/forgotpass')
]
