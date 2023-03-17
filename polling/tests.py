from django.test import TestCase
import requests
import json
from django.shortcuts import render,HttpResponse,redirect
from requests.api import request
from .models import Contact,Candidate,extenduser
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from django.core.files.storage import FileSystemStorage

data = extenduser.objects.filter(user=request.user).first()