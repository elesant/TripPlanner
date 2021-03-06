from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.utils import timezone
from core.constants import EVENT_CATEGORY


class CustomUserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True, is_superuser=False, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('e-mail address', max_length=200, unique=True, db_index=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    tz_offset = models.IntegerField(default=0)
    facebook_id = models.CharField(max_length=200, blank=True, null=True)
    display_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_plans(self):
        plans = [collaboration.plan for collaboration in Collaboration.objects.filter(collaborator=self)]
        return plans

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'table_user'
        verbose_name = 'User'


class Plan(models.Model):

    title = models.CharField(max_length=200)
    collaborator = models.ManyToManyField(User, through='Collaboration')
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def add_collaborator(self, user):
        new_collaboration = Collaboration()
        new_collaboration.collaborator = user
        new_collaboration.plan = self
        new_collaboration.save()
        return new_collaboration

    def get_collaborators(self):
        collaborators = [collaboration.collaborator for collaboration in Collaboration.objects.filter(plan=self)]
        return collaborators

    def get_events(self):
        events = [event for event in Event.objects.filter(plan=self).order_by('order')]
        return events

    class Meta:
        db_table = 'table_plan'


class Collaboration(models.Model):

    collaborator = models.ForeignKey(User, related_name='%(class)s_collaborator')
    plan = models.ForeignKey(Plan, related_name='%(class)s_plan')
    time_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s <-> %s' % (self.collaborator.email, self.plan)

    class Meta:
        db_table = 'table_collaboration'
        unique_together = ('collaborator', 'plan')


class Event(models.Model):

    header = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=EVENT_CATEGORY)
    plan = models.ForeignKey(Plan)
    order = models.PositiveIntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.header

    class Meta:
        db_table = 'table_event'
