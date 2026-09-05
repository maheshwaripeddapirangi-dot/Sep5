from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .serializers import Userserializer
from django.views.decorators.csrf import csrf_exempt
import bcrypt
import json
from .passwords import password_hash
from .models import User
def home_page(req):
    print(req.COOKIES)
    if req.COOKIES.get('is_logged_in'):
        return JsonResponse({'status':200,'Message':'Hi what can I do for you!!!'})
    else:
        return JsonResponse({'status':200,'Message':'Please check you do not have account!!!'})
    return JsonResponse({
        'status':"Created project home page"
    })

@csrf_exempt
def register(req):
    print(req.body)
    data=json.loads(req.body)
    u1=Userserializer(data=data)
    if u1.is_valid():
        print(u1.validated_data)
        # sent_password=u1.validated_data['password'].encode('utf-8')
        # salt=bcrypt.gensalt(rounds=12)
        # hashed_password=bcrypt.hashpw(sent_password,salt)
        #u1.validated_data['password']=hashed_password.decode('utf-8')
        
        u1.validated_data['password']=password_hash(u1.validated_data['password']) 
        u1.save()
        return JsonResponse({'status':'user created','data':data}) 
    else:
        return JsonResponse(u1.errors)

@csrf_exempt
def login(req):
    if req.COOKIES.get('is_logged_in')=='true':
        user_name=req.COOKIES.get('user_name','User')
        message='You already logged in ' + user_name
        return JsonResponse({'status':200,'message':message})
    data=json.loads(req.body)
    try:
        u1=User.objects.get(user_name=data['user_name'])
        print(u1.user_name)
        print(u1.password)
    except Exception as e:
        return JsonResponse({'error':'User not found'})
    entered_password=data['password']
    database_password=u1.password
    if bcrypt.checkpw(entered_password.encode('utf-8'),database_password.encode('utf-8')):
        res=JsonResponse({'status':200,'message':'Login successfull!!!'})
        res.set_cookie(
            key='user_name',
            value=data['user_name'],
            max_age=3600
        )
        res.set_cookie(
                    key='is_logged_in',
                    value='true',
                    max_age=3600
                )
        return res
    return JsonResponse({'status':'Login failed'})
@csrf_exempt
def update(req):
    data=json.loads(req.body)
    try:
        u1=User.objects.get(user_name=data.get('user_name'))
    except Exception as e:
        return JsonResponse({'error':'User not found'})
    sent_password=data.get('password').encode('utf-8')
    salt=bcrypt.gensalt(rounds=12)
    hashed_password=bcrypt.hashpw(sent_password,salt)
    data['password']=hashed_password.decode('utf-8')
    u1=Userserializer(u1,data=data,partial=True)
    if u1.is_valid():
        u1.save()
        return JsonResponse({'status':'Password changed'})
    return JsonResponse(u1.errors)
@csrf_exempt
def logout(req):
    try:
        user_name=req.COOKIES.get('user_name','User')
        message='You successfully logged out '+ user_name
        res=JsonResponse({'status':'Logged out','message':message})
        res.delete_cookie('user_name')
        res.delete_cookie('is_logged_in')
        return res
    except:
        return JsonResponse({'Message':'Logout failed'})
def set_cookie(req):
    res=HttpResponse("Cookie set...")
    res.set_cookie(
        key="is_logged_in",
        value="dark",
        max_age= 10,
    )
    return res


# Create your views here.
