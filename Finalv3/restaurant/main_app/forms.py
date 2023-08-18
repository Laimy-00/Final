from django import forms
from .models import Reservation, Table, CustomUser, News
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm


class ReservationForm(forms.ModelForm):  # form for reservation editing by customer
    class Meta:
        model = Reservation
        fields = ['table', 'additional_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_tables = self.get_available_tables()
        table_choices = [(table.id, f"Table {table.number} (Capacity: {table.capacity})") for table in available_tables]
        self.fields['table'].choices = table_choices

    def get_available_tables(self):  # checking available tables (date and time can`t be changed, new reservation needed)
        three_hours_before_booking = self.instance.booking_time - timezone.timedelta(hours=3)
        three_hours_after_booking = self.instance.booking_time + timezone.timedelta(hours=3)

        occupied_tables = Reservation.objects.filter(
            booking_time__range=(three_hours_before_booking, three_hours_after_booking),
            status__in=['pending', 'confirmed']
        ).exclude(id=self.instance.id).values_list('table_id', flat=True)

        return Table.objects.filter(is_available=True).exclude(id__in=occupied_tables)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['f_name', 'l_name', 'email', 'phone', 'card_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:  # to delete password reset field from this form
            del self.fields['password']
        self.fields['card_number'].required = False


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
