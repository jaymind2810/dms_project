from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.conf import settings

def document_upload_to(instance, filename):
    folder_part = f'folder_{instance.folder.id}' if instance.folder else 'root'
    return os.path.join('documents', folder_part, filename)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('parent', 'name')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_path(self):
        node = self
        parts = []
        while node:
            parts.insert(0, node.name)
            node = node.parent
        return '/' + '/'.join(parts)

class Document(models.Model):
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL, related_name='documents')
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to=document_upload_to)
    name = models.CharField(max_length=512, blank=True, null=True)
    size = models.BigIntegerField()
    content_type = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

