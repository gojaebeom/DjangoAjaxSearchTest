from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Post
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers

# 홈화면
def home(request):
    return render(request, 'home.html')


@csrf_exempt
def search(request):
    print('hello')
    data  = json.loads(request.body)
    jsondata = data.get('data', None)

    post_list = []
    if jsondata is not '': 
        # [컬럼명]__contains = '%s%'
        # [컬럼명]__startswith = 's%'
        # [컬럼명]__endswith = '%s'
        post_list = Post.objects.filter(title__startswith=jsondata)
        
    json_list = serializers.serialize('json', post_list)    
    return HttpResponse(json_list, content_type="application/json")
        
