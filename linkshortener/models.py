from django.db import models

'''
    long_link - the original link
    short_link - new link
    followed_count - count the link has been opened
'''


class Link(models.Model):
    long_link = models.CharField(max_length=50)
    short_link = models.CharField(max_length=50, unique=True)
    followed_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.long_link + 'to' + self.short_link
