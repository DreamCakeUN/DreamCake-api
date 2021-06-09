from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.db import models
from pedido.models import Pastel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Los usuarios deben tener un correo electronico")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):	
	email = models.EmailField(
		verbose_name='email',
		unique=True,
		db_index=True,
	)
	full_name = models.CharField(
		max_length=191,
		blank=True,
	)
	short_name = models.CharField(
		max_length=191,
		blank=True,
	)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	foto = models.ImageField(upload_to='users', null=False, default='/users/default.jpg')

	objects = UserManager()

	USERNAME_FIELD = "email"

	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.short_name

	def __str__(self):
		return f"{self.email} ({self.full_name})"