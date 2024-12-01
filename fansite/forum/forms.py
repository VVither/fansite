from django import forms
from .models import Announcement, Media
from django.core.exceptions import ValidationError


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'text', 'category', 'media']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is None:
            raise ValidationError({
                'text': 'Описание не может быть пустым'
            })
        if text is not None and len(text) < 20:
            raise ValidationError({
                'text': "Описание не может содержать менее 20 символов"
            })
        return cleaned_data


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media_file', 'media_type']
        widgets = {
            'media_type': forms.RadioSelect(),
        }

# class CategoryFilterForm(forms.Form):
#     category = forms.ChoiceField(choices=[('', 'Все категории')] + [(c, c) for c in Announcement.objects.values_list('category', flat=True).distinct()], required=False)