from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from profiles.models import Profile


def is_admin():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return view_function(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return redirect('accounts:login')

        return wrap

    return decorator


def is_user():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_email_verified:
                    if Profile.objects.filter(user__email=request.user).exists():
                        return view_function(request, *args, **kwargs)
                    else:
                        return redirect('my_profile:profile_create')
                else:
                    return redirect('accounts:verify_email')
            else:
                return redirect('accounts:login')

        return wrap

    return decorator


def is_admin_or_user():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return view_function(request, *args, **kwargs)
                else:
                    if request.user.is_email_verified:
                        if Profile.objects.filter(user__email=request.user).exists():
                            return view_function(request, *args, **kwargs)
                        else:
                            return redirect('my_profile:profile_create')
                    else:
                        return redirect('accounts:verify_email')
            else:
                return redirect('accounts:login')

        return wrap

    return decorator
