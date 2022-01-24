from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')



from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


from django.views.generic.edit import CreateView
class AddProduct(PermissionRequiredMixin, CreateView):
    permission_required = ('shop.add_product',)