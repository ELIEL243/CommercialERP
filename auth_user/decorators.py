from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None
            check = False
            if request.user.groups.exists():
                groups = request.user.groups.all()
            for group in groups:
                if group.name in allowed_roles:
                    check = True
            if check is True:
                return view_func(request, *args, **kwargs)
            elif check is False:
                return HttpResponse("Permission non accordée !")
            return wrapper_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
