from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . constants import GENDER_TYPE
from django import forms
from . models import UserAccount



class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget = forms.DateInput(attrs = {'type': 'date'}))
    gender = forms.ChoiceField(choices = GENDER_TYPE)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'gender','birth_date']

    def save(self, commit =True):
        cur_user = super().save(commit = False)
        if commit == True:
            cur_user.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
         
            UserAccount.objects.create(
                user = cur_user,
                birth_date = birth_date,
                gender = gender,
                account_no = 100000 + cur_user.id
            )

        return cur_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })




