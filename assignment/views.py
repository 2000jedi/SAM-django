from __future__ import print_function
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils import timezone


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


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        user = User.objects.filter(user=request.user)[0]
    except:
        return redirect('/login')
    user_type = user.type
    if user_type == u's':
        assignment_query = []
        for user_class in user.Class.all():
            for i in user_class.assignments.filter(due__gte=timezone.now()).all():
                if PersonalAssignment.objects.filter(student=user).filter(assignment=i).count() == 0:
                    assignment_query.append(i)

        assignment_query.sort(cmp=sort_fun)

        query = {
            "assignments": assignment_query,
            "vertical": (-40 + 189 * len(assignment_query)),
            "percentage": 0.00
        }
        return render(request, 'student.html', query)
    if user_type == u't':
        pass