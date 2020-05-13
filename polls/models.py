from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

class Question(models.Model):
    objects = models.Manager()
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    def __str__(self):
        return self.question_text

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    

class Choice(models.Model):
    objects = models.Manager()
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
