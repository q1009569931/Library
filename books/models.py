from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Books(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')

    description = models.CharField(max_length=1024, default='', verbose_name='详细')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')

    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, verbose_name='封面')

    class Meta:
        db_table = 'Books'


class Collection(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Books, on_delete=models.CASCADE)
    createtime = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=100,  blank=True)

    class Meta:
        db_table = 'Collection'

class Comment(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    createtime = models.DateField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        db_table = 'Comment'