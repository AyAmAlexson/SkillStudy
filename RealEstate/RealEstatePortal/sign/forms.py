
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        agents_res_group = Group.objects.get(name='common')
        agents_res_group.user_set.add(user)
        return user