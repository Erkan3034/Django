from django.shortcuts import render , HttpResponse

# Create your views here.

def index(request):
    context = {
        "number1": 10,
        "number2": 20,
        "number3": 30,
    }
    return render(request, 'index.html' , context) # Bu kod, index.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, ana sayfayı temsil eder

def about(request):
    return render(request, 'about.html') # Bu kod, articles.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, makaleler sayfasını temsil eder


def detail(request, id):
    return HttpResponse(f"Bu id'ye sahip yazı: {id}")

def create(request):
    return HttpResponse("Yazı Oluştur")

