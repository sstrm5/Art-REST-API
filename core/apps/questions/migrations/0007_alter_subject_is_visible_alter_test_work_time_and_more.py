# Generated by Django 5.1.3 on 2024-12-24 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_remove_customer_completed_tests'),
        ('questions', '0006_remove_test_question_count_alter_question_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Видна ли тема в списке'),
        ),
        migrations.AlterField(
            model_name='test',
            name='work_time',
            field=models.PositiveIntegerField(blank=True, verbose_name='Время выполнения (мин)'),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.test', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сессия',
                'verbose_name_plural': 'Сессии',
            },
        ),
    ]
