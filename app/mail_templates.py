from app import app

def template1(user, code):
    content = f"<div style='background-color:blue;opacity:.7;color:white;height:25px;'>TRHS</div><br><p>Hello {user.first_name}. You have forgotten your password.</p><br><p>Please click the link below to reset your password:</p><br><a href='https://trhs.herokuapp.com/reset_password/{code}'>Reset Password</a>"
    return content
