from django import forms
from .models import Cinema, Movie, Seat, Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('customer_name', 'customer_email')