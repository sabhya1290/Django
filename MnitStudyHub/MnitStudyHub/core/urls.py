
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from django_browser_reload.urls import browser_reload

urlpatterns = [

    path('', views.BrowseResources, name='BrowseResources'),
    path('<slug:slug>/', views.category_resources, name='category_resources'),

    # path("__reload__/", include("django_browser_reload.urls")),
]
