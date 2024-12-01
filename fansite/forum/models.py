from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Media(models.Model):
    media_file = models.FileField(upload_to='announcement_media/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'webm'])])
    media_type = models.CharField(max_length=50, choices=[('image', 'Изображение'), ('video', 'Видео')], default='image')
        
    def __str__(self):
        return f"Media {self.media_file.name}"
    
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement")
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('tank', 'Танки'), ('healer', 'Хилы'), ('dd', 'ДД'), ('trader', 'Торговцы'),
        ('guildmaster', 'Гилдмастеры'), ('questgiver', 'Квестгиверы'), ('blacksmith', 'Кузнецы'),
        ('leatherworker', 'Кожевники'), ('alchemist', 'Зельевары'), ('spellmaster', 'Мастера заклинаний')
    ])
    media = models.ManyToManyField(Media, related_name='announcements', blank=True)
    status = models.CharField(max_length=20, choices=[('open', 'Открыто'), ('closed', 'Закрыто'), ('archived', 'Архивировано')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses_sent')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user} to {self.announcement.title}"
    
class NewsletterSubscruber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='newsletter_subscriptions')
    is_subscribed = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Subscription for {self.user.username}"
