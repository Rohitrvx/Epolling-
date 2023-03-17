import requests
import json
from django.shortcuts import render,HttpResponse,redirect
from requests.api import request
from .models import Contact,Candidate,extenduser,aadhar
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path

# def facedect(loc):
#         cam = cv2.VideoCapture(0)   
#         s, img = cam.read()
#         if s:   
#              return True   
#                 # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                 # # BASE_DIR = Path(__file__).resolve().parent.parent
#                 # # MEDIA_ROOT =os.path.join(BASE_DIR,'media/images')
                
#                 # loc=str(BASE_DIR) + loc
#                 # face_1_image = face_recognition.load_image_file(loc)
#                 # face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

#                 # #

#                 # small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

#                 # rgb_small_frame = small_frame[:, :, ::-1]

#                 # face_locations = face_recognition.face_locations(rgb_small_frame)
#                 # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#                 # check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                

#                 # print(check)
#                 # if check[0]:
            

#                 # else :
#                         # return False

def index(request):
    # datas = extenduser.objects.filter(user = request.user)
    return render(request,'polling/index.html')


def loginhandle(request):
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        clientKey = request.POST['g-recaptcha-response']
        secretKey = '6LdFN5gbAAAAAMFBK4bF0sAWXHh-gw3I_HmOyQzN'
        captchadata = {
            'secret': secretKey,
            'response': clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        user = authenticate(username=username,password=password)
        if user is not None:
            if verify:
                login(request, user)
                messages.success(request,"Logged in")
                logged_user = aadhar.objects.filter(user=request.user).first()
                if logged_user.added:
                    return redirect('index')
                else:
                    return redirect('aadhar')
            else:
                messages.error(request,"Please verify!")
                return redirect('login')
        else:
            messages.error(request,'Wrong credentials')
            return redirect('login')
        

    return render(request,'polling/index.html')

def register(request):
    usernamed = []
    aadhard = []
    voterd = []
    data = extenduser.objects.all()
    for i in data:
        usernamed.append(i.user.username)
        aadhard.append(i.aadhar)
        voterd.append(i.voterid)

    if request.method == "POST":
        
        username1 = request.POST['username1']
        # email1 = request.POST['email1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        phone = request.POST['phone']
        aadhar1 = request.POST['aadhar']
        voterid = request.POST['voterid']
        ward = request.POST['ward']
        pswd = request.POST['pswd']
        repswd = request.POST['repswd']
        clientKey = request.POST['g-recaptcha-response']
        secretKey = '6LdFN5gbAAAAAMFBK4bF0sAWXHh-gw3I_HmOyQzN'
        captchadata = {
            'secret': secretKey,
            'response': clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        if len(username1)<7:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('index')

        if not username1.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('index')
        if int(age)<18:
            messages.error(request,"You are not Eligible Age:Error ")
            return redirect('index')
        if username1 in usernamed:
            messages.error(request,'Username is already taken')
            return redirect('register')
        if aadhar in aadhard:
            messages.error(request,'Aadhar is already registered')
            return redirect('register')
        if voterid in voterd:
            messages.error(request,'Voterid is already registered')
            return redirect('register')
        if (pswd!=repswd):
             messages.error(request, " Passwords do not match")
             return redirect('index')
        if len(aadhar1) != 12:
            messages.error(request,'Invalid Aadhar (Aadhar should be of 12 digits)')
            return redirect('register')
        if len(voterid) != 10:
            messages.error(request,'Invalid Voter ID')
            return redirect('register')
        if len(phone)>10 or len(phone)<10:
            messages.error(request,'Invalid phone number')
            return redirect('register')
        if verify:
            myuser = User.objects.create_user(username=username1,password=pswd)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            extend = extenduser(user=myuser,age=age,phone=phone,aadhar=aadhar1,voterid=voterid,ward=ward)
            a_user = aadhar(user = myuser)
            a_user.save()
            extend.save()
            messages.success(request, 'User successfully created')
            return redirect('index')
        else:
                messages.error(request,"Please verify!")
                return redirect('register')

    return render(request,'polling/index.html')

def logouthandle(request):
        logout(request)
        messages.success(request,'Successfull logged out')
        return redirect('login')

@login_required(login_url='error')
def results(request):
    data_C = Candidate.objects.filter(party='Congress')
    data_B = Candidate.objects.filter(party='BJP')
    data = extenduser.objects.filter(user=request.user).first()
    ward = data.ward
    candidate_l = Candidate.objects.filter(ward=ward).all()
    return render(request,'polling/result.html',{'data_C':data_C , 'data_B':data_B, 'data':candidate_l, 'U_data':data})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<2 :
            messages.error(request,'Please fill the form Correctly!')
        else:
            contact = Contact(name=name,email=email,phone=phone,desc=desc)
            contact.save()
            messages.success(request, 'Successfully Sent')
    return render(request,'polling/contact.html')

@login_required(login_url='error')    
def votingpanel(request):
    # if request.method == 'POST':
        data = extenduser.objects.filter(user=request.user).first()
        ward = data.ward
        cand_list = Candidate.objects.filter(ward=ward).all()

        return render(request,'polling/votingsection.html',{'cand_list':cand_list, 'data': data})

    # return render(request,'polling/votingsection.html')

def candidate(request):
    if request.method == 'POST':
        name = request.POST['name']
        party = request.POST['party']
        ward = request.POST['ward']
        city = request.POST['city']
        verifyimg=request.FILES['document']
        fs=FileSystemStorage()
        verifyimg=fs.save(verifyimg.name,verifyimg)
        url=fs.url(verifyimg)
        try:
            case = request.POST['case']
        except:
            case = False
        try:
            declare = request.POST['declare']
        except:
            declare = False
        if (case == 'on'):
            messages.error(request,'You are not Eligible')
            return redirect('candidate')
        elif (declare == False):
             messages.error(request,'You must agree to the terms!')
        else:
            cand = Candidate(name=name,party=party,ward=ward,city=city,criminal=False,declare=True,verifyimg=verifyimg )
            cand.save()
            # print(cand)
            messages.success(request,'Your application is under Verification')
            return redirect('candidate')
    return render(request,'polling/candidate.html')

@login_required(login_url='error')
def aadharverify(request):
    if request.method == 'POST':
        data = extenduser.objects.filter(user=request.user).first()
        mobile = data.phone
        print(mobile)
        otpg = str(random.randint(1000,9999))
        data.otp = otpg
        data.save()
        aadharv = request.POST['aadharv']
        voterv = request.POST['voterv']
        data = extenduser.objects.filter(user=request.user).first()
        logged_user = aadhar.objects.filter(user=request.user).first()
        verification_check = client.verify.v2.services(verify_sid) \
                                            .verification_checks \
                            .create(to=mobile, code=otp_code)
        verify_sid = "VA0efa3562ba0924b01ed1542285ba9eeb"
        if logged_user.added:
            if (aadharv == data.aadhar) and (voterv == data.voterid):
                account_sid = 'ACa687dedf4aef828acb11843922795d14'
                auth_token = 'f6b60d371e026535614ae3921cb09989'
                client = Client(account_sid, auth_token)

                message = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=mobile, channel="sms")
                                        
                print("Successfully sent")
                messages.success(request,'A OTP has been sent to your registered mobile number.')
                return redirect('OTP')
            else:
                messages.error(request,'Invalid Aadhar or Voter ID Details, please try again')
                return redirect('verify')
        else:
            messages.error(request,'unauthorised user')
            return redirect('verify')


    return render(request,'polling/aadharverification.html')

@login_required(login_url='error')
def otp(request):
    data = extenduser.objects.filter(user=request.user).first()
    otpf = data.otp
    if request.method == 'POST':
        otpv = request.POST['OTP']
        if (otpf == otpv):
            messages.success(request,'Welcome to the Voting Section')
            return redirect('voting')
        else:
            messages.error(request,'Wrong OTP')
            return redirect('verify') 

    return render(request,'polling/aadharverification.html')

def vote(request,sno):
    is_voted = extenduser.objects.filter(user=request.user).first()
    if (is_voted.voted == True):
        messages.error(request,'No Cheating, You have already VOTED!')
        return redirect('index')
    else:
        count = Candidate.objects.filter(sno=sno).first()
        count.vcount = count.vcount + 1
        count.save()
        is_voted.voted = True
        is_voted.save()
        messages.success(request,'Your response has been recorded')
        return redirect('voting')
def show_results(request):
    if request.method == 'POST':
        try:
            globally = request.POST['globally']
        except:
            globally = False
        print(globally)
        if globally == 'on':
            voter_list = extenduser.objects.all()
            for voter in voter_list:
                if voter.show_results == False:
                    voter.show_results = True
                    voter.save()
            messages.success(request,'Changes applied successfully, Results are now Online')
            return redirect('index')
        elif globally == False:
            voter_list = extenduser.objects.all()
            for voter in voter_list:
                if voter.show_results == True:
                    voter.show_results = False
                    voter.save()
            messages.success(request,'Changes applied successfully, Results are now Offline')
            return redirect('index')

    return render(request,'polling/admin.html')    

def loginmsg(request):
    return render(request,'polling/login1.html')
def send_otp():
    data = extenduser.objects.filter(user=request.user).first()
    mobile = data.phone
    print(mobile)
    otpg = str(random.randint(1000,9999))

    account_sid = 'ACc89a23c638baa619ace57dad5e731244'
    auth_token = '1e530ff69a404936f655bbf8ff2e733b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body='Hello there, your otp is:'+otpg,
                                from_='+12315382390',
                                to='+91'+mobile
                            )
    print("Successfully sent")
@login_required(login_url='error')
def aadharupload(request):
    aadhar_added = aadhar.objects.get(user=request.user)
    if request.method == 'POST':
        aadharphoto=request.FILES['aadharphoto']
        fs=FileSystemStorage()
        aadharphoto=fs.save(aadharphoto.name,aadharphoto)
        url=fs.url(aadharphoto)
        # extend = aadhar(user = request.user,added=True,profile=aadharphoto)
        aadhar_added.added = True
        aadhar_added.profile = aadharphoto
        aadhar_added.save()
        messages.success(request, 'successfully uploaded')
        return redirect('index')
    return render(request,'polling/aadharverify.html')
# logged_user = aadhar.objects.filter(user=request.user).first()
# print(logged_user.profile.url)