from django.shortcuts import render , HttpResponse

# Create your views here.

def index(request):
    return render(request, 'article/index.html') # Bu kod, index.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, ana sayfayı temsil eder