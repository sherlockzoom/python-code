
高级视图和URL配置
===
## URLconf技巧
> URLconf没有什么特别的，就像Django中其他东西一样，是python代码

流线型化(Streamlining)函数导入

```py
from django.conf.urls.defaults import *
from mysite.views import hello, current_datetime, hours_ahead

urlpatterns = patterns('',
    (r'^hello/$', hello),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
)
```
URLconf 中的每一个入口包括了它所关联的视图函数，直接传入了一个函数对象。当然也可以从模块开始导入`mysite.views.hello`都是合法的 。

在我们的URLconf例子中，每个视图字符串的开始部分都是`mysite.views`，造成重复输入。 我们可以把公共的前缀提取出来，作为第一个参数传给 `patterns`函数

```py
from django.conf.urls.defaults import *

urlpatterns = patterns('mysite.views' ,
    (r'^hello/$', 'hello' ),
    (r'^time/$', 'current_datetime' ),
    (r'^time/plus/(d{1,2})/$', 'hours_ahead'),
)
```
字符串方法的好处如下:

- 更紧凑，因为不需要你导入视图函数。

- 如果你的视图函数存在于几个不同的 Python 模块的话，它可以使得 URLconf 更易读和管理。

函数对象方法的好处如下:

- 更容易对视图函数进行包装(wrap)。 

- 更 Pythonic，就是说，更符合 Python 的传统，如把函数当成对象传递。

两个方法都是有效的，甚至你可以在同一个 URLconf 中混用它们。 决定权在你。

###　使用多个视图前缀
在实践中，如果你使用字符串技术，特别是当你的 URLconf 中没有一个公共前缀时，你最终可能混合视图。 然而，你仍然可以利用视图前缀的简便方式来减少重复。 只要增加多个 patterns() 对象，象这样
```py
from django.conf.urls.defaults import *

urlpatterns = patterns('mysite.views',
    (r'^hello/$', 'hello'),
    (r'^time/$', 'current_datetime'),
    (r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
)

urlpatterns += patterns('weblog.views',
    (r'^tag/(\w+)/$', 'tag'),
)
```
### 调试模式中的特例
说到动态构建 urlpatterns，你可能想利用这一技术，在 Django 的调试模式下修改 URLconf 的行为。 为了做到这一点，只要在运行时检查 DEBUG 配置项的值即可
```py
from django.conf import settings
from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^$', views.homepage),
    (r'^(\d{4})/([a-z]{3})/$', views.archive_month),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debuginfo/$', views.debug),
    )
```
URL `debuginfo/`只有在debug为true时才有效。

### 使用命名组
在目前为止的所有 URLconf 例子中，我们使用简单的无命名 正则表达式组，即，在我们想要捕获的URL部分上加上小括号，***Django 会将捕获的文本作为位置参数传递给视图函数***。 在更高级的用法中，还可以使用 命名 正则表达式组来捕获URL，并且将其作为 **关键字 参数传给视图** 。先看个例子：
```py
# 无名组
from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^articles/(\d{4})/$', views.year_archive),
    (r'^articles/(\d{4})/(\d{2})/$', views.month_archive),
)
```
使用命名组重写URLconf后：
```py
from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^articles/(?P<year>\d{4})/$', views.year_archive),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
)
```
> 只有一个细微的差别： 取的值是以关键字参数的方式而不是以位置参数的方式传递给视图函数的。

### 理解匹配/分组算法
需要注意的是如果在URLconf中使用命名组，那么命名组和非命名组是不能同时存在于同一个URLconf的模式中的。 如果你这样做，Django不会抛出任何错误，但你可能会发现你的URL并没有像你预想的那样匹配正确。 具体地，以下是URLconf解释器有关正则表达式中命名组和 非命名组所遵循的算法:

- 如果有任何命名的组，Django会忽略非命名组而直接使用命名组。

- 否则，Django会把所有非命名组以位置参数的形式传递。

- 在以上的两种情况，Django同时会以关键字参数的方式传递一些额外参数。 

### 传递额外的参数到视图函数中
有时会发现你写的视图十分相似，只有点点不同。比如你有2个视图，出来模板不同其他都相同。
```py
# urls.py

from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^foo/$', views.foo_view),
    (r'^bar/$', views.bar_view),
)

# views.py

from django.shortcuts import render_to_response
from mysite.models import MyModel

def foo_view(request):
    m_list = MyModel.objects.filter(is_new=True)
    return render_to_response('template1.html', {'m_list': m_list}) #use tmplate1.html
def bar_view(request):
    m_list = MyModel.objects.filter(is_new=True)
    return render_to_response('template2.html', {'m_list': m_list}) #use tmplate2.html
```
这里做了重复的工作，显然是不够简洁的。我们可以通过捕获URL，在视图中检查再决定使用哪个模板。
```py
# urls.py

from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^(foo)/$', views.foobar_view),
    (r'^(bar)/$', views.foobar_view),
)

# views.py

from django.shortcuts import render_to_response
from mysite.models import MyModel

def foobar_view(request, url):
    m_list = MyModel.objects.filter(is_new=True)
    if url == 'foo':
        template_name = 'template1.html'
    elif url == 'bar':
        template_name = 'template2.html'
    return render_to_response(template_name, {'m_list': m_list})
```
> 这种解决方案的问题还是老缺点，就是把你的URL耦合进你的代码里面了。 如果你打算把 `/foo/` 改成 `/fooey/ `的话，那么你就得记住要去改变视图里面的代码。

