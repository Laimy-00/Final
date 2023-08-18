from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):  # user model
    username = models.CharField(max_length=20, unique=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = PhoneNumberField()
    is_staff = models.BooleanField(default=False)  # if true -> this is not customer, this is crew member
    position = models.ForeignKey('main_app.Position', on_delete=models.DO_NOTHING, null=True)
    schedule = models.ForeignKey('main_app.Schedule', on_delete=models.DO_NOTHING, null=True)
    card_number = models.CharField(max_length=16, null=True)  # physical discount card

    def __str__(self):
        return self.username


class Order(models.Model):  # order model
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dishes = models.ManyToManyField('main_app.Dish')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class Dish(models.Model):  # dish model
    CATEGORIES_CHOICES = (
        ('starter', 'Starter'),
        ('main', 'Main'),
        ('side', 'Side'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    )

    name = models.CharField(max_length=100, unique=True)
    ingredients = models.ManyToManyField('main_app.Ingredient')
    category = models.CharField(max_length=20, choices=CATEGORIES_CHOICES, default='main')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='dishes', blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):  # ingredient model
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Reservation(models.Model):  # reservation model
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('finished', 'Finished'),
    )

    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}"


class Table(models.Model):  # table model
    number = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)  # not used yet

    def __str__(self):
        return f"{self.number}"


class Position(models.Model):  # position model
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Schedule(models.Model):  # schedule model
    DAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    TIME_CHOICES = (
        ('00:00', '00:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    )

    starting_day = models.CharField(max_length=20, choices=DAY_CHOICES, default='monday')
    starting_time = models.CharField(max_length=5, choices=TIME_CHOICES, default='08:00')
    ending_time = models.CharField(max_length=5, choices=TIME_CHOICES, default='17:00')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title
