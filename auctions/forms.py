#from django import forms
from django.forms import ModelForm
from .models import Auctions, Comment

class AuctionForms(ModelForm):

    class Meta:
        model = Auctions
        exclude = ('user',)

class CommentForms(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user','auction')