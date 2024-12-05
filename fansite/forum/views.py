from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, DetailView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from .models import Announcement, Media
from .forms import AnnouncementForm, MediaForm


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/announcement_list.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']
    paginate_by = 27

    def get_queryset(self):
        category = self.kwargs.get('category')
        queryset = Announcement.objects.all()
        if category:
            valid_categories = [c[0] for c in Announcement._meta.get_field('category').choices] #Получаем все валидные категории
            if category in valid_categories:
                queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcement_count'] = self.get_queryset().count()
        context['category'] = self.kwargs.get('category')
        context['year'] = timezone.now().year
        return context

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcement/announcement_detail.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        announcement = self.get_object()
        context['media'] = context['announcement'].media.all()
        context['category'] = announcement.category
        return context

    
class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement/announcement_create.html'
    success_url = reverse_lazy('announcement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_form'] = MediaForm() # Теперь это обычная форма, а не formset
        return context

def post(self, request, *args, **kwargs):
        self.object = None
        announcement_form = self.get_form()

        if announcement_form.is_valid():
            announcement = announcement_form.save()
            for file in request.FILES.getlist('media_file'):  #Обработка списка файлов
                media = Media(media_file=file, media_type=request.POST.get('media_type')) #Выбор типа файла из request.POST
                media.save()
                announcement.media.add(media) #Добавление к объявлению
            return super().form_valid(announcement_form)
        else:
            return self.render_to_response(self.get_context_data(form=announcement_form))