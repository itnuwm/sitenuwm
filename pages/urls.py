from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('edit/<int:pk>/', views.edit_view, name='edit_url'),
    path('add/<int:pk>/', views.add_view, name='add_url'),
    path('delete/<int:pk>/', views.delete_view, name='delete_url'),
]
