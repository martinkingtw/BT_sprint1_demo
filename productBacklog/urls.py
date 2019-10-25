from django.urls import path
from .views import PBListView, PBDetailView
from . import views

urlpatterns = [
    path('', PBListView.as_view(), name='productBacklog-home'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('about/', views.about, name='productBacklog-about'),
<<<<<<< HEAD
    path('delete/', views.delete, name='productBacklog-delete')
=======
    path('create/', views.create_pbi, name='productBacklog-create'),
>>>>>>> 78ce2f0c3681683c008b450dcb435cf8769f2a6d
]