from django.db import models


class User(models.Model):
    def __unicode__(self):
        return self.user.username

    user = models.OneToOneField('auth.User', unique=True)
    type = models.CharField(max_length=1)
    ChineseName = models.CharField(max_length=255, null=True, blank=True)
    EnglishName = models.CharField(max_length=255, null=True, blank=True)
    Class = models.ManyToManyField('assignment.Class')
    subject = models.CharField(max_length=255, null=True, blank=True)


class Class(models.Model):
    def __unicode__(self):
        return self.name

    teacher = models.ForeignKey('auth.User')
    name = models.CharField(max_length=255)
    assignments = models.ManyToManyField('assignment.Assignment')


class Attachment(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)
    content = models.FileField()
    md5 = models.CharField(max_length=255)


class Assignment(models.Model):
    def __unicode__(self):
        return self.content[:16]

    type = models.SmallIntegerField()
    content = models.TextField()
    duration = models.IntegerField()
    assignments = models.ManyToManyField('assignment.Attachment')

    Class = models.ForeignKey('assignment.Class')
    teacher = models.ForeignKey('assignment.User')

    publish = models.DateField(auto_now=True)
    due = models.DateTimeField()


class PersonalAssignment(models.Model):
    def __unicode__(self):
        return self.id
    id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    assignment = models.ForeignKey('assignment.Assignment')
    student = models.ForeignKey('assignment.User')
