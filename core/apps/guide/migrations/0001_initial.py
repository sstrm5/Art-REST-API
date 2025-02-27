# Generated by Django 5.1.2 on 2024-11-06 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0005_question_picture_test_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=255, verbose_name='Название карточки')),
                ('text', models.TextField(verbose_name='Текст карточки')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='cards', verbose_name='Изображение карточки')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.subject', verbose_name='Тема')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
