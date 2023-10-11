#
#
# from ckeditor.fields import RichTextField
# from django.contrib.auth.models import User
# from django.db import models
#
# class Course(models.Model):
#     title = models.CharField(max_length=200)
#     instructor = models.CharField(max_length=100)
#     description = models.TextField()  # Thêm trường description
#     # Các trường khác của khoá học
#     def __str__(self):
#         return self.title
#
#
#
# class Lesson(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = RichTextField()
#
#     def __str__(self):
#         return self.title
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()


    # Add an image field for the lesson

    def __str__(self):
        return self.title

class Test(models.Model):
        Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)
        title = models.CharField(max_length=255)
        start_time = models.DateTimeField(null=True, blank=True)
        end_time = models.DateTimeField(null=True, blank=True)

        def __str__(self):
            return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    choice_1 = models.CharField(max_length=255, default='')
    choice_2 = models.CharField(max_length=255, default='')
    choice_3 = models.CharField(max_length=255, default='')
    choice_4 = models.CharField(max_length=255, default='')
    correct_choice = models.CharField(max_length=1, null=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    def __str__(self):
        return self.text
