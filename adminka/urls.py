from django.urls import path
from . import views as adminka

app_name = 'adminka'

urlpatterns = [
    path('search/', adminka.search_view, name='search_url'),
    path('home/edit/', adminka.home_edit_view, name='home_edit_url'),
    path('user/list/', adminka.user_list_view, name='user_list_url'),
    path('sidebar/toggle/<int:pk>/', adminka.sidebar_toggle_view, name='sidebar_toggle_url'),

    path('add/', adminka.add_view, name='add_url'),
    path('edit/<int:pk>/', adminka.edit_view, name='edit_url'),
    path('delete/<int:pk>/', adminka.delete_view, name='delete_url'),

    path('slug/edit/<int:pk>/', adminka.slug_edit_view, name='slug_edit_url'),
    path('design/edit/<int:pk>/', adminka.design_edit_view, name='design_edit_url'),
    path('admin/edit/<int:pk>/', adminka.admin_edit_view, name='admin_edit_url'),
    path('export/pages/xlsx/', adminka.export_pages_view, name='export_pages_url'),
    # path('delete/<int:pk>/', adminka.delete_view, name='delete_url'),

    # Admin pages
    path('', adminka.adminka_0_view),
    path('<str:slug>/', adminka.adminka_1_view),
    path('<str:slug1>/<str:slug2>/', adminka.adminka_2_view),
    path('<str:slug1>/<str:slug2>/<str:slug3>/', adminka.adminka_3_view),
    path('<str:slug1>/<str:slug2>/<str:slug3>/<str:slug4>/', adminka.adminka_4_view),
    path('<str:slug1>/<str:slug2>/<str:slug3>/<str:slug4>/<str:slug5>/', adminka.adminka_5_view),
    path('<str:slug1>/<str:slug2>/<str:slug3>/<str:slug4>/<str:slug5>/<str:slug6>/', adminka.adminka_6_view),
    path('<str:slug1>/<str:slug2>/<str:slug3>/<str:slug4>/<str:slug5>/<str:slug6>/<str:slug7>/', adminka.adminka_7_view),
]