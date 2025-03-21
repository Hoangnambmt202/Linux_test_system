from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Trả về template home.html
