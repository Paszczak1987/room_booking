from django.views.generic import CreateView, TemplateView

from . import models
from . import forms


# Create your views here.

class RoomHomeView(TemplateView):
    template_name = 'room/home.html'

class RoomCreateView(CreateView):
    model = models.Room
    form_class = forms.RoomCreateForm
    template_name = 'room/new_room.html'

    