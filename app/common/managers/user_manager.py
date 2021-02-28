from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        uuid,
        password=None,
        is_active=False,
        is_staff=False,
        is_superuser=False,
        **kwargs
    ):
        if not uuid:
            raise ValueError("Users must have an uuid")

        user = self.model(uuid=uuid, **kwargs)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        if password is not None:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, uuid, password=None, **kwargs):
        return self.create_user(
            uuid, password, is_active=True, is_staff=True, is_superuser=True, **kwargs
        )
