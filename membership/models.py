from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SocialGroup(models.Model):
    creator = models.ForeignKey(User, related_name='manager')
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='members', through = 'Membership')
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Invitation(models.Model):
    #manager = models.ForeignKey(User, related_name='manager')
    invite = models.ForeignKey(User, related_name='invite')
    socialgroup = models.ForeignKey(SocialGroup, related_name='socialgroup', default='1')
    sent_at = models.DateTimeField(auto_now_add=True)
    RES_TYPES = (('accept', 'accept'), ('reject', 'reject'),)
    response = models.CharField(max_length=15, choices=RES_TYPES)
    responsed_at = models.DateTimeField(null=True)

#    class Meta:                      # does not work
#        unique_together = ('invite', 'socialgroup',)

class Membership(models.Model):
    sgroup = models.ForeignKey(SocialGroup, on_delete=models.CASCADE, related_name='sgroup' )
    member = models.ForeignKey(User, related_name='member')
    role = models.CharField(max_length=30)
    joined_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.ForeignKey(User, related_name='user')
    toUser = models.ManyToManyField(User, related_name='toUser')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)            #models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    #MEG_TYPES = (('invitation', 'invitation'), ('regular', 'regular'),)
    #type = models.CharField(max_length=15, choices=MEG_TYPES, default='regular')
    #responsed_at = models.DateTimeField(null=True)

class Chat(models.Model):
    sgroup = models.ForeignKey(SocialGroup, related_name='chats')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}