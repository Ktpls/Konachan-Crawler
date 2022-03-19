
from django.http import HttpResponse
from django.shortcuts import render_to_response
 
# 表单
def default(request):
    return render_to_response('default.html')
