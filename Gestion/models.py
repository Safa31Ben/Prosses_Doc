from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email.")

        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    TYPE = [
        ("admin", "Admin"),
        ("candidat", "Candidat"),
        ("vice-doyen", "Vice-doyen"),
        ("président-du-CFD", "Président du CFD"),
        ("enseignant", "Enseignant"),
    ]
    type = models.CharField(max_length=50, choices=TYPE, blank=False, null=False)
    username = models.CharField(
        db_index=True, max_length=25, unique=True, blank=False, null=False
    )
    email = models.EmailField(
        db_index=True, max_length=60, unique=True, blank=False, null=False
    )

    nom = models.CharField(max_length=50, blank=False, null=False)
    prenom = models.CharField(max_length=50, blank=False, null=False)
    date_naissance = models.DateField(null=False, blank=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def get_full_name(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        db_table = "utilisateur"
