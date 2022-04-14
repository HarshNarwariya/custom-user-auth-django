from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, password2=None,
    is_admin=False, is_student=True):
        
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.is_student = is_student
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=True,
            is_student=False,
        )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # Personal Details
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    # is account active
    is_active = models.BooleanField(default=True)

    # accounts basic details
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_interviewer = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    # account created date and update date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    # Changing auth model to authorize using email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def has_related_object(self, attr):
        return hasattr(self, attr)

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.email

# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDERS = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
    )
    gender = models.CharField(choices=GENDERS, default='M', max_length=1)

    def __str__(self):
        return self.user.email
    
    def delete(self, using=None, keep_parents=None):
        self.user.is_admin = False
        self.user.save()
        return super().delete(using, keep_parents)

# Faculty Model
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDERS = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
    )
    gender = models.CharField(choices=GENDERS, default='M', max_length=1)

    def __str__(self):
        return self.user.email
    
    def delete(self, using=None, keep_parents=None):
        self.user.is_faculty = False
        self.user.save()
        return super().delete(using, keep_parents)

    class Meta:
        verbose_name_plural = 'Faculties'

# Interviewer Model
class Interviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDERS = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
    )
    gender = models.CharField(choices=GENDERS, default='M', max_length=1)

    def __str__(self):
        return self.user.email
    
    def delete(self, using=None, keep_parents=None):
        self.user.is_interviewer = False
        self.user.save()
        return super().delete(using, keep_parents)