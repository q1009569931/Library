import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

import django

django.setup()

import json
import codecs
from books.models import Books, User

def init__book_data():
    with codecs.open('books.json', 'r', 'utf-8') as f:
        books = json.load(f)

    for b in books:
        print(b)
        try:
            B = Books.objects.get_or_create(ISBN=b['ISBN'], title=b['name'], author=b['author'], press=b['press'])[0]
            if b.get('content_description'):
                B.description = b['content_description']
            if b.get('price'):
                B.price = b['price']
            if b.get('cover'):
                B.cover = b['cover']
            B.save()
        except KeyError:
            continue

def init_user_data():
    u = User.objects.create_user(username='13145747212', password='123456', email='1009569931@163.com')
    u.save()
    u = User.objects.create_user(username='13502610664', password='123456', email='1009569931@163.com')
    u.save()
    print('OK')

if __name__ == '__main__':
    init__book_data()
    init_user_data()