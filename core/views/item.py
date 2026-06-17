from datetime import datetime
from json import dumps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST

from core.forms import ItemForm
from core.models import Item

URL_NAME = "core:item"
CALENDAR_URL_NAME = "core:calendar"
TEMPLATE_PATH = "core/item.html"

@require_http_methods(["GET", "POST"])
@login_required
def create(request):
    if request.method == "GET":
        return _render_create_form(request)

    return _process_create_form(request)

@require_http_methods(["GET", "POST"])
@login_required
def item_view(request, item_id):
    if request.method == "GET":
        return _render_edit_form(request, item_id)

    return _process_edit_form(request, item_id)

@require_POST
@login_required
def delete(request, item_id):
    item = _get_user_item_or_404(user=request.user, item_id=item_id)
    item.delete()

    empty_response = HttpResponse()
    _attach_item_updated_htmx_trigger(empty_response)
    return empty_response

def _render_create_form(request):
    date_str = request.GET.get("date")

    initial_form = {}

    if date_str:
        initial_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        initial_form["start_datetime"] = initial_datetime

    form = ItemForm(initial=initial_form, user=request.user)
    context = {
        "form": form,
    }

    return render(
        request,
        TEMPLATE_PATH,
        context,
    )

def _process_create_form(request):
    form = ItemForm(data=request.POST, user=request.user)

    if not form.is_valid():
        context = {
            "form": form,
        }

        return render(
            request,
            TEMPLATE_PATH,
            context,
        )

    created_item = form.save(commit=False)
    created_item.user = request.user
    created_item.save()

    response = _render_edit_form(request, created_item.id)
    _attach_item_updated_htmx_trigger(response)
    return response

def _render_edit_form(request, item_id):
    item = _get_user_item_or_404(user=request.user, item_id=item_id)
    form = ItemForm(instance=item, user=request.user)
    context = {
        "form": form,
    }

    return render(
        request,
        TEMPLATE_PATH,
        context,
    )

def _process_edit_form(request, item_id):
    item = _get_user_item_or_404(user=request.user, item_id=item_id)
    form = ItemForm(
        data=request.POST,
        instance=item,
        user=request.user,
    )
    context = {
        "form": form,
    }

    if not form.is_valid():
        return render(
            request,
            TEMPLATE_PATH,
            context,
        )

    form.save()

    response = render(
        request,
        TEMPLATE_PATH,
        context,
    )
    _attach_item_updated_htmx_trigger(response)
    return response

def _get_user_item_or_404(user, item_id):
    return get_object_or_404(
        Item,
        user=user,
        id=item_id,
    )

#TODO Check if mutation matters here.
def _attach_item_updated_htmx_trigger(response):
    hx_trigger = {
        "itemUpdated": True,
    }
    serialised_hx_trigger = dumps(hx_trigger)
    response["HX-Trigger"] = serialised_hx_trigger
