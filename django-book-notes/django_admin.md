<h1 id="djnago站点管理">Djnago站点管理</h1>
<p><a href="http://djangobook.py3k.cn/2.0/chapter06/">http://djangobook.py3k.cn/2.0/chapter06/</a></p>
<p>django的自动管理界面：它读取你模型中的元数据，然后提供给你一个强大而且可以使用的界面，网站管理者可以用它立即工作。</p>
<h3 id="django.contrib包">django.contrib包</h3>
<p>django自动管理工具是<code>django.contrib</code>的一部分。使用它在开发中不用“重复造轮子”</p>
<p><code>django.contrib</code>有诸多可用的模块</p>
<ul>
<li>用户鉴别系统<code>django.contrib.auth</code></li>
<li>支持匿名会话<code>django.contrib.sessions</code></li>
<li>用户评注系统 <code>django.contrib.comments</code></li>
<li>。。。</li>
</ul>
<h3 id="激活管理界面">激活管理界面</h3>
<p>要使用django管理站点的功能，需要在项目中花费几个步骤去激活它：</p>
<p>第一步，对你的<code>settings</code>文件做如下修改 ：</p>
<ol>
<li>将<code>django.contrib.admin</code>加入setting的<code>INSTALLED_APPS</code>配置中</li>
<li>保证<code>INSTALLED_APPS</code>中包含<code>django.contrib.auth</code>，<code>django.contrib.contenttypes</code>和<code>django.contrib.sessions</code>，Django的管理工具需要这3个包</li>
<li>确保<code>MIDDLEWARE_CLASSES</code>中包含<code>django.middleware.common.CommonMiddleware</code>、<code>django.contrib.sessions.middleware.SessionMiddleware</code>和<code>django.contrib.auth.middleware.AuthenticationMiddleware</code>’</li>
</ol>
<p>第二步，创建admin用户帐号</p>
<pre><code>python manage.py createsuperuser
</code></pre>
<p>第三步，配置<code>URLconf</code></p>
<pre><code># Include these import statements...
from django.contrib import admin
admin.autodiscover()

# And include this URLpattern...
urlpatterns = patterns('',
    # ...
    (r'^admin/', include(admin.site.urls)),
    # ...
)
</code></pre>
<h3 id="将你的models加入到admin管理中">将你的Models加入到Admin管理中</h3>
<p>有一个关键步骤我们还没做。 让我们将自己的模块加入管理工具中，这样我们就能够通过这个漂亮的界面添加、修改和删除数据库中的对象<br>
在<code>books</code>（你的app）目录下，创建一个文件<code>admin.py</code></p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin
<span class="token keyword">from</span> mysite<span class="token punctuation">.</span>books<span class="token punctuation">.</span>models <span class="token keyword">import</span> Publisher<span class="token punctuation">,</span> Author<span class="token punctuation">,</span> Book

admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>register<span class="token punctuation">(</span>Publisher<span class="token punctuation">)</span>
admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>register<span class="token punctuation">(</span>Author<span class="token punctuation">)</span>
admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>register<span class="token punctuation">(</span>Book<span class="token punctuation">)</span>
</code></pre>
<p>完成后，可以打开页面 <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a></p>
<blockquote>
<p>到此，django的管理工具就可以使用了。那它是怎么工作的呢？</p>
</blockquote>
<h3 id="admin是如何工作的">Admin是如何工作的</h3>
<ol>
<li>服务启动时，django从<code>urs.py</code>执行<code>admin.autodiscover()</code>。这个函数遍历<code>INSTALLED_APPS</code>配置，并寻找相关的<code>admin.py</code>文件。</li>
<li>在找到的app目录下的<code>admin.py</code>文件中，调用<code>admin.site.register()</code>将这个模块注册到管理工具中。</li>
</ol>