from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, 
                                  DetailView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin, 
                                        UserPassesTestMixin)
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from .models import Announcement, Media, Response
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
    template_name = 'announcement/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_form'] = MediaForm() # Теперь это обычная форма, а не formset
        return context

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.user = self.request.user  # Важно! Установите пользователя
        announcement.save()
        media_form = MediaForm(self.request.POST, self.request.FILES)
        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.save()
            announcement.media.add(media)
        return super().form_valid(form)
        
class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement/announcement_form.html'  # один шаблон для создания и редактирования
    success_url = reverse_lazy('announcement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'media_form' not in context:
          try:
            context['media_form'] = MediaForm(instance=self.get_object().media.first())
          except:
            context['media_form'] = MediaForm()
        return context

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.user = self.request.user # Важно! Установите пользователя
        announcement.save()
        media_form = MediaForm(self.request.POST, self.request.FILES, instance=self.get_object().media.first())
        if media_form.is_valid():
            media_form.save()
        return super().form_valid(form)
    
class MyAnnouncementView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcement/my_announcements.html'
    context_object_name = 'my_announcements'

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user).order_by('-created_at')

class MyResponse(ListView):
    model = Response
    template_name = 'response/response_list.html'
    context_object_name = 'My_Response'

    def get_queryset(self):
        return Response.objects.filter(user=self.request.user).order_by('-created_at')

class AnnoucementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcement/announcement_delete.html'
    success_url = reverse_lazy('forum:AnnouncementList')

    def test_func(self):
        Announcement = self.get_object()
        return self.request.user == Announcement.user or self.request.user.is_staff
    
