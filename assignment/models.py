from django.db import models
import datetime
import hashlib
import random


class User(models.Model):
    def __unicode__(self):
        return self.user.username

    user = models.OneToOneField('auth.User', unique=True)
    type = models.CharField(max_length=1)
    ChineseName = models.CharField(max_length=255, blank=True)
    EnglishName = models.CharField(max_length=255, blank=True)
    Class = models.ManyToManyField('assignment.Class', default=[], blank=True)
    subject = models.CharField(max_length=255, blank=True)


class Class(models.Model):
    def __unicode__(self):
        return self.name

    teacher = models.ForeignKey('assignment.User')
    name = models.CharField(max_length=255)
    assignments = models.ManyToManyField('assignment.Assignment', default=[])


class Attachment(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to='Files')
    md5 = models.CharField(max_length=255, primary_key=True, unique=True)

    def get_size(self):
        return self.content.size
    size = property(get_size)

    def save(self, *args, **kwargs):
        self.content.name += random.choice(range(1, 10000))
        super(Attachment, self)
        f = self.content.open('rb')
        md5 = hashlib.md5()
        if f.multiple_chunks():
            for chunk in f.chunks():
                md5.update(chunk)
        else:
            md5.update(f.read())
        f.close()
        self.md5 = md5.hexdigest()


class Assignment(models.Model):
    def __unicode__(self):
        return self.content[:16]

    type = models.SmallIntegerField()
    content = models.TextField()
    duration = models.IntegerField(null=True, blank=True)
    attachments = models.ManyToManyField('assignment.Attachment', default=[], blank=True)

    def get_attachments(self):
        return self.attachments.all()
    attachment_query = property(get_attachments)

    Class = models.ForeignKey('assignment.Class')
    teacher = models.ForeignKey('assignment.User')

    publish = models.DateField(auto_now=True)
    due = models.DateTimeField(default=datetime.datetime(2030, 1, 1), blank=True)


class PersonalAssignment(models.Model):
    def __unicode__(self):
        return str(self.id)
    id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    assignment = models.ForeignKey('assignment.Assignment')
    student = models.ForeignKey('assignment.User')
