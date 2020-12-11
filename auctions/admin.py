from django.contrib import admin
from .models import User,Auctions,Comment,Bid,Watchlist

admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
