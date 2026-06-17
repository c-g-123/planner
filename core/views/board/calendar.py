from calendar import Calendar, DECEMBER, JANUARY, month_name, SUNDAY
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import Item

CALENDAR_TEMPLATE_PATH = "core/board/calendar/calendar.html"
MONTH_TEMPLATE_PATH = "core/board/calendar/month.html"

MINIMUM_ALLOWED_YEAR = 1
MAXIMUM_ALLOWED_YEAR = 9999

FIRST_WEEKDAY = SUNDAY

@require_GET
@login_required
def calendar_view(request):
    context = {
        "current_month": _get_current_month_context(),
    }

    return render(
        request,
        CALENDAR_TEMPLATE_PATH,
        context,
    )

@require_GET
@login_required
def month_view(request, year, month):
    _validate_year(year)
    _validate_month(month)

    month_context = _get_month_context(request.user, year, month)
    previous_month_context = _get_previous_month_context(year, month)
    next_month_context = _get_next_month_context(year, month)
    context = {
        "month": month_context,
        "previous_month": previous_month_context,
        "next_month": next_month_context,
        "current_month": _get_current_month_context()
    }

    return render(
        request,
        MONTH_TEMPLATE_PATH,
        context,
    )

def _validate_year(year):
    if year < MINIMUM_ALLOWED_YEAR or year > MAXIMUM_ALLOWED_YEAR:
        raise Http404()

def _validate_month(month):
    if month < JANUARY or month > DECEMBER:
        raise Http404()

def _get_month_context(user, year, month):
    month_data = _get_month_data(user, year, month)
    context = {
        "year": year,
        "name": month_name[month],
        "data": month_data,
    }

    return context

def _get_previous_month_context(year, month):
    if month == JANUARY:
        return {
            "year": year - 1,
            "month": DECEMBER,
        }

    return {
        "year": year,
        "month": month - 1,
    }

def _get_next_month_context(year, month):
    if month == DECEMBER:
        return {
            "year": year + 1,
            "month": JANUARY,
        }

    return {
        "year": year,
        "month": month + 1,
    }

def _get_current_month_context():
    today = date.today()

    return {
        "year": today.year,
        "month": today.month,
    }

def _get_month_data(user, year, month):
    calendar_data = Calendar(firstweekday=FIRST_WEEKDAY)

    user_items = Item.objects.filter(user=user)

    # TODO Make this include all dates between start and end datetimes.
    date_item_map = defaultdict(list)
    for item in user_items:
        item_date = item.start_datetime.date()
        date_item_map[item_date].append(item)

    month_data = []

    weeks = calendar_data.monthdatescalendar(year, month)
    for week in weeks:
        week_data = []

        for day_date in week:
            is_day_in_month = day_date.month == month
            if not is_day_in_month:
                week_data.append(None)
                continue

            day_date_data = {
                "date": day_date,
                "items": date_item_map[day_date],
            }

            week_data.append(day_date_data)

        month_data.append(week_data)

    return month_data
