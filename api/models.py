from django.db import models
from datetime import datetime

# Create your models here.

class Student(models.Model):
    user_id = models.AutoField(primary_key=True)    
    rollno = models.IntegerField(blank=False,default=0)
    username = models.CharField(max_length=180,default="")
    webmail = models.CharField(max_length=255,default="")
    password = models.CharField(max_length=255,blank=False)
    balance = models.IntegerField(default=0)
    is_shop = models.IntegerField(default=0)

class Transaction(models.Model):
    transact_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Student,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(Student,related_name='receiver',on_delete=models.CASCADE)
    amount = models.IntegerField(default =0)
    title = models.CharField(max_length=100,default="")
    is_shop = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)
    added_to_block = models.BooleanField(default=False)

    def __str__(self):
        return "'%s' transfered '%d' coins to '%s'" % (self.sender, self.amount, self.receiver, )
 
class Friend(models.Model):
    friend_id = models.ForeignKey(Student,related_name='friend',on_delete=models.CASCADE)
    my_id = models.ForeignKey(Student,related_name='me',on_delete=models.CASCADE)

class Fest(models.Model):
    fest_id = models.AutoField(primary_key=True)
    fest_name = models.CharField(max_length=255)
    fest_desc = models.CharField(max_length=255)
    live = models.IntegerField(default=0)

class Stalls(models.Model):
    stall_id = models.AutoField(primary_key=True)
    fest = models.ForeignKey(Fest, on_delete=models.CASCADE)
    stall_name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    live = models.IntegerField(default=0)

class Reqmoney(models.Model):
    from_req = models.ForeignKey(Student,related_name='from_req',on_delete=models.CASCADE)
    to_req = models.ForeignKey(Student,related_name='to_req',on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100,default="")