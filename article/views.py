from django.shortcuts import render , HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html') # Bu kod, index.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, ana sayfayı temsil eder

def about(request):
    return render(request, 'about.html') # Bu kod, articles.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, makaleler sayfasını temsil eder


