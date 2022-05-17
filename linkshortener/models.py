from django.db import models
from .utils import generate_short_url

'''
    long_link - the original link
    short_link - new link
    followed_count - count the link has been opened
'''


class Link(models.Model):
    long_link = models.CharField(max_length=100)
    short_link = models.CharField(max_length=50, unique=True)
    followed_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.long_link + ' ' + 'to' + ' ' + self.short_link

    def save(self, *args, **kwargs):
        # If there are no short url in pass instance we call special method
        if not self.short_link:
            self.short_link = generate_short_url(self)

        super().save(*args, **kwargs)
