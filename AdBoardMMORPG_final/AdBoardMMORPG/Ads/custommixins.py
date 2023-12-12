from django.contrib.auth.mixins import AccessMixin
from django.http import Http404


class UserIsOwnerMixin(AccessMixin):
    """
    Mixin, который разрешает просмотр DetailView только для создавшего объект пользователя.
    """

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Проверяем, что объект имеет атрибут "created_by" и он совпадает с текущим пользователем.
        if hasattr(obj, 'author') and obj.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied.")
