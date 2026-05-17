from django.shortcuts import render

#home views 
def home(request) : 
    return render(request, 'home.html')