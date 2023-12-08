from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .views import ScrapDataAPIReddit, ScrapDataAPIYoutube

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search-youtube/', ScrapDataAPIYoutube.as_view(), name='search_results_youtube'),
    path('search-reddit/', ScrapDataAPIReddit.as_view(), name='search_results_reddit'),
    path('reddit-topics/', ScrapDataAPIReddit.as_view(), name='reddit-topic-list'),
    path('youtube-videos/', ScrapDataAPIYoutube.as_view(), name='youtube-video-list'),
    path('', RedirectView.as_view(url=reverse_lazy('youtube-video-list'), permanent=True), name='scrapper-dashboard')
]
