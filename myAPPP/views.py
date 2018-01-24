from django.shortcuts import render
from django.shortcuts import redirect
# from django.db import models  # 那会包导入错了，就是一直登陆不进去，靠
# from myAPPP import forms  # 导入自定义创建的表单模型
from . import forms
from . import models
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import hashlib
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.


def hash_code(s, salt='myAPPP'):  # 加点盐  ,用的是APP名称，即 myAPPP ？？,不是工程名称 untitled3 。使用Python内置的hashlib库，使用哈希值的方式加密密码
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    pass
    # return render(request, 'myAPPP/index.html')
    return render(request, 'login/index.html')  # 引用模板templates里的login路径


def login(request):
    if request.session.get('is_login', None):
        redirect('/index/')

    if request.method == 'POST':
        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)

        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():  # 使用表单类自带的is_valid()方法一步完成数据验证工作
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            print('*' * 50)
            print('*' * 50)
            print('*' * 50)
            print(username, password)
            print('*' * 50)

            # noinspection PyBroadException
            try:
                user = models.User.objects.get(name=username)  # models 为myAPPP里的，不django.db 里的models
                if not user.has_confirmed:
                    message = '该用户还未通过邮件确认！'
                    return render(request, 'login/login.html', locals())

                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    return redirect('/index/')
                else:
                    message = '密码不正确！'
            except BaseException:  # 我增加了 BaseException具体的异常，lifei，要不异常定义太宽泛，没有针对性
                message = "用户名不存在！"

            # hashkey = CaptchaStore.generate_key()
            # imgage_url = captcha_image_url(hashkey)

        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()  # 【代码规范很重要】算是领教Python缩进格式的问题了，
    # 此处向右缩进一个Tab，login页面的表单就不能自动渲染，点击提交后，才加载出来，我靠，排查了一遍代码，
    # 发现是此处向右缩进了，一开始以为是login.html 的问题
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterUser(request.POST)
        message = "请检查填写的内容！！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)

                send_email2(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                # return redirect('/login/')  # 自动跳转到登录页面
                return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面。

    register_form = forms.RegisterUser()
    return render(request, 'login/register.html', locals())
    # return render(request, 'login/register.html')  # 如果是myAPPP，会提示模板里找不到此文件


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/index/')
    request.session.flush()

    return redirect('/index/')


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)

    return code


def send_email2(email, code):
    subject = '来自www.liujiangblog.com的注册确认邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！\
                      如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except BaseException:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.cc_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
