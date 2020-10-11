from calendar import HTMLCalendar
from datetime import date

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day):
		# events_per_day = events.filter(start_time__day=day)
		d = ''
		# for event in events_per_day:
		# 	d += f'<li> {event.title} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		# events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="cal">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week)}\n'
		return cal

# https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html