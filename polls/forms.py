from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Question
from django.forms import inlineformset_factory
from .models import Question, Choice

User = get_user_model()


from django import forms
from django.forms import inlineformset_factory
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'description_short', 'description_full', 'image', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice, 
    fields=['choice_text'], 
    extra=3,
    can_delete=True  
)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.avatar = self.cleaned_data["avatar"]
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']