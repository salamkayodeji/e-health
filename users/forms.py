from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserProfile

PARTICULARS = (
('DOCTOR', 'DOCTOR'),
('PATIENT', 'PATIENT'),
)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(widget = forms.HiddenInput(), required=False)
    category = forms.CharField(
        max_length=30,
        widget=forms.Select(choices=PARTICULARS),
    )
    class Meta:
        model = UserProfile
        fields = ('email', 'full_name', 'phone', 'is_staff', 'category', 'password')
        
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.category = self.cleaned_data["category"]
        if user.category == 'DOCTOR':    
            user.is_staff = True
        else:
            user.is_staff = False            
        print(user.category)
        print(user.is_staff)
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'full_name', 'phone', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
