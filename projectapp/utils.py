from datetime import datetime
from datetime import datetime, timedelta
from barbers.models import Availability, BarberProfile
from .models import Appointment, Service
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def combine_date_time(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def generate_time_slots(barber, service, date):
    slots = []
    
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    weekday = date_obj.weekday()
    
    availability = Availability.objects.filter(barber=barber, day_of_week=weekday).first()
    if not availability:
        return 0
    start_time = availability.start_time
    end_time = availability.end_time
    
    start_datetime = datetime.combine(date_obj, start_time)
    end_datetime = datetime.combine(date_obj, end_time)
    
    duration = service.duration
    current = start_datetime
    
    while current + timedelta(minutes=duration) <= end_datetime:
        slots.append(current)
        current += timedelta(minutes=duration)
    
    booked = Appointment.objects.filter(
        barber=barber, 
        appointment_time__date=date_obj
        ).values_list("appointment_time", flat=True)

    available_slots = [slot for slot in slots if slot not in booked]
    return available_slots

def calculate_extra_fee(booking_type):
    if booking_type == "home":
        return 12
    return 0


def SearchBarbers(queryset, query):
    if query:
        allservices = Service.objects.filter(name__icontains=query)
    
        queryset  = BarberProfile.objects.filter(
            Q(services__in=allservices) |
            Q(full_name__icontains=query)|
            Q(address__icontains=query)|
            Q(shop_name__icontains=query)
        ).distinct()
        
    return queryset

def paginateBarbers(request, barbers, results):
    page = request.GET.get("page")
    paginator = Paginator(barbers, results)
    
    try:
        barbers = paginator.get_page(page)
    
    except PageNotAnInteger:
        page = 1
        barbers = paginator.get_page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        barbers = paginator.get_page(page)
    
    page = barbers.number
    leftIndex = page  - 4
    
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = page + 5
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, barbers