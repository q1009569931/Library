from django import forms


class RegisterForm(forms.Form):
    userid = forms.CharField(label='账户', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(label='重复密码', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(label='昵称', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    userid = forms.CharField(label='账户', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

class searchForm(forms.Form):
    CHOICE = (
        ('ISBN', 'ISBN'),
        (u'书名', u'书名'),
        (u'作者', u'作者')
    )

    search_by = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE, initial=u'书名')
    keyword = forms.CharField(
            label='',
            max_length=32,
            widget=forms.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': u'请输入需要检索的图书信息',
                'name': 'keyword',
            })
        )
