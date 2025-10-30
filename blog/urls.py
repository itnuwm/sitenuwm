from django.urls import path
from blog import views as news

app_name = 'blog'

urlpatterns = [
	path('', news.post_list, name='post_list'),
	path('<slug:slug>/', news.post_detail, name='post_detail'),
]

