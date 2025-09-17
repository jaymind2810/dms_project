from django.urls import path
from .views import FolderDetailView, FolderCreateView, DocumentUploadView, download_document, ajax_create_folder

app_name = 'documents'

urlpatterns = [
    path('', FolderDetailView.as_view(), name='root'),
    path('folder/<int:pk>/', FolderDetailView.as_view(), name='folder-detail'),
    path('folder/create/', FolderCreateView.as_view(), name='folder-create'),
    path('upload/', DocumentUploadView.as_view(), name='upload'),
    path('download/<int:pk>/', download_document, name='download'),
    path('ajax/create-folder/', ajax_create_folder, name='ajax-create-folder'),
]
