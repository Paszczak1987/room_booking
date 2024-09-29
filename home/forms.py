from django import forms
from django.utils import timezone
from . import models

class BaseRoomForm(forms.ModelForm):
    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is None:
            raise forms.ValidationError("Ilość miejsc jest wymagana.")
        if capacity <= 10:
            raise forms.ValidationError("Ilość miejsc musi być większa niż 10.")
        if capacity > 200:
            raise forms.ValidationError("Ilość miejsc nie może być większa niż 200.")
        return capacity
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Nazwa pokoju jest wymagana.")
        if len(name) < 3:
            raise forms.ValidationError("Nazwa pokoju musi zawierać przynajmniej 3 znaki.")
        if not name.isalnum():
            raise forms.ValidationError("Nazwa pokoju musi być alfanumeryczna (bez znaków specjalnych).")
        return name


class RoomCreateForm(BaseRoomForm):
    class Meta:
        model = models.Room
        fields = ['name', 'capacity', 'projector']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nazwa sali'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Ilość miejsc'}),
            'projector': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nazwa sali"
        self.fields['capacity'].label = "Ilość miejsc"
        self.fields['projector'].label = "Czy w sali jest projektor"

class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = ['date', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        room = kwargs.pop('room', None)
        self.room = room.pk
        super(ReservationCreateForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = "Data rezerwacji"
        self.fields['comment'].label = "Notatka"
        
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Nie można zarezerwować sali wstecznie.")
        if models.Reservation.objects.filter(room=self.room, date=date).exists():
            raise forms.ValidationError("Ta sala jest już zarezerwowana na wybrany dzień.")
        return date


class RoomEditForm(BaseRoomForm):
    class Meta:
        model = models.Room
        fields = ['name', 'capacity', 'projector']
        widgets = {
            'projector': forms.CheckboxInput(),
        }
        
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)
        if self.room:
            self.fields['name'].widget.attrs['placeholder'] = self.room.name
            self.fields['capacity'].widget.attrs['placeholder'] = str(self.room.capacity)
