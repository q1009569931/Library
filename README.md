[TOC]

# 项目要点

## 给模型增加字段

```python
'''
img就是增加的
增加字段要考虑默认值，在代码中没有考虑的话，运行迁移时会被要求输入。
'''
class User(models.Model):
    userid = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    createtime = models.DateField(auto_now_add=True)
    img = models.ImageField(blank=True)

    class Meta:
        db_table = 'User'
```

```shell
python manage.py migrations
python manage.py migrate
```



## 实现登录时界面右上角显示用户名

```python
'''
views.py
判断登录，把是否登录的信息传给模板
'''
def index(request):
    if request.session.get('userid', False):
        username = request.session.get('userid')
    else:
        username = None
    content = {'username': username}
    return render(request, 'index.html', content)
```

```html
<!--
利用模板的标签，if判断
-->
<header>
			{% if username %}
			<a href="{% url 'library:userpage' username %}">{{ username }}</a>
			{% else %}
			<a href="#" id="login">登录</a>
			<a href="{% url 'library:register' %}" id="registor">注册</a>
			{% endif %}
</header>
```



## 保存图片作为头像

```python
'''
views.py
'''
def userpage(request, username):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['img']
            imgname = username + '.jpg'
            # 先保存起来
            u = User.objects.get(userid=username)
            u.img = imgname
            u.save()
            # 以绝对路径保存，最后的[2:]很坑爹，因为有“D:”，要把它去掉，这应该不是最优解
            real_path = settings.BASE_DIR + u.img.path[2:]
            with open(real_path, 'wb') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return redirect('/library/')
        else:
            pass
    else:
        form = UserForm()
        print('11111')
    return render(request, 'userpage.html', {'form': form, 'username': username})
```



## Django获取GET请求的参数

```python
    search_by = request.GET.get('search_by')
    keyword = request.GET.get('keyword')
```



## Django模板上显示图片（非线上环境）

在模板文件中，类似``<img src="/media/{{ book.cover }}">``的html语句，在浏览器中实际是通过访问 http://127.0.0.1:8000/media/....来找到图片并显示的。

1. 需要配置urls.py，让上面的url能够找到文件。
   - 有两种方式一种是通过static，一种是通过media
2. 配置settings.py

```python
# 通过media来访问

# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# settings.py
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