对一个可选URL配置参数的**优雅解决方法**： URLconf里面的每一个模式都可以包含第三个数据： 一个关键字参数的字典：
```py
# urls.py

from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^foo/$', views.foobar_view, {'template_name': 'template1.html'}),
    (r'^bar/$', views.foobar_view, {'template_name': 'template2.html'}),
)

# views.py

from django.shortcuts import render_to_response
from mysite.models import MyModel

def foobar_view(request, template_name):
    m_list = MyModel.objects.filter(is_new=True)
    return render_to_response(template_name, {'m_list': m_list})
```
在后面的通用视图系统，我们会更加细节的讨论。
###　伪造捕捉到的值
比如说你有匹配某个模式的一堆视图，以及一个并不匹配这个模式但视图逻辑是一样的URL。 这种情况下，你可以通过向**同一个视图**传递额外URLconf参数来伪造URL值的捕捉。

例如，你可能有一个显示某一个特定日子的某些数据的应用，URL类似这样的：
```
/mydata/jan/01/
/mydata/jan/02/
/mydata/jan/03/
# ...
/mydata/dec/30/
/mydata/dec/31/
```
当然你可以直接使用命名组来捕获
```py
urlpatterns = patterns('',
    (r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', views.my_view),
)
```
**[友谊的小船说翻就翻](http://baike.baidu.com/item/%E5%8F%8B%E8%B0%8A%E7%9A%84%E5%B0%8F%E8%88%B9%E8%AF%B4%E7%BF%BB%E5%B0%B1%E7%BF%BB)**，比如你的BOSS可能会想增加这样一个URL，` /mydata/birthday/` ， 这个URL等价于` /mydata/jan/06/ `。这时你可以这样利用额外URLconf参数：
```py
urlpatterns = patterns('',
    (r'^mydata/birthday/$', views.my_view, {'month': 'jan', 'day': '06'}),
    (r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', views.my_view),
)
```
在这里最帅的地方莫过于你根本不用改变你的视图函数。 视图函数只会关心它 获得 了 参数，它不会去管这些参数到底是捕捉回来的还是被额外提供的。month和day

### 创建一个通用视图
抽取出我们代码中共性的东西是一个很好的编程习惯.
```
def say_hello(person_name):
    print 'Hello, %s' % person_name

def say_goodbye(person_name):
    print 'Goodbye, %s' % person_name
# 把问候语提出来看做一个参数
def greet(person_name, greeting):
    print '%s, %s' % (greeting, person_name)
```
通过使用额外的URLconf参数，你可以把同样的思想应用到Django的视图中。

更具体地说，比如这个视图显示一系列的 Event 对象，那个视图显示一系列的 BlogEntry 对象，并意识到它们都是一个用来显示一系列对象的视图的特例，而对象的类型其实就是一个变量。
```py
# urls.py

from django.conf.urls.defaults import *
from mysite import views

urlpatterns = patterns('',
    (r'^events/$', views.event_list),
    (r'^blog/entries/$', views.entry_list),
)

# views.py

from django.shortcuts import render_to_response
from mysite.models import Event, BlogEntry

def event_list(request):
    obj_list = Event.objects.all()
    return render_to_response('mysite/event_list.html', {'event_list': obj_list})

def entry_list(request):
    obj_list = BlogEntry.objects.all()
    return render_to_response('mysite/blogentry_list.html', {'entry_list': obj_list})
```
这两个视图都是一样的功能，显示一些列的对象。让我们把显示的对象抽象出来
```py
# urls.py

from django.conf.urls.defaults import *
from mysite import models, views

urlpatterns = patterns('',
    (r'^events/$', views.object_list, {'model': models.Event}),
    (r'^blog/entries/$', views.object_list, {'model': models.BlogEntry}),
)

# views.py

from django.shortcuts import render_to_response

def object_list(request, model):
    obj_list = model.objects.all()
    template_name = 'mysite/%s_list.html' % model.__name__.lower()
    return render_to_response(template_name, {'object_list': obj_list})
```
就这样小小的改动，我们突然发现我们有了一个可复用的，模型无关的视图！ 从现在开始，当我们需要一个视图来显示一系列的对象时，我们可以简简单单的重用这一个 object_list 视图，而无须另外写视图代码了。 以下是我们做过的事情：

- 我们通过 model 参数直接传递了模型类。 额外URLconf参数的字典是可以传递任何类型的对象，而不仅仅只是字符串。

- 这一行： model.objects.all() 是 鸭子界定 

- 我们使用 model.__name__.lower() 来决定模板的名字。 每个Python的类都有一个 __name__ 属性返回类名。 这特性在当我们直到运行时刻才知道对象类型的这种情况下很有用。 比如， BlogEntry 类的 __name__ 就是字符串 'BlogEntry' 。

- 这个例子与前面的例子稍有不同，我们传递了一个通用的变量名给模板。 当然我们可以轻易的把这个变量名改成 blogentry_list 或者 event_list




> [Django book 高级视图好URL配置](http://djangobook.py3k.cn/2.0/chapter08/)
> Written with [StackEdit](https://stackedit.io/).