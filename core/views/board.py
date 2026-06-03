from calendar import Calendar, MONDAY, month_name
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import Item

CALENDAR_TEMPLATE_PATH = "core/board/calendar.html"

@require_GET
@login_required
def calendar(request):
    items = Item.objects.filter(user=request.user)
    context = {"months": _get_populated_months(items)}
    return render(request, CALENDAR_TEMPLATE_PATH, context)

# TODO Refactor this function written by George.
def _get_populated_months(items):
    today = date.today()

    items_by_day = defaultdict(list)

    for item in items:
        items_by_day[item.start_datetime.date()].append(item)

    cal = Calendar(firstweekday=MONDAY)

    months = []

    for month_offset in range(-3, 9):
        month = today.month + month_offset
        year = today.year

        while month < 1:
            month += 12
            year -= 1

        while month > 12:
            month -= 12
            year += 1

        weeks = []

        for week in cal.monthdayscalendar(year, month):
            week_data = []

            for day in week:
                if day == 0:
                    week_data.append(None)
                    continue

                day_date = date(year, month, day)

                week_data.append({
                    "date": day_date,
                    "items": items_by_day[day_date],
                })

            weeks.append(week_data)

        months.append({
            "name": month_name[month],
            "year": year,
            "weeks": weeks,
        })

    return months
