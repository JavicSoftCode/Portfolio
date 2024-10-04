# Generated by Django 5.1.1 on 2024-10-04 14:36

import BackEnd.Apps.accounts.utils
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birth_day', models.DateField(validators=[BackEnd.Apps.accounts.utils.ValidatorUser.validate_age], verbose_name='Fecha Nacimiento')),
                ('first_name', models.CharField(max_length=30, validators=[BackEnd.Apps.accounts.utils.ValidatorUser.validate_full_name], verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=30, validators=[BackEnd.Apps.accounts.utils.ValidatorUser.validate_full_name], verbose_name='Apellido')),
                ('username', models.CharField(max_length=20, unique=True, validators=[BackEnd.Apps.accounts.utils.ValidatorUser.validate_username], verbose_name='Usuario')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[BackEnd.Apps.accounts.utils.ValidatorUser.validate_email], verbose_name='Correo Electrónico')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Super Usuario',
                'verbose_name_plural': 'Super Usuarios',
            },
            bases=('accounts.customuser',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario Normal',
                'verbose_name_plural': 'Usuarios Normales',
            },
            bases=('accounts.customuser',),
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('roles', models.ManyToManyField(blank=True, to='accounts.role')),
            ],
            options={
                'verbose_name': 'Usuario Administrador',
                'verbose_name_plural': 'Usuarios Administradores',
            },
            bases=('accounts.customuser',),
        ),
    ]
