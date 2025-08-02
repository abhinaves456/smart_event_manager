from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from .models import Event, Ticket, UserProfile

# The main dashboard view
@login_required
def dashboard_view(request):
    if hasattr(request.user, 'userprofile') and request.user.userprofile.is_admin:
        events = Event.objects.all().order_by('-date')
        tickets = Ticket.objects.all()
    else:
        events = Event.objects.all().order_by('-date')
        tickets = Ticket.objects.filter(user=request.user)
    
    # Get a list of event IDs the current user has booked
    booked_event_ids = tickets.values_list('event_id', flat=True)
        
    return render(request, 'eventapp/dashboard.html', {
        'events': events, 
        'tickets': tickets,
        'booked_event_ids': booked_event_ids
    })

# The user signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'eventapp/signup.html', {'form': form})

# The user logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# NEW VIEW: To handle booking a ticket for an event
@login_required
def book_ticket_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Check if the user already has a ticket
    if Ticket.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, f"You already have a ticket for {event.title}.")
    else:
        Ticket.objects.create(event=event, user=request.user)
        messages.success(request, f"Successfully booked your ticket for {event.title}!")
    return redirect('dashboard')