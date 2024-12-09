from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from .views import (AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView,
                    )

app_name = 'forum'

urlpatterns = [
    path('announcements/', AnnouncementListView.as_view(), name='AnnouncementList'),
    path('announcements/<int:pk>', AnnouncementDetailView.as_view, name = "AnnouncementDetail"),
    path('announcements/<int:pk>/create', AnnouncementCreateView.as_view, name="AnnouncementCreate"),
    path('', name='My_announcement'),
    path('', name='My_response'),
]