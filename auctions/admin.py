from django.contrib import admin
from .models import User,Auctions,Comment

admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Comment)
