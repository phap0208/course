# Generated by Django 4.1.10 on 2023-10-03 08:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_course_title_alter_lesson_title_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
