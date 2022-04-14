from django.db.models.signals import post_save
from accounts.models import Admin, User, Student, Faculty, Interviewer
from django.dispatch import receiver
# from django.core.exceptions import Related


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
    