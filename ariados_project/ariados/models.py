from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField


class Trainer(models.Model):
    name = models.CharField(unique=True, max_length=80)
    TEAM_CHOICES = (
        ('INSTINCT', 'INSTINCT'),
        ('MYSTIC', 'MYSTIC'),
        ('VALOR', 'VALOR'),
    )
    team = models.CharField(choices=TEAM_CHOICES, max_length=20)
    home_location = models.CharField(max_length=100)
    current_location = GeopositionField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'trainer'


class FriendRequest(models.Model):
    trainer_from = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer_from')
    trainer_to = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer_to')
    STATUS_CHOICES = (
        ('SENT', 'SENT'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REJECTED', 'REJECTED'),
        ('IGNORED', 'IGNORED'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    class Meta:
        managed = True
        db_table = 'friend_request'
        unique_together = ('trainer_from', 'trainer_to')


class IsFriendOf(models.Model):
    trainer1 = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer1')
    trainer2 = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer2')

    class Meta:
        managed = True
        db_table = 'is_friend_of'
        unique_together = ('trainer1', 'trainer2')


class Event(models.Model):
    title = models.CharField(max_length=100, default='', blank=False, null=False)
    description = models.CharField(max_length=100, default='', null=False)
    location = GeopositionField()
    start_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    end_date = models.DateTimeField(default=datetime.now, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'event'


class Attends(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'attends'


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    VIEWERS_CHOICES = (
        ('INSTINCT', 'INSTINCT'),
        ('MYSTIC', 'MYSTIC'),
        ('VALOR', 'VALOR'),
        ('GLOBAL', 'GLOBAL'),
    )
    viewers = models.CharField(choices=VIEWERS_CHOICES, max_length=20)
    STATUS_CHOICES = (
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    creator = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=False)
    # Parent Post
    answer_of = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    last_update = models.DateTimeField(default=datetime.now, blank=True, null=False)
    likes = models.IntegerField(default=0, null=False, blank=False)
    dislikes = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'post'


class Vote(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('LIKE', 'LIKE'),
        ('DISLIKE', 'DISLIKE'),
    )

    class Meta:
        managed = True
        db_table = 'vote'


# Clases de autenticación de los módulos de Django-auth y Django-admin
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
