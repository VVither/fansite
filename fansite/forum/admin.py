from django.contrib import admin
from .models import Media, Announcement, Response, NewsletterSubscruber

admin.site.register(Media)
admin.site.register(Announcement)
admin.site.register(Response)
admin.site.register(NewsletterSubscruber)

