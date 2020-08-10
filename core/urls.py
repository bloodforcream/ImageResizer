from django.urls import path

from core.views import HomePageView, AddImageView, ImageDetailView


urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('images/add/', AddImageView.as_view(), name='add-image-page'),
    path('images/<slug:slug>/', ImageDetailView.as_view(), name='image-detail-page'),
]
