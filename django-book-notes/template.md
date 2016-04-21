模板高级进阶
===

## 模板语言回顾

> + 模板是一个纯文本文件，或是一个用Django模板语言标记过的普通Python字符串。模板可以包含模板标签和变量.
> + 模板标签是一个模板里面起标记作用的标记。
> + 区块标签被`{%`和`%}`包围：

```py
{% if is_logged_in %}
    Thanks for logging in!
{% else %}
    Please log in.
{% endif %}
```

> + 变量是一个模板用来输出值的标记
> +  变量标签`{{ }}`

	My first name is {{ first_name }}. My last name is {{ last_name }}.

**context** 是一个传递给模板的名称到值的映射（类似Python字典）。
**模板渲染** 就是是通过从context获取值来替换模板中变量并执行所有的模板标签。

## RequestContext和Context处理器
你需要一段context来解析模板。 一般情况下，这是一个`django.template.Context`的实例，不过在Django中还可以用一个特殊的子类， `django.template.RequestContext` ，这个用起来稍微有些不同。 `RequestContext` 默认地在模板`context`中加入了一些变量，如 `HttpRequest` 对象或当前登录用户的相关信息。
当你不想在一系例模板中都明确指定一些相同的变量时，你应该使用 RequestContext.考虑这两个视图：

```py
from django.template import loader, Context

def view_1(request):
    # ...
    t = loader.get_template('template1.html')
    c = Context({
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'message': 'I am view 1.'
    })
    return t.render(c)

def view_2(request):
    # ...
    t = loader.get_template('template2.html')
    c = Context({
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'message': 'I am the second view.'
    })
    return t.render(c)
```
这里故意不使用快捷的`render_to_response()`方法，是为了清晰说明所有步骤。
每个视图都传递了3个相同的变量：app、user、ip_address。如果把这些冗余去掉可好？
创建 RequestContext 和 context处理器 就是为了解决这个问题。
上面例子用context processors改写后：
```py
from django.template import loader, RequestContext
#context处理器，接受HttpRequest对象，返回字典.
def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }

def view_1(request):
    # ...
    t = loader.get_template('template1.html')
    c = RequestContext(request, {'message': 'I am view 1.'},
            processors=[custom_proc])
    return t.render(c)

def view_2(request):
    # ...
    t = loader.get_template('template2.html')
    c = RequestContext(request, {'message': 'I am the second view.'},
            processors=[custom_proc])
    return t.render(c)
```
为了讲解context处理器底层是如何工作的，在上面的例子中我们没有使用 `render_to_response()` 。但是建议选择`render_to_response()` 作为context的处理器。这就需要用到`context_instance`参数：
```py
from django.shortcuts import render_to_response
from django.template import RequestContext

def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }

def view_1(request):
    # 使用context_instance参数
    return render_to_response('template1.html',
        {'message': 'I am view 1.'},
        context_instance=RequestContext(request, processors=[custom_proc]))

def view_2(request):
    # ...
    return render_to_response('template2.html',
        {'message': 'I am the second view.'},
        context_instance=RequestContext(request, processors=[custom_proc]))
```
## django.core.context_processors.auth3

如果 `TEMPLATE_CONTEXT_PROCESSORS` 包含了这个处理器，那么每个 `RequestContext` 将包含这些变量：

+ `user` :一个 `django.contrib.auth.models.User `实例，描述了当前登录用户（或者一个 `AnonymousUser` 实例，如果客户端没有登录）。
+ `messages` : 一个当前登录用户的消息列表（字符串）。 在后台，对每一个请求，这个变量都调用 `request.user.get_and_delete_messages()` 方法。 这个方法收集用户的消息然后把它们从数据库中删除。
+ `perms` ： `django.core.context_processors.PermWrapper` 的一个实例，包含了当前登录用户有哪些权限。

## django.core.context_processors.debug
这个处理器把调试信息发送到模板层。 如果`TEMPLATE_CONTEXT_PROCESSORS`包含这个处理器，每一个`RequestContext`将包含这些变量:

+ `debug` ：你设置的 DEBUG 的值（ True 或 False ）。你可以在模板里面用这个变量测试是否处在debug模式下。
+ `sql_queries `：包含类似于 ``{‘sql’: …, ‘time’: `` 的字典的一个列表， 记录了这个请求期间的每个SQL查询以及查询所耗费的时间。 这个列表是按照请求顺序进行排列的。
+ DEBUG 参数设置为` True `。
+ 请求的`ip`应该包含在`INTERNAL_IPS` 的设置里面。

## django.core.context_processors.i18n
如果这个处理器启用，每个 RequestContext 将包含下面的变量：

+ `LANGUAGES` ： `LANGUAGES` 选项的值。
+ `LANGUAGE_CODE` ：如果 `request.LANGUAGE_CODE` 存在，就等于它；否则，等同于 `LANGUAGE_CODE` 设置。

## django.core.context_processors.request
如果启用这个处理器，每个` RequestContext` 将包含变量 `request` ， 也就是当前的 `HttpRequest` 对象。 注意这个处理器默认是不启用的，你需要激活它


## 写Context处理器的一些建议

编写处理器的一些建议：

+ 使每个`context`处理器完成尽可能小的功能。 使用多个处理器是很容易的，所以你可以根据逻辑块来分解功能以便将来复用。
+ 要注意 `TEMPLATE_CONTEXT_PROCESSORS `里的`context processor `将会在基于这个`settings.py`的每个 模板中有效，所以变量的命名不要和模板的变量冲突。 变量名是大小写敏感的，所以`processor`的变量全用大写是个不错的主意。
+ 不论它们存放在哪个物理路径下，只要在你的Python搜索路径中，你就可以在 `TEMPLATE_CONTEXT_PROCESSORS` 设置里指向它们。 建议你把它们放在应用或者工程目录下名为 `context_processors.py` 的文件里。