from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:search_type>/<str:main>/<str:sub1>/<str:sub2>/<str:sub3>/', views.search, name='search'),
    # path('<str:search_type>/<str:main>/<str:sub1>/<str:sub2>/', views.search, name='search'),
    # path('<str:search_type>/<str:main>/<str:sub1>/', views.search, name='search'),
    # path('<str:search_type>/<str:main>/', views.search, name='search'),
    # path('<str:search_type>/', views.search, name='search'),
    path('human/<str:gene_name>/', views.search, name='search'),
    path('human/', views.search, name='search'),
    path('', views.search, name='search'),
    # path('SearchType/pathways&main=<str:main>&sub1=<str:sub1>&sub2=<str:sub2>&sub3=<str:sub3>&geneName=<str:gene_name>', views.search_by_pathway, name='search_by_pathway'),
]