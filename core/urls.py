from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.index.index, name="index"),

    path("register/", views.authentication.register, name="register"),
    path("login/", views.authentication.login_view, name="login"),
    path("logout/", views.authentication.logout_view, name="logout"),

    path("calendar/", views.board.calendar.calendar_view, name="calendar"),
    path("calendar/month/current/", views.board.calendar.current_month, name="current_month"),
    path("calendar/month/<int:year>/<int:month>/", views.board.calendar.month_view, name="month"),

    path("item/create/", views.item.create, name="create_item"),
    path("item/<int:item_id>/", views.item.item_view, name="item"),
    path("item/<int:item_id>/delete/", views.item.delete, name="delete_item"),

    path("tags/", views.tag.tags, name="tags"),
    path("tag/create/", views.tag.create, name="create_tag"),
    path("tag/<int:tag_id>/", views.tag.tag_view, name="tag"),
    path("tag/<int:tag_id>/delete/", views.tag.delete, name="delete_tag"),
]
