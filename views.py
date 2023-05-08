from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

# fileupload
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# index
def index(request):
    return render(request, 'crud/index.html', {})

# fileupload
def uploadtest(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'crud/upload/uploadtest.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'crud/upload/uploadtest.html')