from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

# create an author table with user and auction
# create an watchers table with user and auction

class Categories(models.Model):
    category = models.TextField(max_length=64)
    # auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, default='')

    def __str__(self):
        return f"{self.category}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    image_url = models.CharField(max_length=128, blank=True)
    category = models.ForeignKey(Categories,blank=True, default="1", on_delete=models.CASCADE)


    def __str__(self):
        return f"Auction {self.id}: {self.title}"

class Authors(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE)
    auction = models.OneToOneField(Auction, on_delete=CASCADE)

    def __str__(self):
        return f"ID: {self.id}, {self.author} {self.auction}"

class Watchers(models.Model):
    watcher = models.OneToOneField(User, on_delete=CASCADE)
    auction = models.OneToOneField(Auction, on_delete=CASCADE)

class Bid(models.Model):
    bid_price = models.IntegerField()
    auction = models.ForeignKey(Auction, on_delete=CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"Bid {self.id}"

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default="")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,default='')

