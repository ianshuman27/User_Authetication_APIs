from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title=models.CharField(max_length=255)
    content=models.CharField(max_length=255)
    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='article')

    def __str__(self):
         return self.title
    
class Composer(models.Model):
     name=models.CharField(max_length=255)
     category=models.ForeignKey(Article, on_delete=models.CASCADE,related_name='com')
    

     def __str__(self):
          return self.name