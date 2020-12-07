from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Auctions(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    first_date = models.DateTimeField(auto_now=True)
    starting_price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE,related_name='comments', null=True, blank=True)
    comment_text = models.CharField(max_length=100)

    def __str__(self):
        return self.comment_text

