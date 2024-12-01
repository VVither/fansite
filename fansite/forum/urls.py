from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from .views import (AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView,
                    )

app_name = 'forum'

urlpatterns = [
    path('announcements/', AnnouncementListView.as_view(), name='AnnouncementList'),
    # path(),
    # path(),
    # path(),
    # path(),
]