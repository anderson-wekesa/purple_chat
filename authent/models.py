from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class PurpleUsersManager(BaseUserManager):
    def create_user(self, username, email, password, image):
        email = self.normalize_email(email)

        # if image is None:
        #     image = 'generic_user.jpg'
            
        user = self.model(email=email, username=username, image='generic_user.jpg')
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username = username, email = email, password = password, image='generic_user.jpg')

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user



class PurpleUsers(AbstractBaseUser):
    username = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(max_length = 256, unique = True)
    image = models.ImageField(upload_to='profiles/', default='generic_user.jpg', blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = PurpleUsersManager()

    #Fields required when creating a superuser
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length = 1000)
    time = models.TimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.content[:16]
