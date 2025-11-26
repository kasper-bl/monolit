import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model


class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})


from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Question(models.Model):
    question_text = models.CharField( verbose_name="название", max_length=200)
    description_short = models.CharField( max_length=300, verbose_name="Краткое описание", blank=True) 
    description_full = models.TextField(verbose_name="Полное описание", blank=True)  
    image = models.ImageField(upload_to='polls/images/', verbose_name="Изображение", blank=True, null=True) 
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    expires_at = models.DateTimeField( verbose_name= "Истекает в",  null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question_text

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
 
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')