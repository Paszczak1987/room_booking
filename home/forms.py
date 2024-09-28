from django import forms
from . import models

class RoomCreateForm(forms.ModelForm):
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
        if models.Room.objects.filter(name=name).exists():
            raise forms.ValidationError("Sala o tej nazwie już istnieje.")
        return name
    
    