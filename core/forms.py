from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, ProgramApplication, StudentProfile


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'interest', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Amina'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Mtui'}),
            'email': forms.EmailInput(attrs={'placeholder': 'amina@example.com'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us a bit about yourself and what brings you here...',
                'rows': 5,
            }),
        }


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Amina'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Mtui'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'amina@example.com'}))
    phone = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': '+255 XXX XXX XXX'}))
    age = forms.IntegerField(required=False, min_value=10, max_value=35, widget=forms.NumberInput(attrs={'placeholder': '18'}))
    location = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Arusha'}))
    school_or_organization = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'School, college, or organization'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone', 'age', 'location', 'school_or_organization', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                age=self.cleaned_data.get('age'),
                location=self.cleaned_data.get('location', ''),
                school_or_organization=self.cleaned_data.get('school_or_organization', ''),
            )
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ProgramApplicationForm(forms.ModelForm):
    class Meta:
        model = ProgramApplication
        fields = ['program', 'motivation']
        widgets = {
            'motivation': forms.Textarea(attrs={
                'placeholder': 'Tell us why you want to join this program and what you hope to learn...',
                'rows': 6,
            }),
        }
