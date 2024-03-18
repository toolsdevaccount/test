from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

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