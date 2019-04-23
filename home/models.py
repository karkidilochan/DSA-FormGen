from django.db import models
import os

SEM_CHOICES = (
        ('ODD', 'ODD'),
        ('EVEN', 'EVEN'),
     )

CLASS_CHOICES = (
        ('0', 'Lecture'),
        ('1', 'Practical'),
        ('2', 'Tutorial'),
        ('3', 'Project(4students)'),
        ('4', 'Project(3students)')

     )

PROG_CHOICES = (
        ('0', 'BEX'),
        ('1', 'BCT'),
        ('2', 'BCE'),
        ('3', 'BME'),
        ('4', 'BEL'),
        ('5', 'SH'),
     )


CLASSNO_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
     )

class Teacher_name(models.Model):

    teacher_name = models.CharField('Teacher name:', max_length=100, default='')


    class Meta:
        ordering = ('teacher_name',)
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.teacher_name


class Dsaform(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    dep_name = models.CharField('Department name:', max_length=1, choices=PROG_CHOICES, default='')
    sem_name = models.CharField('Semester(ODD/EVEN):', max_length=4, choices=SEM_CHOICES, default='')
    class_no = models.CharField('No. of days per week:', max_length=100, choices=CLASSNO_CHOICES, default='')
    teachername = models.ForeignKey(Teacher_name, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
        verbose_name = "Dsaform"
        verbose_name_plural = "Dsaforms"

    def __str__(self):
        return self.teachername.teacher_name


class Subject_name(models.Model):

    subject_name = models.CharField('Enter subject name:', max_length=100, default='')

    class Meta:
        ordering = ('subject_name',)
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.subject_name


class Subject(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    dsaform = models.ForeignKey(Dsaform, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject_name, on_delete=models.CASCADE)
    program_name = models.CharField('Enter program:', max_length=1, choices=PROG_CHOICES, default='')
    class_type = models.CharField('Enter class type:', max_length=1, choices=CLASS_CHOICES, default='')
    class_num = models.FloatField('Enter the no. of periods per week:', max_length=5, default='')





from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=Dsaform)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    teacher = instance.teachername.teacher_name
    teacher = teacher.replace(' ', '')
    if os.remove(str(teacher.lower()) + '.docx'):
        os.remove(str(teacher.lower()) + '.docx')

