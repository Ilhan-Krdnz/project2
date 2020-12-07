#from django import forms
from django.forms import ModelForm
from .models import Auctions, Comment, Bid

class AuctionForms(ModelForm):

    class Meta:
        model = Auctions
        exclude = ('user',)

class CommentForms(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user','auction')

class BidForms(ModelForm):

	class Meta:
		model = Bid
		exclude = ('user','auction')