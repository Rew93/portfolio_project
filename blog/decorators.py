from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from blog.models import BlogModel, CommentsModel


# def user_not_author(function=None, redirect_url='blog'):
#     '''
#
#     :param function:
#     :param redirect_url:
#     :return:
#     '''
#
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 return redirect(redirect_url)
#
#             return view_func(request, *args, **kwargs)
#
#         return _wrapped_view
#
#     if function:
#         return decorator(function)
#
#     return decorator
def verify_author(func):
    def check_and_call(request, *args, **kwargs):
        slug = kwargs["slug"]
        instance = get_object_or_404(BlogModel, slug=slug)
        if request.user == instance.author:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return check_and_call


def verify_author_comment(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs['comment_id']
        instance = get_object_or_404(CommentsModel, id=id)
        if request.user == instance.author:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return check_and_call
