import pytz as pytz
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm, LessonForm
from .models import Course, Lesson, Test, Question


def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    course = lesson.course  # Lấy khóa học liên quan đến bài học

    # Tìm bài học trước và sau


    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)  # Pass the instance for updating
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated successfully.')
            return redirect('lesson_detail', lesson_id=lesson_id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'form': form,
        'course': course,

    })

def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lesson_set.all()  # Lấy danh sách bài học của khóa học

    return render(request, 'course_lessons.html', {'course': course, 'lessons': lessons})

def start_test(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(test=test)
    return render(request, 'start_test.html', {'test': test, 'questions': questions})


def submit_test(request, test_id):
    if request.method == 'POST':
        test = Test.objects.get(id=test_id)
        questions = Question.objects.filter(test=test)
        score = 0
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.id}', None)
            if selected_choice == question.correct_choice:
                score += 1
        test.end_time = timezone.now()
        test.save()
        return render(request, 'test_result.html', {'test': test, 'score': score})
    return redirect('start_test', test_id)


def test_result(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(test=test)
    score = 0
    for question in questions:
        selected_choice = request.POST.get(f'question_{question.id}', None)
        if selected_choice == question.correct_choice:
            score += 1

    # Lấy thời gian hiện tại theo múi giờ UTC
    current_time_utc = timezone.now()

    # Chuyển múi giờ sang múi giờ Việt Nam
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = current_time_utc.astimezone(vn_tz)

    # Cập nhật thời gian kết thúc của bài kiểm tra
    test.end_time = current_time_vn
    test.save()

    return render(request, 'test_result.html', {'test': test, 'score': score, 'current_time_vn': current_time_vn})
