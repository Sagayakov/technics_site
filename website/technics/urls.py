from django.urls import path

from . import views


urlpatterns = [
    path('', views.TechnicsView.as_view()),
    path('filter/', views.FilterTechView.as_view(), name='filter_url'),
    path('search/', views.Search.as_view(), name='search'),
    path('<slug:slug>/', views.TechnicDetailView.as_view(), name='technic_detail_url'),
    path('review/<int:pk>/', views.AddCommentsView.as_view(), name='add_comments_url'),
    path('like/<int:pk>/', views.post_rating, name='add_ratings_url'),
]
