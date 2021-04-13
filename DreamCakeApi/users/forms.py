from allauth.account.forms import LoginForm
from django import forms

class CLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(CLoginForm, self).__init__(*args, **kwargs)
		print(f'TEST:\n{self.fields["login"].widget.attrs}')
		login = self.fields["login"]
		login.label = 'Usuario'
		widget = login.widget.attrs

		widget['placeholder'] = 'Nombre de usuario'
		widget['ref'] = '{this.input}'
		# self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'yourclass'})
		# self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'yourclass'})