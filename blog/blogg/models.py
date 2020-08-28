from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
# excel workbook -> database
# worksheet -> table
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,default="")
    email=models.EmailField(default='')
    phone=models.IntegerField(max_length=12)
    content=models.TextField(max_length=100,default="")
    date=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return "Message from "+self.name+' '+self.email

class Blog(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=20,default="")
    content=models.TextField(default='')
    author=models.CharField(max_length=20)
    views=models.IntegerField(default=0)
    slug=models.CharField(max_length=50,default="")
    timestamp=models.DateTimeField(blank=True)
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)



    def __str__(self):
        return "Post from " + self.author + ' ' + self.title

class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField(default="")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    time=models.DateTimeField(default=now)
    def __str__(self):
        return self.user.username +" "+self.comment


