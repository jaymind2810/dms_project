from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import FileResponse, JsonResponse
from .models import Folder, Document
from .forms import FolderForm, DocumentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os, mimetypes



class FolderDetailView(ListView):
    model = Document
    template_name = 'documents/folder_detail.html'
    context_object_name = 'documents'
    paginate_by = 20

    def get_folder(self):
        folder_id = self.kwargs.get('pk')
        if folder_id:
            return get_object_or_404(Folder, pk=folder_id)
        return None

    def get_queryset(self):
        folder = self.get_folder()
        if folder:
            return Document.objects.filter(folder=folder)
        return Document.objects.filter(folder__isnull=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        folder = self.get_folder()
        ctx['folder'] = folder
        ctx['children'] = folder.children.all() if folder else Folder.objects.filter(parent__isnull=True)
        ctx['folder_form'] = FolderForm(initial={'parent': folder})
        ctx['upload_form'] = DocumentForm(initial={'folder': folder})
        return ctx


class FolderCreateView(CreateView):
    model = Folder
    form_class = FolderForm
    success_url = reverse_lazy('documents:root')
    template_name = 'documents/folder_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DocumentUploadView(FormView):
    form_class = DocumentForm
    template_name = 'documents/folder_detail.html'  # optional
    success_url = '/documents/'  # fallback

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            uploaded_file = form.cleaned_data['file']
            doc.name = uploaded_file
            doc.size = uploaded_file.size
            doc.content_type = getattr(uploaded_file, 'content_type', '')
            doc.save()
            folder = doc.folder
            if folder:
                return redirect('documents:folder-detail', pk=folder.id)
            return redirect('documents:root')
        return redirect('documents:root')

def download_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    file_path = doc.file.path
    if os.path.exists(file_path):
        mime, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{doc.name}"'
        if mime:
            response['Content-Type'] = mime
        return response
    return JsonResponse({'error': 'File not found'}, status=404)

def ajax_create_folder(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        print("name : ", name)
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        parent_id = request.POST.get('parent')
        parent = None
        if parent_id:
            parent = get_object_or_404(Folder, pk=parent_id)

        if Folder.objects.filter(name=name, parent=parent).exists():
            return JsonResponse({'error': 'Folder already exists'}, status=400)

        folder = Folder.objects.create(
            name=name,
            parent=parent,
            created_by=None
        )

        return JsonResponse({
            'created': True,
            'id': folder.id,
            'name': folder.name,
            'path': folder.get_path()
        })

 