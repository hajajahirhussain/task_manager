from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from jose import jwt, JWTError
from django.contrib.auth import get_user_model
User = get_user_model()

SECRET_KEY = "your_secret_key"  # use the same one from FastAPI
ALGORITHM = "HS256"

# def jwt_login_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         token = request.session.get('jwt_token')
#         if not token:
#             messages.error(request, "Please login first.")
#             return redirect(f"/login/?next={request.path}")

#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             # request.email = payload.get("sub")
#             request.username = payload.get("sub")
#         except JWTError:
#             messages.error(request, "Invalid or expired token.")
#             return redirect(f"/login/?next={request.path}")

#         return view_func(request, *args, **kwargs)

#     return wrapper


def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.session.get('jwt_token')
        if not token:
            messages.error(request, "Please login first.")
            return redirect(f"/login/?next={request.path}")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            user = User.objects.filter(username=username).first()
            if not user:
                # Auto-create user if not found
                user = User.objects.create_user(username=username, password="temp")
            request.username = username
            request.user = user  # 🔥 THIS IS THE FIX!
        except JWTError:
            messages.error(request, "Invalid or expired token.")
            return redirect(f"/login/?next={request.path}")

        return view_func(request, *args, **kwargs)
    return wrapper