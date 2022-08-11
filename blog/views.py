from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
def home(request):
    context = {
        'posts': 123
    }
    return render(request, 'blog/home.html', context)
