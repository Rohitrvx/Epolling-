from django.db import models
from django.db.models.aggregates import Count
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.contrib.auth.models import User

class Contact(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=30)
    desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from ' + self.name

class Candidate(models.Model):
    sno = models.AutoField(primary_key= True)
    name = models.CharField(max_length=50,default="")
    ward = models.CharField(max_length=15,default="")
    city = models.CharField(max_length=15,default="")
    party = models.CharField(max_length=10,default="")
    criminal = models.BooleanField(default=False)
    declare = models.BooleanField(default=False)
    vcount = models.IntegerField(default=0)
    verifyimg = models.FileField(upload_to='images/',default=False)

    def __str__(self):
        return  '{},{}'.format(self.name,self.party)

class extenduser(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,default="")
    phone = models.CharField(max_length=13,default="")
    age = models.IntegerField(default=0)
    aadhar = models.CharField(max_length=13,default="")
    voterid = models.CharField(max_length=20,default="")
    ward = models.CharField(max_length=10,default="")
    voted = models.BooleanField(default=False)
    show_results = models.BooleanField(default=False)
    otp = models.CharField(max_length=4,default="")
    # aadharphoto = models.FileField(upload_to='images/', default=False)

    def __str__(self):
        return self.user.username

class aadhar(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile = models.FileField(upload_to='', default=False)
    added = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username