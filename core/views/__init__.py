from django.shortcuts import redirect, render

import core.views.authentication
import core.views.board
import core.views.item
import core.views.tag

CALENDAR_URL = "core:calendar"
INDEX_TEMPLATE_PATH = "core/index.html"

def index(request):
    return render(request, INDEX_TEMPLATE_PATH)
