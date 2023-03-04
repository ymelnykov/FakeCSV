from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create_schema", views.create_schema, name="create_schema"),
    path("update_schema", views.update_schema, name="update_schema"),
    path("delete_schema", views.delete_schema, name="delete_schema"),
    path("create_dataset", views.create_dataset, name="create_dataset"),
]