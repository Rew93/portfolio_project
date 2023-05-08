from django.shortcuts import HttpResponseRedirect, reverse


def user_not_authenticated(function=None, redirect=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse(redirect))
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
