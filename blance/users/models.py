from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Користувач повинен мати або email, або телефон")

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    password_update_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    USERNAME_FIELD = "email"  # Основний ідентифікатор - email
    REQUIRED_FIELDS = ["phone"]  # Телефон обов’язковий тільки при реєстрації

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.phone if self.phone else "Без імені"

    def get_username(self):
        return self.email if self.email else self.phone

    def save(self, *args, **kwargs):
        if self.pk:
            old = User.objects.get(pk=self.pk)

            if old.password != self.password:
                self.password_update_at = timezone.now()
        super().save(*args, **kwargs)
