from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, date_of_birth, avatar,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            date_of_birth=date_of_birth,
            avatar=avatar,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            date_of_birth=date_of_birth,
            avatar=None,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_student(self, email, full_name, date_of_birth, password=None):
        """
        Creates and saves a student with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            date_of_birth=date_of_birth,
            avatar=None,
        )

        user.is_student = True
        user.save(using=self._db)
        return user

    def create_educator(self, email, full_name, date_of_birth, password=None):
        """
        Creates and saves a educator with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            date_of_birth=date_of_birth,
            avatar=None,
        )

        user.is_educator = True
        user.save(using=self._db)
        return user

    def create_unistuff(self, email, full_name, date_of_birth, password=None):
        """
        Creates and saves a unistuff with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            date_of_birth=date_of_birth,
            avatar=None,
        )

        user.is_unistuff = True
        user.save(using=self._db)
        return user
