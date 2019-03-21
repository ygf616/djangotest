from django.test import TestCase
from sign.models import Guest, Event
from django.contrib.auth.models import User


# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address="shenzhen",
                             start_time="2016-08-31 02:18:22")
        Guest.objects.create(id=1, event_id=1, realname="alen", phone='13711001101', email="alen@mail.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="13711001101")
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)


# 测试sign应用的视图
class IndexPageTest(TestCase):

    def test_index_page_renders_index_template(self):
        '''测试index视图'''
        response = self.client.get(
            '/index/')  # 虽然没有导入django.test.Client类，但是self.client最终调用的依然是django.test.Client类的方法，请求/index/路径
        self.assertEqual(response.status_code, 200)  # status_code获取HTTP返回的状态码，使用assertEqual断言状态码是否为200
        self.assertTemplateUsed(response, 'index.html')  # 使用assertTemplateUsed()断言服务器是否使用的是index.html模板进行响应


class LoginActionTest(TestCase):
    '''测试登录动作'''

    def setUp(self):  # 初始化，调用User.objects.create_user创建登录用户数据
        User.objects.create_user('james', 'james@qq.com', '123456')

    def test_add_admin(self):
        '''测试添加的用户数据是否正确'''
        user = User.objects.get(username='james')
        self.assertEqual(user.username, 'james')
        self.assertEqual(user.email, 'james@qq.com')  # 注意这里书中有误，user表里的字段是email而不是mail，否则会报错

    def test_login_action_username_password_null(self):
        '''测试用户名密码为空'''
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)  # 通过post()方法请求'/login_aciton/'路径测试登录功能
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)  # assertIn()方法断言返回的HTML页面中是否包含指定的提示字符串

    def test_login_action_username_password_error(self):
        '''测试用户名密码错误'''
        test_data = {'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_success(self):
        '''测试登录成功'''
        test_data = {'username': 'james', 'password': '123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code,
                         302)  # 这里为什么断言的是302，是因为登录成功后，通过HttpResponseRedirect()跳转到了'/event_manage/'路径，这是一个重定向
