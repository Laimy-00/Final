from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .forms import ReservationForm, CustomUserChangeForm, NewsForm
from .models import CustomUser, Reservation, Order, Dish, News


def index(request):  # main page
    news = News.objects.all().order_by('-pub_date')
    context = {
        'news': news
    }
    return render(request, 'index.html', context=context)


def gallery(request):  # gallery page
    return render(request, 'gallery.html')


def dishes(request):  # page with dishes
    paginator = Paginator(Dish.objects.all(), 6)
    page_number = request.GET.get('page')
    all_dishes = paginator.get_page(page_number)
    context = {
        'dishes': all_dishes
    }
    return render(request, 'dishes.html', context=context)


def contact(request):  # page with contacts
    return render(request, 'contact.html')


def about(request):  # page with info about restaurant
    return render(request, 'about.html')


def privacy(request):  # page with info about restaurant
    return render(request, 'privacy.html')


@csrf_protect
def register(request):  # new users registration page
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                password_validation.validate_password(password)
            except password_validation.ValidationError as e:
                messages.error(request, ', '.join(e.messages))
                return redirect('register')
            if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
                messages.error(request, f'User with username {username} or email {email} already exists!')
                return redirect('register')
            CustomUser.objects.create_user(username=username, email=email, password=password)
            messages.info(request, f'User {username} successfully created!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords not match!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def account(request):  # account page (for users and for crew there are two different pages)
    current_user = request.user
    if current_user.is_staff:
        if current_user.position_id:
            position = current_user.position
            schedule = current_user.schedule
            return render(request, 'staff.html', {'position': position, 'schedule': schedule})
        else:
            return render(request, 'staff.html')
    else:
        active_reservations = Reservation.objects.filter(customer_id=current_user).exclude(
            Q(status='cancelled') | Q(status='finished'))
        return render(request, 'account.html', {'reservations': active_reservations})


@login_required
def create_reservation(request):  # new reservation request. First creating date and time only.
    if request.method == "POST":  # After redirecting to reservation editing page.
        booking_time_str = request.POST['booking_time']
        booking_time = datetime.strptime(booking_time_str, '%Y-%m-%dT%H:%M')
        customer = request.user
        now = timezone.localtime(timezone.now())
        try:
            if booking_time.date() <= (now + timedelta(days=1)).date():  # checking is date and time correct
                raise ValidationError(
                    "Booking must be made for tomorrow or later.")  # (from tomorrow from 15:00 to 20:00)
            if booking_time.time() < now.replace(hour=15, minute=0, second=0, microsecond=0).time() \
                    or booking_time.time() > now.replace(hour=20, minute=0, second=0, microsecond=0).time():
                raise ValidationError("Booking time must be between 15:00 and 20:00.")

            new_reservation = Reservation.objects.create(
                customer_id=customer,
                booking_time=booking_time,
            )
            reservation_id = new_reservation.id
            return redirect('edit_reservation', reservation_id=reservation_id)
        except ValidationError as e:
            return render(request, 'create_reservation.html', {'error_message': e.message})

    return render(request, 'create_reservation.html')


@login_required
def edit_reservation(request, reservation_id):  # Reservation editing page
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ReservationForm(instance=reservation)

    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'edit_reservation.html', context)


@login_required
def cancel_reservation(request, reservation_id):  # Reservation canceling page
    reservation = get_object_or_404(Reservation, id=reservation_id, customer_id=request.user)
    reservation.status = 'cancelled'
    reservation.save()
    return redirect('account')


@login_required
def cancelled_reservation(request):  # List of canceled reservations of current user
    current_user = request.user
    cancelled_reservations = Reservation.objects.filter(customer_id=current_user, status='cancelled')
    return render(request, 'cancelled_reservation.html', {'reservations': cancelled_reservations})


@login_required
def finished_reservations(request):  # List of finished reservations of current user
    current_user = request.user
    fin_reservations = Reservation.objects.filter(customer_id=current_user, status='finished')
    return render(request, 'finished_reservations.html', {'reservations': fin_reservations})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)


@login_required
def reservations(request):  # page for reviewing/editing pending and confirmed reservations by managers and chiefs
    current_user = request.user
    name = current_user.position.name
    if name != 'Manager' and name != 'Chief':
        return redirect('account')
    active_reservations = Reservation.objects.exclude(Q(status='cancelled') | Q(status='finished'))  # Q objects for logic or
    return render(request, 'reservations.html', {'reservations': active_reservations})


@login_required
def unactive_reservations(request):
    current_user = request.user
    name = current_user.position.name
    if name != 'Manager' and name != 'Chief':
        return redirect('account')
    not_active_reservations = Reservation.objects.exclude(Q(status='pending') | Q(status='confirmed'))  # Q objects for logic or
    return render(request, 'reservations.html', {'reservations': not_active_reservations})


@login_required
def staff_list(request):  # page for reviewing/editing restaurant crew by managers and chiefs
    current_user = request.user
    name = current_user.position.name
    if name != 'Manager' and name != 'Chief':
        return redirect('account')
    all_crew = CustomUser.objects.filter(is_staff=True)
    return render(request, 'staff_list.html', {'staff_list': all_crew})


@login_required
def create_news(request):
    current_user = request.user
    name = current_user.position.name
    if name != 'Manager' and name != 'Chief':
        return redirect('account')
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewsForm()

    context = {
        'form': form
    }
    return render(request, 'create_news.html', context)


@login_required
def orders(request):
    my_orders = Order.objects.filter(customer_id=request.user)
    context = {
        'orders': my_orders
    }
    return render(request, 'orders.html', context)
