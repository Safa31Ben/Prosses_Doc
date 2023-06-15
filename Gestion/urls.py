from django.urls import path, include
from . import views

from rest_framework.routers import SimpleRouter
from .views import LoginViewSet, RegistrationViewSet, UtilisateurUpdateViewSet

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r"auth/login", LoginViewSet, basename="auth-login")
routes.register(r"auth/register", RegistrationViewSet, basename="auth-register")

urlpatterns = [
    *routes.urls,
    path("api-auth/", include("rest_framework.urls")),
    path("user_List", views.user_list, name="user_update"),
    path(
        "update/<str:pk>",
        UtilisateurUpdateViewSet.as_view({"put": "update"}),
        name="user_update",
    ),
    path("DeleteUser/<str:pk>", views.DeleteUser, name="DeleteUser"),
    path("User_detail/<str:pk>", views.user_detail, name="UserDetail"),
    path("AddEmplacement/", views.AddEmplacement, name="AddEmplacement"),
    path("AddConcoursAndSujet/", views.AddConcoursAndSujet, name="AddConcoursAndSujet"),
]
