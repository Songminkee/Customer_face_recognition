from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from accounts.models import User
from registration.models import Borrower
from history.models import TrackingLog
from django.conf import settings
import glob
import os

class HistoryView(TemplateView):
    def get(self,request,*args, **kwargs):
        uid = User.objects.get(username=request.user).uid
        borrowers = Borrower.objects.filter(userborrower__uid=uid)
        return render(request,'history/history.html',{'borrowers':borrowers})

class HistoryViewDetail(TemplateView):
    def get(self,request,bid,*args, **kwargs): 
        uid = User.objects.get(username=request.user).uid
        borrowers = Borrower.objects.filter(userborrower__uid=uid)
        logs = TrackingLog.objects.filter(borrowertrackinglog__bid=bid)
        
        for log in logs.values():
            if not os.access(os.path.join(settings.STATIC_ROOT,log['video_path']),os.R_OK):
                TrackingLog.objects.get(video_path=log['video_path']).delete()

        return render(request,'history/history_detail.html',{'logs':logs,'bid':bid,'borrowers':borrowers})

class HistoryVideo(TemplateView):
    def get(self,request,bid,tid,*args, **kwargs):
        uid = User.objects.get(username=request.user).uid
        borrowers = Borrower.objects.filter(userborrower__uid=uid)
        log = TrackingLog.objects.get(tid=tid)
        logs = TrackingLog.objects.filter(borrowertrackinglog__bid=bid)
        return render(request,'history/history_video.html',{'log':log,'bid':bid,'borrowers':borrowers,'logs':logs})