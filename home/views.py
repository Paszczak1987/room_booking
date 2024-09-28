from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from . import models
from . import forms


# Create your views here.

class RoomHomeView(TemplateView):
    template_name = 'room/home.html'

class RoomCreateView(CreateView):
    model = models.Room
    form_class = forms.RoomCreateForm
    template_name = 'room/new_room.html'
    success_url = reverse_lazy('home:room_list')

class RoomListView(ListView):
    model = models.Room
    template_name = 'room/list.html'
    context_object_name = 'rooms'
    
    def get_queryset(self):
        return models.Room.objects.prefetch_related('reservation_set').all()
    
    def get_context_data(self, **kwargs):
        # Dodaj dodatkowe informacje do kontekstu
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()  # Pobierz dzisiejszą datę
        # Sprawdź rezerwacje dla każdej sali
        for room in context['rooms']:
            room.has_reservation_today = room.reservation_set.filter(date=today).exists()
        return context
    

class RoomDetailView(DetailView):
    model = models.Room
    template_name = 'room/room_details.html'
    context_object_name = 'room'
    
    def get_queryset(self):
        return models.Room.objects.prefetch_related('reservation_set').all()
    
    def get_context_data(self, **kwargs):
        # Dodaj dodatkowe informacje do kontekstu
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()  # Pobierz dzisiejszą datę
        # Sprawdź rezerwacje na dziś
        context['reservations_today'] = self.object.reservation_set.filter(date=today)
        context['reservations_from_today'] = self.object.reservation_set.filter(date__gt=today)
        return context

class ReservationCreateView(CreateView):
    model = models.Reservation
    form_class = forms.ReservationCreateForm
    template_name = 'room/reservation.html'
    success_url = reverse_lazy('home:room_list')
    
    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(models.Room, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['reservations_today'] = self.room.reservation_set.filter(date=today)
        context['reservations_from_today'] = self.room.reservation_set.filter(date__gt=today)
        context['room'] = self.room
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.room
        return kwargs
    
    def form_valid(self, form):
        form.instance.room = self.room
        return super().form_valid(form)

    
    