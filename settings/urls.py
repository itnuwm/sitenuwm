"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from system import views as system
from pages import views as pages

urlpatterns = [
    path('', system.home_view, name='home_url'),
    path('login/', system.login_view, name='login_url'),
    path('logout/', system.logout_view, name='logout_url'),
    path('app/', system.app_view, name='app_url'),
    path('policy/', system.privacy_policy_view, name='privacy_policy_url'),
    
    path('page/', include('pages.urls', namespace='page')),
    path('adminka/', include('adminka.urls', namespace='adminka')),
    path('news/', include('blog.urls', namespace='news')),
    path('admin/', admin.site.urls),    

    path('<slug:slug>/', pages.layer_1_view),
    path('<slug:slug1>/<slug:slug2>/', pages.layer_2_view),
    path('<slug:slug1>/<slug:slug2>/<slug:slug3>/', pages.layer_3_view),
    path('<slug:slug1>/<slug:slug2>/<slug:slug3>/<slug:slug4>/', pages.layer_4_view),
    path('<slug:slug1>/<slug:slug2>/<slug:slug3>/<slug:slug4>/<slug:slug5>/', pages.layer_5_view),
    path('<slug:slug1>/<slug:slug2>/<slug:slug3>/<slug:slug4>/<slug:slug5>/<slug:slug6>/', pages.layer_6_view),
    path('<slug:slug1>/<slug:slug2>/<slug:slug3>/<slug:slug4>/<slug:slug5>/<slug:slug6>/<slug:slug7>/', pages.layer_7_view),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)