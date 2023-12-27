from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
            for group in groups:
                if group.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponse("Permission non accordée !")
        return wrapper_func

    return decorator
