from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email):
        user = self.model(username=username, email=email)
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.model(
            username=username, email=email, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        return self.get(username=username_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(
        max_length=128,
        blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.username

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username
