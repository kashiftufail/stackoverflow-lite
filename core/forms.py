from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: customize built-in fields too
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

