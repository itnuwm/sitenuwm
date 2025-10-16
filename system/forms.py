from django import forms
from django.contrib.auth.models import Group, User


class LoginForm(forms.Form):
	username = forms.CharField(
		label = 'Логін',
		widget = forms.TextInput(
			attrs = {
				'class' : 'form-control',
				'placeholder' : ''}))
	password = forms.CharField(
		label = 'Пароль',
		widget = forms.PasswordInput(
			attrs = {
				'class' : 'form-control',
				'placeholder' : ''}))


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Exclude default perms
        default_prefixes = ['add_', 'change_', 'delete_', 'view_']
        self.fields['permissions'].queryset = self.fields['permissions'].queryset.exclude(
            codename__regex=r'^(' + '|'.join(default_prefixes) + ').*'
        )

        # 👇 Clean display: show only the permission name
        # self.fields['permissions'].label_from_instance = lambda obj: obj.name


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Exclude default perms
        default_prefixes = ['add_', 'change_', 'delete_', 'view_']
        self.fields['user_permissions'].queryset = self.fields['user_permissions'].queryset.exclude(
            codename__regex=r'^(' + '|'.join(default_prefixes) + ').*'
        )

        # 👇 Clean display: show only the permission name
        # self.fields['user_permissions'].label_from_instance = lambda obj: obj.name

