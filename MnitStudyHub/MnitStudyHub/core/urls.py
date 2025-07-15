
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from django_browser_reload.urls import browser_reload

urlpatterns = [

    path('', views.BrowseResources, name='BrowseResources'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('your_notes/', views.YourNotes, name='your_notes'),
    path('your_notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('bookmark/', views.bookmark, name='bookmark'),
    path('bookmark/delete/<int:pdf_id>/', views.delete_bookmark, name='delete_bookmark'),
    path('pdf/<path:path>/', views.pdf_view, name='pdf_view'),
    path('<slug:slug>/', views.category_resources, name='category_resources'),
    path('bookmark/<int:pdf_id>/', views.toggle_bookmark, name='toggle_bookmark'),

]
