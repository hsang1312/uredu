from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Users


class UserCreationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('email',)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('email',)


