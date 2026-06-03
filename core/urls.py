from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),

    path("register/", views.authentication.register, name="register"),
    path("login/", views.authentication.login_view, name="login"),
    path("logout/", views.authentication.logout_view, name="logout"),

    path("calendar/", views.board.calendar, name="calendar"),

    path("item/create/", views.item.create, name="create_item"),
    path("item/<item_id>/edit/", views.item.edit, name="edit_item"),
    path("item/<item_id>/delete/", views.item.delete, name="delete_item"),

    path("tags/", views.tag.tags, name="tags"),
    path("tag/create/", views.tag.create, name="create_tag"),
    path("tag/<tag_id>/edit/", views.tag.edit, name="edit_tag"),
    path("tag/<tag_id>/delete/", views.tag.delete, name="delete_tag"),
]
