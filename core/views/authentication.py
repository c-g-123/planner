from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods, require_POST

CALENDAR_URL_NAME = "core:calendar"
INDEX_URL_NAME = "core:index"

TEMPLATE_PATH = "core/authentication.html"

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect(CALENDAR_URL_NAME)

    if request.method == "GET":
        return _register_get(request)

    return _register_post(request)

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect(CALENDAR_URL_NAME)

    if request.method == "GET":
        return _login_get(request)

    return _login_post(request)

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect(INDEX_URL_NAME)

def _register_get(request):
    context = {
        "form": UserCreationForm(),
        "is_registration": True,
    }

    return render(
        request,
        TEMPLATE_PATH,
        context,
    )

def _register_post(request):
    form = UserCreationForm(request.POST)

    if not form.is_valid():
        context = {
            "form": form,
            "is_registration": True,
        }

        return render(
            request,
            TEMPLATE_PATH,
            context,
        )

    created_user = form.save()
    login(request, created_user)

    return redirect(CALENDAR_URL_NAME)

def _login_get(request):
    context = {
        "form": AuthenticationForm(),
        "is_registration": False,
    }

    return render(
        request,
        TEMPLATE_PATH,
        context,
    )

def _login_post(request):
    form = AuthenticationForm(request, data=request.POST)

    if not form.is_valid():
        context = _get_authentication_context(form, is_registration=False)

        return render(
            request,
            TEMPLATE_PATH,
            context,
        )

    authenticated_user = form.get_user()
    login(request, authenticated_user)

    return redirect(CALENDAR_URL_NAME)

def _get_authentication_context(form, is_registration):
    context = {
        "form": form,
        "is_registration": is_registration,
    }

    return context
