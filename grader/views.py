import pandas as pd

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import User, Course, Result
from .forms import CourseForm
# Create your views here.

def index(request):
    user = request.user
    try:
        if user.is_student:
            return render(request, 'grader/student.html')
        if user.is_lecturer:
            courses = Course.objects.all().order_by('course_code')
            ctx = {
                'courses': courses
            }
            return render(request, 'grader/lecturer.html', ctx)
    except AttributeError:
        return render(request, 'grader/index.html')
    return render(request, 'grader/index.html')

@login_required
def upload(request):
    if request.POST:
        course_id = request.POST["course"]
        c = Course.objects.get(id=int(course_id))
        file = request.FILES["file"]
        if file:
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                username = row['Matric Number']
                test_score=int(row['Test Score'])
                exam_score=int(row['Exam Score'])
                aggr = test_score + exam_score
                if aggr >= 70 and aggr <= 100:
                    grade = 5
                elif aggr >= 60 and aggr <= 69:
                    grade = 4
                elif aggr >= 50 and aggr <= 59:
                    grade = 3
                elif aggr >= 45 and aggr <= 49:
                    grade = 2
                elif aggr >= 40 and aggr <= 44:
                    grade = 1
                else:
                    grade = 0
                result = Result.objects.create(
                    student=User.objects.get(username=username),
                    course=c,
                    test_score=test_score,
                    exam_score=exam_score,
                    grade = grade
                )
                
                result.save()
        return redirect(course, id=int(course_id))

@login_required
def check_result(request):
    r = Result.objects.filter(student=request.user)
    tcp, tnu, gp = 0, 0, 0
    
    for result in r:
        u = result.course.unit
        tnu += u
        cp = result.grade * u
        tcp += cp
    
    gp = tcp/tnu

        
    ctx = {
        'results': r,
        'tcp': tcp,
        'tnu': tnu,
        'gp': gp,
    }
    return render(request, 'grader/result.html', ctx)

@login_required
def addcourse(request):
    user = request.user
    if user.is_lecturer:
        if request.POST:
            form_data = CourseForm(request.POST)
            if form_data.is_valid():
                x = form_data.save()
                return redirect(course, id=x.id) 
        ctx = {'form': CourseForm}
        return render(request, 'grader/addcourse.html', ctx)
    return redirect(index)

@login_required
def courses(request):
    ctx = {
        'courses': Course.objects.all().order_by('course_code')
    }
    return render(request, 'grader/courses.html', ctx)

@login_required
def course(request, id):
    user = request.user
    if user.is_lecturer:
        ctx = {
            'course': Course.objects.get(id=id)
        }
        return render(request, 'grader/course.html', ctx)
    return redirect(courses)


def login_view(request):   

    if request.method == "POST":
        next = request.POST['next']
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            
            if next == "":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(next)
        else:
            return render(request, "grader/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "grader/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        user_type = request.POST["type"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "grader/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if user_type == 'student':
                user.is_student = True
            elif user_type == 'lecturer':
                user.is_lecturer = True
            user.save()
        except IntegrityError:
            return render(request, "grader/register.html", {
                "message": "Username/Email already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "grader/register.html")

