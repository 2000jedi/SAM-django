from __future__ import print_function
from django.http import HttpResponse
import mimetypes

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils import timezone
import urllib


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
            raise StandardError
        login(request, user)
        return redirect('/')
    except:
        return render(request, 'login.html', {'msg': msg})


def logout_view(request):
    logout(request)
    return redirect('/')


# sort by nearest due date and then longest since published
def sort_fun(a, b):
    if a.due != b.due:
        return a.due < b.due
    return a.publish > b.publish


# attachment dealer
def attachment_get(request, uri):
    if not request.user.is_authenticated():
        return redirect('/login')
    try:
        attach = Attachment.objects.filter(md5=uri).all().first()
    except:
        raise KeyError

    f = attach.content.open('rb')
    response = HttpResponse(f.read())
    mime, encoding = mimetypes.guess_type(f)
    if mime is None:
        mime = 'application/octet-stream'
    response['Content-Type'] = mime
    response['Content-Length'] = str(attach.size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % attach.name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(attach.name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def attachment_upload(attach):
    pass


def settings_view(request, alert_password=False):
    if not request.user.is_authenticated():
        return redirect('/login')

    return render(request, 'settings.html', {'alert':alert_password})


def settings_adjust(request, uri):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise KeyError(request.method + " is not supported")
    if uri == 'password':
        if request.user.check_password(request.POST['oldPass']):
            request.user.set_password(request.POST['newPass'])
            request.user.save()
            return "success"
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

    if user.type == u's':
        classes = user.Class.all()
        query = {
            'classes': classes
        }
        return render(request, 'classes_s.html', query)
    if user.type == u't':
        classes = user.Class.all()
        query = {
            'classes': classes
        }
        return render(request, 'classes_s.html', query)


def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    user = User.objects.filter(user=request.user).first()

    if user.type == u's':
        assignment_query = {}
        finished = {}
        count_completion = {
            'total': 0,
            'completed': 0
        }
        for user_class in user.Class.all():
            for i in user_class.assignments.filter(due__gte=timezone.now()).all():
                if PersonalAssignment.objects.filter(student=user).filter(assignment=i).count() == 0:
                    finished[len(assignment_query)] = False
                else:
                    count_completion['completed'] += 1
                    finished[len(assignment_query)] = True
                assignment_query[len(assignment_query)] = i

                # Only type 1 (assignment) is counted
                if i.type == 1:
                    count_completion['total'] += 1

        percentage = 1.0
        if count_completion['total'] != 0:
            percentage = count_completion['completed'] * 1.0 / count_completion['total']

        # sort cards by time
        for i in range(len(assignment_query)):
            for j in range(i+1, len(assignment_query)):
                if not sort_fun(assignment_query[i], assignment_query[j]):
                    assignment_query[i], assignment_query[j] = assignment_query[j], assignment_query[i]
                    finished[i], finished[j] = finished[j], finished[i]

        query = {
            "assignments": assignment_query,
            "vertical": (-40 + 189 * len(assignment_query)),
            "percentage": percentage,
            "finished": finished
        }
        return render(request, 'dashboard_s.html', query)
    if user.type == u't':
        return redirect('/classes')


def markComplete(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise KeyError("Method Not Supported")

    user = User.objects.filter(user=request.user).first()
    newPA = PersonalAssignment(assignment=Assignment.objects.filter(id=request.POST['assignment_id']).first()
                               , student=user)
    newPA.save()
    return redirect('/')


def markUnComplete(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != 'POST':
        raise KeyError("Method Not Supported")

    user = User.objects.filter(user=request.user).first()
    for PA in PersonalAssignment.objects.filter(student=user,
                                                assignment=Assignment.objects.filter(id=request.POST['assignment_id']))\
            .all():
        PA.delete()
    return redirect('/')


def update_sql():
    # remove outdated info
    for i in PersonalAssignment.objects.all():
        if i.assignment.due < timezone.now():
            i.delete()
