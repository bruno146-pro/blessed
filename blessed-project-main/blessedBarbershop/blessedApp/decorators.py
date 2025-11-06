from django.shortcuts import redirect

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            rol = request.session.get('rol')
            if rol not in roles_permitidos:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator