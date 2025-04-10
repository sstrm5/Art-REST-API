# Generated by Django 5.1.3 on 2024-12-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0005_question_picture_test_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="completed_tests",
            field=models.ManyToManyField(
                blank=True,
                related_name="customers",
                to="questions.test",
                verbose_name="Завершенные тесты",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="in_process",
            field=models.BooleanField(
                default=False, verbose_name="В процессе прохождения теста"
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="customers",
                verbose_name="Изображение профиля",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="role",
            field=models.CharField(
                choices=[("CUSTOMER", "Пользователь"), ("ADMIN", "Администратор")],
                default="CUSTOMER",
                max_length=50,
                verbose_name="Роль пользователя",
            ),
        ),
    ]
