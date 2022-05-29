import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import string
import random


class UserAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password=None):
        if not email:
            raise ValueError('User must has an email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.is_staff = True
        user.ia_admin = True
        user.is_superuser = True
        user.save()
        return user

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must has an email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    affiliated_from = models.ForeignKey('self',
                                        models.SET_NULL,
                                        null=True,
                                        blank=True)
    affiliated_code = models.CharField(max_length=10, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0, null=False, blank=False)
    phone = models.CharField(max_length=21, default='')
    address = models.CharField(max_length=256, default='')
    town = models.CharField(max_length=56, default='')
    postalcode = models.CharField(max_length=11, default='')
    country = models.CharField(max_length=250, default='')
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.affiliated_code:
            # Generate ID once, then check the db. If exists, keep trying.
            self.affiliated_code = id_generator()
            while UserAccount.objects.filter(
                    affiliated_code=self.affiliated_code).exists():
                self.affiliated_code = id_generator()
        super(UserAccount, self).save()