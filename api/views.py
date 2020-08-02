from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from api.models import *
from django.core import serializers
from django.shortcuts import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
import json
import math
import matplotlib.pyplot as plt
import cv2
import os
from api.utils import *
import random,operator
# Create your views here.

blockchain = Blockchain()
blockchain.create_genesis_block()

@require_http_methods(['POST'])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        rollno = body['rollno']
        password = body['password']
        usr = Student.objects.filter(rollno=rollno)
        if len(usr)!=0:
            if usr.password == password:
                data['status']='Login Successfull'
            else:
                data['status'] = 'Invalid'
        else:
            data['status']='Student not registered'
    return JsonResponse(data)

@require_http_methods(['POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        rollno = body['rollno']
        webmail = body['webmail']
        password = body['password']
        user = Student.objects.filter(rollno=rollno)
        if len(user)==0:
            user.save()
            data['status']='Successfully Registered'
        else:
            data['status'] = 'Student already registered'
    return JsonResponse(data)

@require_http_methods(['POST'])
@csrf_exempt
def transact(request):
    if request.method == 'POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        print(body)
        sendid = int(body['sender'])
        s = Student.objects.get(user_id=sendid)
        recid = int(body['receiver'])
        r = Student.objects.get(user_id=recid)
        amount = int(body['amount'])
        title = body['title']
        if r.is_shop==1:
            trans = Transaction(sender=s,receiver=r,amount=amount,title=title,is_shop=1)
        else:
            trans = Transaction(sender=s,receiver=r,title=title,amount=amount)
        
        r.balance += amount
        r.save()
        s.balance -= amount
        s.save()

        # add to blockchain
        # blockchain.add_new_transaction(trans)
        # #blockchain.mine()
        # chain_data=[]
        # for b in blockchain.chain:
        #     chain_data.append(b.__dict__)
        # dict1 = {
        #     'length' : len(chain_data),
        #     'chain' : chain_data
        # }
        # print(dict1)
        trans.save()
        data['data']='success'
        data['status']='200'
    return JsonResponse(data)


@require_http_methods(['GET'])
@csrf_exempt
def get_transaction(request):
    if request.method =='GET':
        data={
            'data':[],
            'status':''
        }
        user1 = request.GET.get('user1')
        user2 = request.GET.get('user2')
        u = Student.objects.get(user_id=int(user1))
        trans1 = Transaction.objects.filter(sender=user1,receiver=user2)
        trans2 = Transaction.objects.filter(sender=user2,receiver=user1)
        trans=[]
        for t in trans1:
            trans.append(t)
        for t in trans2:
            trans.append(t)

        trans=sorted(trans, key=operator.attrgetter('time_stamp'))
        
        for t in trans:
            tmp={
            'sname':'',
            's_rollno':'',
            'rname':'',
            'r_rollno':'',
            'amount':'',
            'date':'',
            'type':''
            }
            tmp['sname']=t.sender.username
            tmp['s_rollno']=t.sender.rollno
            tmp['rname']=t.receiver.username
            tmp['r_rollno']=t.receiver.rollno
            date = t.time_stamp.strftime('%y-%m-%d %a %H:%M:%S')
            tmp['date'] = date
            tmp['amount'] = t.amount
            if(u.username==tmp['sname']):
                tmp['type']='sent'
            else:
                tmp['type']='received'
            
            data['data'].append(tmp)

    return JsonResponse(data)

@require_http_methods(['GET'])
@csrf_exempt
def get_friends(request):
    if request.method == 'GET':
        my_id = request.GET.get('user_id')
        print(my_id)
        friends = Friend.objects.filter(my_id=my_id)
        result = {
            'data':[]
        }
        tmp={
            'fid':'',
            'fname':'',
            'frollno':''
        }
        for f in friends:
            tmp['fid']=f.friend_id.user_id
            tmp['fname']=f.friend_id.username
            tmp['frollno']=f.friend_id.rollno
            result['data'].append(tmp)
            tmp={
            'fid':'',
            'fname':'',
            'frollno':''
            }
        
        return JsonResponse(result)

@require_http_methods(['GET'])
@csrf_exempt
def get_recent_shop(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        print(user_id)
        s = Student.objects.get(user_id=int(user_id))
        trans = Transaction.objects.filter(sender=s,is_shop=1).order_by("time_stamp")
        
        new_trans=[]
        c=0
        for t in trans:
            c=0
            for tnew in new_trans:
                if t.receiver.user_id==tnew.receiver.user_id:
                    c=1
                    break
            if c==0:
                new_trans.append(t)
        
        result = {
            'data':[]
        }
        
        
        for t in new_trans:
            tmp={
                'shop_name':'',
                'shop_id':''
            }

            tmp['shop_name']=t.receiver.username
            tmp['shop_id']=t.receiver.user_id

            result['data'].append(tmp)

        return JsonResponse(result)

@require_http_methods(['GET'])
@csrf_exempt
def get_recent_student(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        s = Student.objects.get(user_id=user_id)
        trans = Transaction.objects.filter(sender=s,is_shop=0).order_by("time_stamp")
        
        new_trans=[]
        c=0
        for t in trans:
            c=0
            for tnew in new_trans:
                if t.receiver.user_id==tnew.receiver.user_id:
                    c=1
                    break
            if c==0:
                new_trans.append(t)

        result = {
            'data':[]
        }
        for t in new_trans:
            tmp={
                'student_name':'',
                'student_id':''
            }

            tmp['student_name']=t.receiver.username
            tmp['student_id']=t.receiver.user_id

            result['data'].append(tmp)

        return JsonResponse(result)

@require_http_methods(['GET'])
@csrf_exempt
def get_balance(request):
    if request.method=='GET':
        user_id = request.GET.get('user_id')

        user = Student.objects.get(user_id=user_id)

        result = {
            'data':0
        }

        result['data']=user.balance

        return JsonResponse(result)

@require_http_methods(['POST'])
@csrf_exempt
def add_friend(request):
    if request.method=='POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        print(body)
        user_id = int(body['user_id'])
        his_rollno = int(body['roll_no'])

        f = Student.objects.get(rollno=his_rollno)
        u = Student.objects.get(user_id=user_id)

        friends = Friend(friend_id=f,my_id=u)
        friends.save()

        data['data']='success'
        data['status']='200'

        return JsonResponse(data)
    
@require_http_methods(['POST'])
@csrf_exempt
def put_request(request):
    if request.method=='POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        print(body)
        from_userid=int(body['from'])
        to_userid = int(body['to'])
        amount = int(body['amount'])
        r = Reqmoney(from_req=f,to_req=t,amount=amount,status='pending')
        r.save()
        data['data']='request sent'
        data['status']='200'

        return JsonResponse(data)

@require_http_methods(['POST'])
@csrf_exempt
def accept_req(request):
    if request.method=='POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        print(body)
        from_userid=int(body['from'])
        to_userid = int(body['to'])
        r = Reqmoney.objects.get(from_req=f,to_req=t,status='pending')
        r.status = 'accepted'
        r.save()
        r.from_req.balance += r.amount
        r.to_req.balance -= r.amount

        r.from_req.save()
        r.to_req.save()

        data['data']='accepted'
        data['status']='200'

        return JsonResponse(data)



@require_http_methods(['GET'])
@csrf_exempt
def fest(request):
    if request.method == 'GET':
        fest = Fest.objects.all()

        result= {
            'data':[]
        }

        for f in fest:
            temp= {
            'fest_id': '',
            'fest_name' : '',
            'fest_desc' : '',
            'live' : ''
        }
        temp['fest_id'] = f.fest_id
        temp['fest_name'] = f.fest_name
        temp['fest_desc'] = f.fest_desc
        temp['live'] = f.live

        result['data'].append(temp)

    return JsonResponse(result)


@require_http_methods(['GET'])
@csrf_exempt
def stall(request):
    if request.method == 'GET':
        id = request.GET.get('fest_id')
        stall = Stalls.objects.filter(fest_id = id)
            
        result= {
            'data':[]
        }

        for s in stall:
            temp= {
            'stall_id': '',
            'fest' : '',
            'stall_name' : '',
            'amount' : 'live',
            'live' : ''
        }
        temp['stall_id'] = s.stall_id
        temp['fest'] = s.fest
        temp['stall_name'] = s.stall_name
        temp['amount'] = s.amount
        temp['live'] = s.live

        result['data'].append(temp)
        
    return JsonResponse(temp)