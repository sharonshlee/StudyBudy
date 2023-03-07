from django.shortcuts import render
from .models import Room


# Create your views here.

rooms = [
    {'id': 1, 'name': "Let's learn python!"},
    {'id': 2, 'name': "Let's learn javascript!"},
    {'id': 3, 'name': "Let's learn html!"},
]
def home(request):
    # get, filter, exclude
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)