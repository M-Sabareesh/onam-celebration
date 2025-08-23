from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Games app coming soon!")

app_name = 'games'

urlpatterns = [
    path('', placeholder_view, name='home'),
]
