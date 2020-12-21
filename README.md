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


그리고 `python manage.py runserver` 명령어로 서버를 열고 [127.0.0.1:8000/admin](127.0.0.1:8000/admin) 주소로 접속, 로그인해주세요

![]()