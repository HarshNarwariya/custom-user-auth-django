# custom-user-auth-django


### Django Custom User Authentication

**For authorization it uses email of the user instead of username.**

Follow these steps to create custom user model. 
NOTE: Interviewer, Student, Faculty and Admin are the profiles associated with different users. Like admin has Admin profile and student has Student profile.

### models.py

```python
from django.db import models

# import BaseUserManager and AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

# Manager for customuser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, password2=None,
    is_admin=False, is_student=True):
        '''
        Function which is used to create a user which is by default a student.
        
        To make admin pass is_admin=True
        '''
        
        # email is not given raise error
        if not email:
            raise ValueError('User must have an email address')
            
        # create user instance
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        
        # set password
        user.set_password(password)
        
        # set attrs
        user.is_admin = is_admin
        user.is_student = is_student
        
        # save the instance, but before saving grab signals
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        '''
        Function to create superuser
        '''
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

# User model
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
    
    # is user student?
    is_student = models.BooleanField(default=True)
    
    # is user interviewer?
    is_interviewer = models.BooleanField(default=False)
    
    # is user faculty?
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
```

### signals.py

```python
from django.db.models.signals import post_save
from accounts.models import Admin, User, Student, Faculty, Interviewer
from django.dispatch import receiver
# from django.core.exceptions import Related

# take post_save signal from User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_admin:
            Admin.objects.create(user=instance)
        if instance.is_interviewer:
            Interviewer.objects.create(user=instance)
        if instance.is_faculty:
            Faculty.objects.create(user=instance)
        if instance.is_student:
            Student.objects.create(user=instance)
        

# save instance whenever updated or created
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_admin:
        if not instance.has_related_object('admin'):
            Admin.objects.create(user=instance)
        instance.admin.save()

    if instance.is_student == True:
        if not instance.has_related_object('student'):
            Student.objects.create(user=instance)
        instance.student.save()

    if instance.is_faculty == True:
        if not instance.has_related_object('faculty'):
            Faculty.objects.create(user=instance)
        instance.faculty.save()
    
    if instance.is_interviewer == True:
        if not instance.has_related_object('interviewer'):
            Student.objects.create(user=instance)
        instance.student.save()
    
```

### admin.py
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import Admin, Faculty, Interviewer, Student, User

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_student', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_student', 'is_interviewer', 'is_faculty',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'is_admin', 'is_student', 'is_faculty', 'is_interviewer', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(Interviewer)
```

### settings.py
```python
...
INSTALLED_APPS = [
  ...
  # Mention the apps here
  'accounts.apps.AccountsConfig',
  ...
]
...
# change auth model to our custom model
AUTH_USER_MODEL = 'accounts.User'
...
```

### run

```python
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
...
python manage.py runserver
```

After that go to admin panel at '/admin'
