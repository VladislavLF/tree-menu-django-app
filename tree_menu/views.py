from django.shortcuts import render

def index(request):
    return render(request, 'tree_menu/index.html')

def about(request):
    return render(request, 'tree_menu/about.html')

def contact(request):
    return render(request, 'tree_menu/contact.html')