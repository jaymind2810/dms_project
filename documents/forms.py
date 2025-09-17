from django import forms
from .models import Folder, Document

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['folder', 'file', 'name', 'description']
