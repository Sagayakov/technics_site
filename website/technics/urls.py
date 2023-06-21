from django.urls import path

from . import views


urlpatterns = [
    path('', views.TechnicsView.as_view()),
    path('<slug:slug>/', views.TechnicDetailView.as_view(), name='technic_detail_url'),
    path('review/<int:pk>/', views.AddCommentsView.as_view(), name='add_comments_url'),

]
