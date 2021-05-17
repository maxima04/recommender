# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
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


class Course(models.Model):
    course_name = models.CharField(max_length=55)

    class Meta:
        managed = False
        db_table = 'course'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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


class Likert(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    course_name = models.CharField(max_length=70)
    timestamp = models.CharField(max_length=60)
    a1 = models.CharField(max_length=255)
    a2 = models.CharField(max_length=255)
    a3 = models.CharField(max_length=255)
    a4 = models.CharField(max_length=255)
    a5 = models.CharField(max_length=255)
    a6 = models.CharField(max_length=255)
    a7 = models.CharField(max_length=255)
    a8 = models.CharField(max_length=255)
    a9 = models.CharField(max_length=255)
    a10 = models.CharField(max_length=255)
    a11 = models.CharField(max_length=255)
    a12 = models.CharField(max_length=255)
    a13 = models.CharField(max_length=255)
    a14 = models.CharField(max_length=255)
    i1 = models.CharField(max_length=255)
    i2 = models.CharField(max_length=255)
    i3 = models.CharField(max_length=255)
    ac1 = models.CharField(max_length=255)
    ac2 = models.CharField(max_length=255)
    ac3 = models.CharField(max_length=255)
    ac4 = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'likert'




class Opinion(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    e1 = models.CharField(max_length=255)
    e2 = models.CharField(max_length=255)
    e3 = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'opinion'


class Survey(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    course_name = models.CharField(max_length=55)
    timestamp = models.CharField(max_length=70)
    a1 = models.CharField(max_length=255)
    a2 = models.CharField(max_length=255)
    a3 = models.CharField(max_length=255)
    a4 = models.CharField(max_length=255)
    a5 = models.CharField(max_length=255)
    a6 = models.CharField(max_length=255)
    a7 = models.CharField(max_length=255)
    a8 = models.CharField(max_length=255)
    a9 = models.CharField(max_length=255)
    a10 = models.CharField(max_length=255)
    a11 = models.CharField(max_length=255)
    a12 = models.CharField(max_length=255)
    a13 = models.CharField(max_length=255)
    a14 = models.CharField(max_length=255)
    i1 = models.CharField(max_length=255)
    i2 = models.CharField(max_length=255)
    i3 = models.CharField(max_length=255)
    ac1 = models.CharField(max_length=255)
    ac2 = models.CharField(max_length=255)
    ac3 = models.CharField(max_length=255)
    ac4 = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'survey'


class Surveyquestions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'surveyquestions'


class User(models.Model):
    name = models.CharField(max_length=55)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=55)
    role = models.CharField(max_length=55)
    is_user = models.IntegerField()
    is_admin = models.IntegerField()
    is_itbl = models.IntegerField()
    is_ito = models.IntegerField()
    is_acad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
