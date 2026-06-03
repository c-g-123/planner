from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from core.forms import TagForm
from core.models import Tag

TAGS_URL_NAME = "core:tags"
EDIT_TAG_URL_NAME = "core:edit_tag"
TAGS_TEMPLATE_PATH = "core/tags.html"
TAG_TEMPLATE_PATH = "core/tag.html"

@require_GET
@login_required
def tags(request):
    user_tags = Tag.objects.filter(user=request.user)

    context = {
        "tags": user_tags,
    }

    return render(request, TAGS_TEMPLATE_PATH, context)

@require_http_methods(["GET", "POST"])
@login_required
def create(request):
    if request.method == "GET":
        return _create_get(request)

    return _create_post(request)

@require_http_methods(["GET", "POST"])
@login_required
def edit(request, tag_id):
    if request.method == "GET":
        return _edit_get(request, tag_id)

    return _edit_post(request, tag_id)

@require_POST
@login_required
def delete(request, tag_id):
    tag = _get_user_tag_or_404(user=request.user, tag_id=tag_id)
    tag.delete()
    return redirect(TAGS_URL_NAME)

def _create_get(request):
    context = {
        "form": TagForm(user=request.user),
    }

    return render(
        request,
        TAG_TEMPLATE_PATH,
        context
    )

def _create_post(request):
    form = TagForm(data=request.POST, user=request.user)

    if not form.is_valid():
        context = {
            "form": form,
        }

        return render(
            request,
            TAG_TEMPLATE_PATH,
            context
        )

    created_tag = form.save(commit=False)
    created_tag.user = request.user
    created_tag.save()

    return redirect(EDIT_TAG_URL_NAME, tag_id=created_tag.id)

def _edit_get(request, tag_id):
    tag = _get_user_tag_or_404(user=request.user, tag_id=tag_id)
    form = TagForm(instance=tag, user=request.user)

    context = {
        "form": form,
    }

    return render(
        request,
        TAG_TEMPLATE_PATH,
        context
    )

def _edit_post(request, tag_id):
    tag = _get_user_tag_or_404(user=request.user, tag_id=tag_id)
    form = TagForm(data=request.POST, instance=tag, user=request.user)

    context = {
        "form": form,
    }

    if not form.is_valid():
        return render(
            request,
            TAG_TEMPLATE_PATH,
            context
        )

    form.save()

    return redirect(EDIT_TAG_URL_NAME, tag_id=tag.id)

def _get_user_tag_or_404(user, tag_id):
    return get_object_or_404(
        Tag,
        user=user,
        id=tag_id
    )
