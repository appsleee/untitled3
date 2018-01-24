import os
from django.core.mail import send_mail  # 1.纯文本格式时调用
from django.core.mail import EmailMultiAlternatives
import datetime
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled3.settings'

# 1.发送纯文本格式的邮件
# if __name__ == '__main__':
#     send_mail(
#         '来自www.liujiangblog.com的测试邮件',
#         '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python和Django技术的分享！',
#         '937373673@qq.com',  # 发送方
#         ['861116543@qq.com'],  # 接收方
#     )


# # 2.发送HTML格式的邮件
if __name__ == '__main__':
    subject, from_email, to = '来自www.liujiangblog.com的测试邮件', 'youtoo556@sina.com', '861116543@qq.com'   # 861116543@qq.com  youtoo556@sina.com
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    print('*' * 50)
    print('*' * 50)
    print('*' * 50, '\n')
    print('OK,邮件发送成功...')
    print('\n')
    # print('发送时间为:', datetime.datetime.now())
    print('发送时间为:', time.strftime('%Y-%m-%d %H:%M:%S'))

#  亲测，新浪邮箱可以使用 apps_leee@sina.com ，654321fei，新浪邮箱可以发到QQ邮箱！
#  可以单独运行此模块进行，邮件功能的测试
