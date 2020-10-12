from django.shortcuts import render, redirect, HttpResponse
from .models import Schedules
from django.contrib.auth.models import User
from .forms import UserForm, LogForm
from django.contrib import messages
import bcrypt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Email Imports:
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Calendar imports #
# from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
# from django.views import generic
# from calendar import HTMLCalendar
from .utils import Calendar

from datetime import date, time, datetime, timedelta
import datetime
import time
from calendar import HTMLCalendar
import calendar


def index(request):
    context = {
        'reg_form': UserForm(),
        'log_form': LogForm(),
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == "POST":
        b_form = UserForm(request.POST)
        if len(b_form.errors) > 0:
            for key, value in b_form.errors.items():
                messages.error(request, value)
            return redirect('/')
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=make_password(request.POST['password1']), username=request.POST['email'])
        return redirect('/home')
    return redirect('/')

def log(request):
    if request.method == "POST":
        user_log = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user_log != None:
            login(request, user_log)
            return redirect('/home')
    messages.error(request, "Incorrect Login")
    return redirect('/')

@login_required(login_url='/')
def home(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    # d = datetime.date.today()
    # cal = calendar.HTMLCalendar(firstweekday=0)
    # cal = calendar.month(year, month)
    # d = datetime.date.today().day
    # print(month, "x"*10)

##########  New Calendar Section
    def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()

    # d = get_date(self.request.GET.get('month', None))
    cal = Calendar(year, month)
    html_cal = cal.formatmonth(withyear=True)

##########
    context = {
        "date_list": Schedules.objects.all(),
        "today": datetime.date.today(),
        # "cal": cal.formatmonth(year, month),
        # "cal": cal,
        'calendar': mark_safe(html_cal),
        'month': month,
        
    }
    return render(request, 'home.html', context)

def prev_month(request, id):
    pass
    # d = datetime.date.today().day
    # first = d.replace(day=1)
    # prev_month = first - timedelta(days=1)
    # month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    # return month

def next_month(request):
    pass
    # d = datetime.date.today().day
    # days_in_month = calendar.monthrange(d.year, d.month)[1]
    # last = d.replace(day=days_in_month)
    # next_month = last + timedelta(days=1)
    # month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    # return month


def log_out(request):
    logout(request)
    return redirect('/')

def add_date(request):
    if request.method == "POST":
        errors =  Schedules.objects.schedule_val(request.POST)
        if  len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/home')
        Schedules.objects.create(date=request.POST['date'],time=request.POST['time_list'], description=request.POST['desc'], scheduler=request.user)

        context = {
            "date_list": Schedules.objects.all(),
            "today": datetime.date.today(),
        }
        return render(request, 'a_list.html', context)
        #####
        # return redirect('/home')
    return redirect('/home')

def remove_date(request, id):
    delete_date = Schedules.objects.get(id=id)
    delete_date.delete()
    context = {
        "date_list": Schedules.objects.all(),
        "today": datetime.date.today(),
    }
    return render(request, 'a_list.html', context)
    # return redirect('/home')

@login_required(login_url='/')
def edit_page(request, id):
    date = Schedules.objects.get(id=id)
    date.time = str(date.time)
    context = {
        "date": date,
    }
    return render(request, 'edit.html', context)

def edit_date(request, id):
    if request.method == "POST":
        errors =  Schedules.objects.schedule_val(request.POST)
        if  len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f'/edit/{id}')
        schedule_date = Schedules.objects.get(id=id)
        schedule_date.date = request.POST['date']
        schedule_date.time = request.POST['time_list']
        schedule_date.description = request.POST['desc']
        schedule_date.save()        
        return redirect('/home')
    return redirect(f'/edit/{id}')

def confirm_page(request, id):
    context = {
        "schedule": Schedules.objects.get(id=id)
    }
    return render(request, 'confirmation.html', context)

def confirm(request, id):
    sendemail = request.GET.getlist('email_check')
    if len(sendemail) > 0:
        context = {
            "schedule": Schedules.objects.get(id=id),
            "user": User.objects.get(username=request.user),
        }

        html_message = render_to_string('mail_template.html', context)
        plain_message = strip_tags(html_message)

        print(plain_message)
        send_mail(
            'Appoinment Reminder',
            plain_message,
            'f7adc01b02-d98d6b@inbox.mailtrap.io',
            [sendemail],
            html_message = html_message,
            fail_silently=False,
        )
    
    schedule = Schedules.objects.get(id=id)
    schedule.confirm = True
    schedule.save()
    return redirect('/home')

def un_confirm(request, id):
    schedule = Schedules.objects.get(id=id)
    schedule.confirm = False
    schedule.save() 
    return redirect('/home')