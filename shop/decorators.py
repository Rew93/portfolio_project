from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from shop.models import ReviewModel


def verify_author_review(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs['comment_id']
        instance = get_object_or_404(ReviewModel, id=id)
        if request.user == instance.author:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return check_and_call
