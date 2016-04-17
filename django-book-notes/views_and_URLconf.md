
高级视图和URL配置
===
[toc]

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

- 在以上的两种情况，Django同时会以关键字参数的方式传递一些额外参数。 更具体的信息可参考下一节





> Written with [StackEdit](https://stackedit.io/).