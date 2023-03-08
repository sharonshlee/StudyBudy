from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.

def home(request):
    # get, filter, exclude
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # "topic__name" --> query upwards to the parent
    # "icontains" --> topic name at least contains the value in q
    # "contains" == case sensitive, icontains == case insensitive
    # can use startswith, endswith
    # if q is '', all topics will be matched without filter
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )

    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    """create room using room form with fields: host, topic, name, description"""
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    """Update room details"""
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # instance=room to prefill

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room) # instance=room to tell which room
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    """Delete a room"""
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})