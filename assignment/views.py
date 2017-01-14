from __future__ import print_function
from django.http import HttpResponse
import mimetypes

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation, PermissionDenied, ObjectDoesNotExist
import urllib


class AssignmentForm:  # Student side assignment form
    assignment = None
    finished = None
    index = None

    def __init__(self, assignments, finished_status):
        self.assignment = assignments
        self.finished = finished_status

    def __cmp__(self, other):
        return self.assignment.due < other.assignment.due if self.assignment.due != other.assignment.due else self.assignment.publish > other.assignment.publish


class StudentForm:
    student = None
    enrolled = None

    def __init__(self, student, enrolled):
        self.student = student
        self.enrolled = enrolled

    def __cmp__(self, other):
        return True if self.enrolled else False if other.enrolled else self.student.user.id < other.student.user.id


class ClassForm:
    Class = None
    student_enrolled = None

    def __init__(self, Class):
        self.Class = Class
        self.student_enrolled = filter(lambda x: x is not None, [student if student.Class.filter(id=self.Class.id).count() != 0 else None for student in User.objects.filter(type='s').all()])


# logging
def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    msg = False
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            msg = True
            raise PermissionDenied("Username and Password does not match")
        login(request, user)
        return redirect('/')
    except:
        return render(request, 'login.html', {'msg': msg})


def logout_view(request):
    logout(request)
    return redirect('/')


# attachment dealer
def attachment_get(request, uri):
    if not request.user.is_authenticated():
        return redirect('/login')
    try:
        attach = Attachment.objects.filter(md5=uri).all().first()
    except:
        raise ObjectDoesNotExist("File not exists")

    with attach.content as f:
        f_bytes = f.read()
        f.close()
    response = HttpResponse(f_bytes)
    mime, encoding = mimetypes.guess_type(f_bytes)
    response['Content-Type'] = 'application/octet-stream' if mime is None else mime
    response['Content-Length'] = str(attach.size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    # Chrome and Firefox behave differently
    filename_header = 'filename=%s' % attach.name.encode('utf-8') if u'WebKit' in request.META['HTTP_USER_AGENT'] else 'filename*=UTF-8\'\'%s' % urllib.quote(attach.name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def attachment_upload():  # TODO: Everything about uploading attachment
    pass


def settings_view(request, alert_password=False):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:
        return render(request, 'settings.html', {'alert': alert_password, 'user_type': User.objects.filter(user=request.user).first().type})


def settings_adjust(request, uri):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise PermissionDenied("Method not supported")
    if uri == 'password':
        if request.user.check_password(request.POST['oldPass']):
            request.user.set_password(request.POST['newPass'])
            request.user.save()
            return redirect('/settings')
        else:
            return settings_view(request, True)

    if uri == 'email':
        request.user.email = request.POST['email']
        request.user.save()
        return redirect('/settings')
    return settings_view(request)


def class_view(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    user = User.objects.filter(user=request.user).first()
    query = {'classes': user.Class.all(), 'blur': ''}

    if request.method == 'GET':
        if user.type == u's':
            return render(request, 'classes_s.html', query)
        else:
            query['classes'] = [ClassForm(i) for i in query['classes']]
            query['is_manage_user'] = False
            query['is_manage_assignment'] = False
            return render(request, 'classes_t.html', query)
    elif request.method == 'POST':
        if user.type == u's':
            raise PermissionDenied('Method not Supported')
        elif user.type == u't':
            class_id = request.POST['class_id']
            query['classes'] = [ClassForm(i) for i in query['classes']]
            query['class_id'] = class_id
            query['blur'] = 'blur'
            if request.POST['type'] == 'student':  # update students
                query['is_manage_user'] = True
                query['is_manage_assignment'] = False
                query['students'] = sorted([StudentForm(student, student.Class.filter(id=class_id).count() != 0) for student in User.objects.filter(type='s').all()])
            else:  # type == assignment
                if request.POST.get('assignment_id', -1) == '-1':  # add a new assignment
                    query['is_manage_user'] = False
                    query['is_manage_assignment'] = True
                    query['cur_class'] = Class.objects.filter(id=class_id).first()
                else:
                        query = {}  # not finished, if assignment id is a value it means a given assignment is here to revise
            return render(request, 'classes_t.html', query)


def update_student(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    user = User.objects.filter(user=request.user).first()
    if not user.type == u't':
        raise SuspiciousOperation('You are not allowed here')

    class_id = request.POST['class_id']
    if user.Class.filter(id=class_id).count() == 0:
        raise SuspiciousOperation('You are not allowed here')

    cls = user.Class.filter(id=class_id).first()
    for student in User.objects.filter(type="s").all():
        if request.POST[str(student.user.username)] == 'true':
            student.Class.add(cls)
        elif request.POST[str(student.user.username)] == 'false':
            student.Class.remove(cls)
        student.save()
    return redirect('/classes')


def single_class_view(request, class_id):
    if not request.user.is_authenticated():
        return redirect('/login')

    user = User.objects.filter(user=request.user).first()

    cls = Class.objects.filter(id=class_id).first()
    if User.objects.filter(user=request.user, Class=cls).count() == 0:
        raise PermissionDenied('You are not enrolled to this class')
    query = {'assignments': cls.assignments.all()}
    return render(request, 'single_class_s.html', query) if user.type == 's' else render(request, 'single_class_t.html', query)


def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    user = User.objects.filter(user=request.user).first()

    if user.type == u't':
        return redirect('/classes')

    if user.type == u's':
        aggregate = []
        count_finish = {'total': 0, 'finish': 0}
        for user_class in user.Class.all():
            for i in user_class.assignments.filter(due__gte=timezone.now()).all():
                if PersonalAssignment.objects.filter(student=user).filter(assignment=i).count() == 0:
                    aggregate.append(AssignmentForm(i, False))
                else:
                    if i.type == 1:
                        count_finish['finish'] += 1
                        aggregate.append(AssignmentForm(i, True))
                # Only type 1 (assignment) is counted
                if i.type == 1:
                    count_finish['total'] += 1

        # sort cards by time
        aggregate.sort()

        query = {
            "assignments": aggregate,
            "vertical": (-40 + 189 * len(aggregate)),
            "percentage": count_finish['finish'] * 1.0 / count_finish['total'] if count_finish['total'] != 0 else 1.0
        }
        return render(request, 'dashboard.html', query)


def mark_complete(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise PermissionDenied("Method Not Supported")

    new_pa = PersonalAssignment(assignment=Assignment.objects.filter(id=request.POST['assignment_id']).first(), student=User.objects.filter(user=request.user).first())
    new_pa.save()
    return redirect('/')


def mark_incomplete(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise PermissionDenied("Method Not Supported")

    for PA in PersonalAssignment.objects.filter(student=User.objects.filter(user=request.user).first(), assignment=Assignment.objects.filter(id=request.POST['assignment_id'])).all():
        PA.delete()
    return redirect('/')


def update_sql(request):
    if not request.user.is_superuser:
        raise SuspiciousOperation('Must be Admin')
    # remove outdated info
    for i in PersonalAssignment.objects.all():
        if i.assignment.due < timezone.now():
            i.delete()
    return redirect('/admin')

# TODO: Question & Answer
# TODO: Aggregate class files
# TODO: Club negotiation
