from django.contrib import admin

from .models import Comment, Auction, User, Bid, Authors, Watchers, Watchlist, Categories

# Register your models here.
admin.site.register(Comment)
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Authors)
admin.site.register(Watchers)
admin.site.register(Watchlist)
admin.site.register(Categories)