## 시작하기
__venv 설치 및 실행 , django 프로젝트 생성 단계는 건너뛰고 시작합니다.__


먼저 테스트를 진행하기 위한 post 앱을 만들겠습니다.
```python
python manage.py startapp post
```


만든 post 앱을 config 의 `settings.py` 에 알려주도록 해요.

```python
# config/settings.py
...
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
# post 앱 등록
'post',
]
```

이제 데이터를 조회할 데이터베이스를 만들어봅시다.

```python
# post/models.py 
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    addr = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
```


그리고 다음 명령어로 테이블 등록을 진행하겠습니다

```
python manage.py makemigrations
python manage.py migrate
```


이번 예제에서는 post를 직접 crud 하지 않을겁니다. admin 사이트를 이용하여 정당히 게시물을 생성하고   
빠르게 ajax 기능 구현을 살펴보죠. 

먼저 admin 사이트를 이용하기 위해선 admin 계정을 만들어 주는 것 이 중요합니다.

```
python manage.py createsuperuser 
```

명령어 입력후 username은 원하는 이름으로 등록, 이메일은 생략 가능, 페스워드는 암호가 짧으면 경고하지만 yes로 무시해줍니다.
admin 계정은 만들었지만 정작 admin 사이트에서 post 테이블을 볼 수가 없습니다. 그 이유는 admin 사이트에서 post 테이블을 
관리하겠다고 장고에게 알려주어야 하기 때문이지요. `post/admin.py` 파일에 다음 코드를 작성해주세요

```python
# post/admin.py 

from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```


그리고 `python manage.py runserver` 명령어로 서버를 열고 [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) 주소로 접속, 로그인해주세요. 그리고 다음 이미지와 같이 테이블의 레코드를 
3~4 개 정도만 만들어주세요.

![이미지](https://github.com/gojaebeom/django-ajax-search-test/blob/main/images/20201221_165835.png?raw=true)
![이미지](https://github.com/gojaebeom/django-ajax-search-test/blob/main/images/20201221_165922.png?raw=true)
![이미지](https://github.com/gojaebeom/django-ajax-search-test/blob/main/images/20201221_170003.png?raw=true)

이제 테이블의 테스트할 데이터들은 생성이 되었고, 자동완성 기능을 사용할 html 을 보여주는 view(controller)와  ajax 자동완성 요청을 받을 view(controller) 가 있으면 될것 같습니다. 
그리고 해당 views를 어떤 요청이 올 때 실행할 건지 설정하는 urls(router) 도 정의해보죠. 


```python
# post/views.py

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
```
<br>

```python
# config/urls.py 

from django.contrib import admin
from django.urls import path
from post import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('search', views.search),
]

```

이제 보여줄 html을 작성하면 될것 같습니다. 하지만 그전에 html 파일의 기본 경로를 장고에게 알려줘야합니다. `settings.py` 파일에 다음과 같은 설정을 해주세요.


```python
# 상단에 선언
import os

...
# 템플릿 배열을 찾아 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 이부분 설정
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

```

이제 프로젝트 최상위 경로에서 (manage.py 가 있는 위치) `templates` 이름의 폴더를 만들어 주세요. 그리고 그 위치에 home.html 파일을 만들어줍니다. 양식은 다음과 같아요.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Sniglet&display=swap" rel="stylesheet">
    <title>Document</title>
</head>
<style>
    html,body{height:100%;margin:0;}
    body{display:flex;flex-direction: column; justify-content:flex-start;align-items:center;}
    .text-con{font-size:50px;font-family: 'Sniglet', cursive;margin-top:200px;margin-bottom:20px;}
    .search-con{display:flex;flex-direction:column;width:320px;border:1px solid #BDBDBD;border-radius:30px;padding:10px;}
    .search-con input{border:none;}
    .search-con input:focus {outline:none;}
    .search-list{display:none;flex-direction:column;width:300px;border:1px solid #BDBDBD;border-radius:10px;padding:10px;}
</style>
<body>
    <div class="text-con">
        GojaeGle
    </div>
    <div class="search-con">
        <input type="text" id="search_input" placeholder="찾는 게시물을 입력하세요" autocomplete=off>
    </div>
    <div class="search-list" id="search-list">

    </div>
    

    <script> 
        search_input = document.getElementById('search_input')
        search_list = document.getElementById('search-list')
        
        search_input.onkeyup = async () => 
        {
            let json = await fetch('/search', {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'cors', // no-cors, cors, *same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                    'Content-Type': 'application/json',
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                redirect: 'follow', // manual, *follow, error
                referrer: 'no-referrer', // no-referrer, *client
                body: JSON.stringify({'data':search_input.value}), // body data type must match "Content-Type" header
            }).then(res=>res.json())

            
            search_list.innerHTML = ''

            if(search_input.value != '' && json.length != 0)
                search_list.style.display='flex'
            else
                search_list.style.display='none'

            for(el of json)
            {
                console.log(el)
                search_list.innerHTML += 
                `
                <span>${el.fields.title}</span>
                `
            }
        }
    </script>
</body>
</html>
```

html 파일에 위와같이 css, js 파일을 하나로 합치는 것은 좋지 않지만 빠른 예제를 만들기 위해 일단은 저렇게 작성하였습니다.


```js
// 자바스크립트 코드만 따로 추출
search_input = document.getElementById('search_input')
        search_list = document.getElementById('search-list')
        
        search_input.onkeyup = async () => 
        {
            let json = await fetch('/search', {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'cors', // no-cors, cors, *same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                    'Content-Type': 'application/json',
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                redirect: 'follow', // manual, *follow, error
                referrer: 'no-referrer', // no-referrer, *client
                body: JSON.stringify({'data':search_input.value}), // body data type must match "Content-Type" header
            }).then(res=>res.json())

            
            search_list.innerHTML = ''

            if(search_input.value != '' && json.length != 0)
                search_list.style.display='flex'
            else
                search_list.style.display='none'

            for(el of json)
            {
                console.log(el)
                search_list.innerHTML += 
                `
                <span>${el.fields.title}</span>
                `
            }
        }
```
