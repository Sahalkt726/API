from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    slug=models.SlugField(max_length=250,unique=True)
    published=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Article,self).save(*args,**kwargs)



