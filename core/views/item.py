from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_POST

from core.forms import ItemForm
from core.models import Item

CALENDAR_URL_NAME = "core:calendar"
EDIT_URL_NAME = "core:edit_item"
TEMPLATE_PATH = "core/item.html"

@require_http_methods(["GET", "POST"])
@login_required
def create(request):
    if request.method == "GET":
        return _create_get(request)

    return _create_post(request)

@require_http_methods(["GET", "POST"])
@login_required
def edit(request, item_id):
    if request.method == "GET":
        return _edit_get(request, item_id)

    return _edit_post(request, item_id)

@require_POST
@login_required
def delete(request, item_id):
    item = _get_user_item_or_404(user=request.user, item_id=item_id)
    item.delete()
    return redirect(CALENDAR_URL_NAME)

def _create_get(request):
    context = {
        "form": ItemForm(user=request.user),
    }

    return render(
        request,
        TEMPLATE_PATH,
        context,
    )

def _create_post(request):
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

    return redirect(EDIT_URL_NAME, item_id=created_item.id)

def _edit_get(request, item_id):
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

def _edit_post(request, item_id):
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

    return redirect(CALENDAR_URL_NAME)

def _get_user_item_or_404(user, item_id):
    return get_object_or_404(
        Item,
        user=user,
        id=item_id,
    )
