from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from .views import (AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView,
                    MyAnnouncementView, AnnouncementUpdateView, AnnoucementDeleteView)

app_name = 'forum'

urlpatterns = [
    path('announcements/', AnnouncementListView.as_view(), name='AnnouncementList'),
    path('announcements/<int:pk>', AnnouncementDetailView.as_view(), name = "AnnouncementDetail"),
    path('announcements/create', AnnouncementCreateView.as_view(), name="AnnouncementCreate"),
    path('announcements/Myannouncements', MyAnnouncementView.as_view(), name='My_announcement'),
    path('announcements/<int:pk>/update', AnnouncementUpdateView.as_view(), name='AnnouncementUpdate'),
    path('announcements/<int:pk>/delete',AnnoucementDeleteView.as_view(), name='AnnoucementDelete'),
    #path('',, name='My_response'),
]