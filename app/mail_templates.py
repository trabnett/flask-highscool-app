from app import app

def template1(user, code):
    x = f"<div style='background-color:blue;opacity:.7;color:white;height:25px;'>TRHS</div><br><p>Hello {user.first_name}. You have forgotten your password.</p><br><p>Please click the link below to reset your password:</p><br><a href='http://127.0.0.1:5000/reset_password/{code}'>Reset Password</a>"
    print('hello', user.first_name, code, x)
    return x
