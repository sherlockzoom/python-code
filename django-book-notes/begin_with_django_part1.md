<h1 id="django开发起步篇">django开发起步篇</h1>
<div class="toc"><ul><li><a href="#django开发起步篇">django开发起步篇</a><ul><li><ul><li><a href="#django是怎样处理请求的">django是怎样处理请求的</a></li><li><a href="#模块系统template-system">模块系统(Template System)</a><ul><li><a href="#python代码中使用django模板的最基本方式">python代码中使用django模板的最基本方式</a></li><li><a href="#模板渲染">模板渲染</a></li><li><a href="#基本的模板标签和过滤器">基本的模板标签和过滤器</a></li><li><a href="#过滤器">过滤器</a></li><li><a href="#include-模板标签">include 模板标签</a></li><li><a href="#模板继承">模板继承</a></li></ul></li><li><a href="#设计哲学理念">设计哲学理念</a></li></ul></li></ul></li></ul></div><h3 id="django是怎样处理请求的">django是怎样处理请求的</h3>
<p><code>http://127.0.0.1:8000/hello/</code>为例</p>
<ul>
<li>进来的请求转入<code>/hello/</code></li>
<li><code>Django</code>通过在<code>ROOT_URLCONF</code>配置来决定根<code>URLconf</code>.</li>
<li><code>Django</code>在<code>URLconf</code>中的所有URL模式中，查找第一个匹配<code>/hello/</code>的条目。</li>
<li>如果找到匹配，将调用相应的视图函数</li>
<li>视图函数返回一个<code>HttpResponse</code></li>
<li>Django转换<code>HttpResponse</code>为一个适合的HTTP response， 以Web page显示出来</li>
</ul>
<h3 id="模块系统template-system"><a href="http://djangobook.py3k.cn/2.0/chapter04/">模块系统</a>(Template System)</h3>
<p>硬编码指的是：HTML被直接编码在python代码中，如下所示：</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">def</span> current_datetime<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    now <span class="token operator">=</span> datetime<span class="token punctuation">.</span>datetime<span class="token punctuation">.</span>now<span class="token punctuation">(</span><span class="token punctuation">)</span>
    html <span class="token operator">=</span> <span class="token string">"&lt;html&gt;&lt;body&gt;It is now %s.&lt;/body&gt;&lt;/html&gt;"</span> <span class="token operator">%</span> now
    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span>html<span class="token punctuation">)</span>
</code></pre>
<p>HTML硬编码到你的视图不是一个好主意。下面一一道来：</p>
<ul>
<li>对页面设计进行的任何改变都必须对python代码进行相应的修改。站点设计的修改往往比底层python代码修改要频繁的多。</li>
<li>Python代码编写和HTML设计是两项不同的工作。设计者和HTML/CSS的编码人员不应该去编辑python代码来完成他们的工作</li>
<li>程序员编写Python代码和设计人员制作模板两项工作同时进行的效率最高。</li>
</ul>
<p>因此，将页面的设计和python代码分离开会更干净简洁更容易维护。使用Django的模板系统来实现这种模式。</p>
<blockquote>
<p>模板是一个文本，用于分离文档的表现形式和内容。模板定义了占位符以及各种用于规范文档该如何显示的各部分基本逻辑（模板标签）。 模板通常用于产生HTML，但是Django的模板也能产生任何基于文本格式的文档</p>
</blockquote>
<p>该模板描述了一个向某个与公司签单人员致谢 HTML 页面</p>
<pre class=" language-html"><code class="prism  language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>head</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>title</span><span class="token punctuation">&gt;</span></span>Ordering notice<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>title</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>head</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>body</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>h1</span><span class="token punctuation">&gt;</span></span>Ordering notice<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>h1</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Dear {{ person_name }},<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Thanks for placing an order from {{ company }}. It's scheduled to
ship on {{ ship_date|date:"F j, Y" }}.<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Here are the items you've ordered:<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>ul</span><span class="token punctuation">&gt;</span></span>
{% for item in item_list %}
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>li</span><span class="token punctuation">&gt;</span></span>{{ item }}<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>li</span><span class="token punctuation">&gt;</span></span>
{% endfor %}
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>ul</span><span class="token punctuation">&gt;</span></span>

{% if ordered_warranty %}
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Your warranty information will be included in the packaging.<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
{% else %}
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>You didn't order a warranty, so you're on your own when
    the products inevitably stop working.<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
{% endif %}

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Sincerely,<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>br</span> <span class="token punctuation">/&gt;</span></span>{{ company }}<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>body</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<p>逐步分析上面模板：</p>
<ol>
<li>用大括号括起来的文字<code>{{ person.name }}</code>称为<strong>变量</strong></li>
<li><code>{% if ordered_warranty %}</code> 是<strong>模板标签</strong>，标签是仅通知模板系统完成某些工作的标签</li>
<li>最后，这个模板的第二段中有一个关于<strong>filter</strong>过滤器的例子，它是一种最便捷的转换变量输出格式的方式。 如这个例子中的<code>{{ship_date|date:”F j, Y” }}</code>，我们将变量<code>ship_date</code>传递给<code>date</code>过滤器，同时指定参数<code>”F j,Y”</code>。<code>date</code>过滤器根据参数进行格式输出</li>
</ol>
<h4 id="python代码中使用django模板的最基本方式">python代码中使用django模板的最基本方式</h4>
<ol>
<li>可以用原始的模板代码字符串创建一个 Template 对象， Django同样支持用指定模板文件路径的方式来创建 Template 对象</li>
<li>调用模板对象的render方法，并且传入一套变量context。它将返回一个基于模板的展现字符串，模板中的变量和标签会被context值替换。</li>
</ol>
<pre class=" language-py"><code class="prism  language-py"><span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">from</span> django <span class="token keyword">import</span> template
<span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> t <span class="token operator">=</span> template<span class="token punctuation">.</span>Template<span class="token punctuation">(</span><span class="token string">'My name is {{ name }}.'</span><span class="token punctuation">)</span>
<span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> <span class="token number">c</span> <span class="token operator">=</span> template<span class="token punctuation">.</span>Context<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">'name'</span><span class="token punctuation">:</span> <span class="token string">'Adrian'</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">print</span> t<span class="token punctuation">.</span>render<span class="token punctuation">(</span><span class="token number">c</span><span class="token punctuation">)</span>
My name <span class="token keyword">is</span> Adrian<span class="token punctuation">.</span>
<span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> <span class="token number">c</span> <span class="token operator">=</span> template<span class="token punctuation">.</span>Context<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">'name'</span><span class="token punctuation">:</span> <span class="token string">'Fred'</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token operator">&gt;</span><span class="token operator">&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">print</span> t<span class="token punctuation">.</span>render<span class="token punctuation">(</span><span class="token number">c</span><span class="token punctuation">)</span>
My name <span class="token keyword">is</span> Fred<span class="token punctuation">.</span>
</code></pre>
<p><code>Template/Context/render</code></p>
<h4 id="模板渲染">模板渲染</h4>
<p>一旦你创建一个 Template 对象，你可以用 context 来传递数据给它。 一个context是一系列变量和它们值的集合。之后调用 Template 对象 的 render() 方法并传递context来填充模板</p>
<blockquote>
<p>Django模板系统的基本规则： 写模板，创建 Template 对象，创建 Context ， 调用 render() 方法。</p>
</blockquote>
<h4 id="基本的模板标签和过滤器">基本的模板标签和过滤器</h4>
<p><code>if</code></p>
<pre class=" language-py"><code class="prism  language-py"><span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> today_is_weekend <span class="token operator">%</span><span class="token punctuation">}</span>
    <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Welcome to the weekend<span class="token operator">!</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
<span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span>
<span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span><span class="token operator">-</span>
<span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> today_is_weekend <span class="token operator">%</span><span class="token punctuation">}</span>
    <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Welcome to the weekend<span class="token operator">!</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
<span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">else</span> <span class="token operator">%</span><span class="token punctuation">}</span>
    <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Get back to work<span class="token punctuation">.</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
<span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span>
</code></pre>
<blockquote>
<p>并没有 <code>{% elif %}</code> 标签， 请使用嵌套的<code>{% if %}</code> 标签来达成同样的效果<br>
<code>for</code></p>
</blockquote>
<pre class=" language-html"><code class="prism  language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>ul</span><span class="token punctuation">&gt;</span></span>
{% for athlete in athlete_list %}
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>li</span><span class="token punctuation">&gt;</span></span>{{ athlete.name }}<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>li</span><span class="token punctuation">&gt;</span></span>
{% endfor %}
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>ul</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<p>在执行循环之前先检测列表的大小是一个通常的做法，当列表为空时输出一些特别的提示。</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> athlete_list <span class="token operator">%</span><span class="token punctuation">}</span>
    <span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">for</span> athlete <span class="token keyword">in</span> athlete_list <span class="token operator">%</span><span class="token punctuation">}</span>
        <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span><span class="token punctuation">{</span><span class="token punctuation">{</span> athlete<span class="token punctuation">.</span>name <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
    <span class="token punctuation">{</span><span class="token operator">%</span> endfor <span class="token operator">%</span><span class="token punctuation">}</span>
<span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">else</span> <span class="token operator">%</span><span class="token punctuation">}</span>
    <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>There are no athletes<span class="token punctuation">.</span> Only computer programmers<span class="token punctuation">.</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
<span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span>
</code></pre>
<p>每个<code>{% for %}</code>循环里有一个称为<code>forloop</code> 的模板变量。这个变量有一些提示循环进度信息的属性。</p>
<ol>
<li><code>forloop.counter</code> 总是一个表示当前循环的执行次数的整数计数器。 这个计数器是从1开始的，所以在第一次循环时 <code>forloop.counter</code> 将会被设置为1。</li>
<li><code>forloop.counter0</code> 类似于 <code>forloop.counter</code> ，但是它是从0计数的。 第一次执行循环时这个变量会被设置为0。</li>
<li><code>forloop.revcounter</code> 是表示循环中剩余项的整型变量。 在循环初次执行时 <code>forloop.revcounter</code> 将被设置为序列中项的总数。 最后一次循环执行中，这个变量将被置1</li>
<li><code>forloop.revcounter0</code> 类似于 <code>forloop.revcounter</code> ，但它以0做为结束索引。 在第一次执行循环时，该变量会被置为序列的项的个数减1</li>
<li><code>forloop.first</code> 是一个布尔值，如果该迭代是第一次执行，那么它被置为````</li>
<li><code>forloop.last</code> 是一个布尔值；在最后一次执行循环时被置为<code>True</code></li>
<li>f<code>orloop.parentloop</code> 是一个指向当前循环的上一级循环的 <code>forloop</code> 对象的引用（在嵌套循环的情况下</li>
</ol>
<p><code>ifequal/ifnotequal</code></p>
<blockquote>
<p><code>{% ifequal %}</code> 标签比较两个值，当他们相等时，显示在 <code>{% ifequal %}</code> 和 <code>{% endifequal %}</code> 之中所有的值。</p>
</blockquote>
<h4 id="过滤器">过滤器</h4>
<p>显示的内容是变量 <code>{{ name }}</code> 被过滤器 <code>lower</code> 处理后的结果，它功能是转换文本为小写</p>
<pre><code>{{ name|lower }}
{{ my_list|first|upper }}
</code></pre>
<p>一个例子看看模板加载</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>template<span class="token punctuation">.</span>loader <span class="token keyword">import</span> get_template
<span class="token keyword">from</span> django<span class="token punctuation">.</span>template <span class="token keyword">import</span> Context
<span class="token keyword">from</span> django<span class="token punctuation">.</span>http <span class="token keyword">import</span> HttpResponse
<span class="token keyword">import</span> datetime

<span class="token keyword">def</span> current_datetime<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    now <span class="token operator">=</span> datetime<span class="token punctuation">.</span>datetime<span class="token punctuation">.</span>now<span class="token punctuation">(</span><span class="token punctuation">)</span>
    t <span class="token operator">=</span> get_template<span class="token punctuation">(</span><span class="token string">'current_datetime.html'</span><span class="token punctuation">)</span>
    html <span class="token operator">=</span> t<span class="token punctuation">.</span>render<span class="token punctuation">(</span>Context<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">'current_date'</span><span class="token punctuation">:</span> now<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span>html<span class="token punctuation">)</span>
</code></pre>
<p><code>render_to_response()</code>进一步简化模板载入</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render_to_response
<span class="token keyword">import</span> datetime

<span class="token keyword">def</span> current_datetime<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    now <span class="token operator">=</span> datetime<span class="token punctuation">.</span>datetime<span class="token punctuation">.</span>now<span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'current_datetime.html'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">'current_date'</span><span class="token punctuation">:</span> now<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre>
<p><code>locals()</code> 时要注意是它将包括 所有 的局部变量，它们可能比你想让模板访问的要多</p>
<h4 id="include-模板标签">include 模板标签</h4>
<pre class=" language-html"><code class="prism  language-html">{% include 'nav.html' %}
{% include "nav.html" %}
</code></pre>
<h4 id="模板继承">模板继承</h4>
<blockquote>
<p>一个常见的 Web 开发问题： 在整个网站中，如何减少共用页面区域（比如站点导航）所引起的重复和冗余代码？</p>
</blockquote>
<p>解决这个问题的服务器端 include 方案是找出两个模板中的共同部分，将其保存为不同的模板片段，然后在每个模板中进行 include。 也许你会把模板头部的一些代码保存为 <code>header.html</code> 文件：</p>
<pre class=" language-html"><code class="prism  language-html"><span class="token doctype">&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"&gt;</span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span> <span class="token attr-name">lang</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>en<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>head</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<p>你可能会把底部保存到文件 <code>footer.html</code> :</p>
<pre class=" language-html"><code class="prism  language-html">    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>hr</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Thanks for visiting my site.<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>body</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<p>但是这样的拆分也是有问题的，比如每个页面都有一个不同的标题，那么如果包含在头部，这样就不能每个页面进行定制了。为此Django 的模板继承系统解决了这些问题。</p>
<ol>
<li>第一步定义<code>基础模板</code>，该框架之后将有子模板所继承<code>base.html</code></li>
</ol>
<pre class=" language-html"><code class="prism  language-html"><span class="token doctype">&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"&gt;</span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span> <span class="token attr-name">lang</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>en<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>head</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>title</span><span class="token punctuation">&gt;</span></span>{% block title %}{% endblock %}<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>title</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>head</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>body</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>h1</span><span class="token punctuation">&gt;</span></span>My helpful timestamp site<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>h1</span><span class="token punctuation">&gt;</span></span>
    {% block content %}{% endblock %}
    {% block footer %}
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>hr</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Thanks for visiting my site.<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
    {% endblock %}
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>body</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<ol start="2">
<li>每个<code>{% block %}</code>标签所要做的是告诉模板引擎，该模板下的这一块内容将有可能被子模板覆盖。</li>
</ol>
<blockquote>
<p><code>{% block %}</code> 标签告诉模板引擎，子模板可以重载这些部分</p>
</blockquote>
<p><code>current_datetime.html</code>模板</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token punctuation">{</span><span class="token operator">%</span> extends <span class="token string">"base.html"</span> <span class="token operator">%</span><span class="token punctuation">}</span>

<span class="token punctuation">{</span><span class="token operator">%</span> block title <span class="token operator">%</span><span class="token punctuation">}</span>The current time<span class="token punctuation">{</span><span class="token operator">%</span> endblock <span class="token operator">%</span><span class="token punctuation">}</span>

<span class="token punctuation">{</span><span class="token operator">%</span> block content <span class="token operator">%</span><span class="token punctuation">}</span>
<span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>It <span class="token keyword">is</span> now <span class="token punctuation">{</span><span class="token punctuation">{</span> current_date <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token punctuation">.</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
<span class="token punctuation">{</span><span class="token operator">%</span> endblock <span class="token operator">%</span><span class="token punctuation">}</span>
</code></pre>
<p>你可以根据需要使用任意多的继承次数。 使用继承的一种常见方式是下面的三层法：</p>
<ul>
<li>
<p>创建 base.html 模板，在其中定义站点的主要外观感受。 这些都是不常修改甚至从不修改的部分。</p>
</li>
<li>
<p>为网站的每个区域创建 base_SECTION.html 模板(例如, base_photos.html 和 base_forum.html )。这些模板对 base.html 进行拓展，并包含区域特定的风格与设计。1</p>
</li>
<li>
<p>为每种类型的页面创建独立的模板，例如论坛页面或者图片库。 这些模板拓展相应的区域模板。</p>
</li>
</ul>
<p>以下是使用模板继承的一些诀窍：</p>
<ul>
<li>
<p>如果在模板中使用 {% extends %} ，必须保证其为模板中的第一个模板标记。 否则，模板继承将不起作用。3</p>
</li>
<li>
<p>一般来说，基础模板中的 {% block %} 标签越多越好。 记住，子模板不必定义父模板中所有的代码块，因此你可以用合理的缺省值对一些代码块进行填充，然后只对子模板所需的代码块进行（重）定义。 俗话说，钩子越多越好。4</p>
</li>
<li>
<p>如果发觉自己在多个模板之间拷贝代码，你应该考虑将该代码段放置到父模板的某个 {% block %} 中。</p>
</li>
<li>
<p>如果你需要访问父模板中的块的内容，使用 {{ block.super }}这个标签吧，这一个魔法变量将会表现出父模板中的内容。 如果只想在上级代码块基础上添加内容，而不是全部重载，该变量就显得非常有用了。14</p>
</li>
<li>
<p>不允许在同一个模板中定义多个同名的 {% block %} 。 存在这样的限制是因为block 标签的工作方式是双向的。 也就是说，block 标签不仅挖了一个要填的坑，也定义了在父模板中这个坑所填充的内容。如果模板中出现了两个相同名称的 {% block %} 标签，父模板将无从得知要使用哪个块的内容。4</p>
</li>
<li>
<p>{% extends %} 对所传入模板名称使用的加载方法和 get_template() 相同。 也就是说，会将模板名称被添加到 TEMPLATE_DIRS 设置之后。3</p>
</li>
<li>
<p>多数情况下， {% extends %} 的参数应该是字符串，但是如果直到运行时方能确定父模板名，这个参数也可以是个变量。 这使得你能够实现一些很酷的动态功能</p>
</li>
</ul>
<h3 id="设计哲学理念">设计哲学理念</h3>
<ol start="2">
<li>业务逻辑应该和表现逻辑相对分开 。我们将模板系统视为控制表现及表现相关逻辑的工具，仅此而已。 模板系统不应提供超出此基本目标的功能。</li>
<li>语法不应受到 HTML/XML 的束缚 。尽管 Django 模板系统主要用于生成 HTML，它还是被有意地设计为可生成非 HTML 格式，如纯文本。 一些其它的模板语言是基于 XML 的，将所有的模板逻辑置于 XML 标签与属性之中，而 Django 有意地避开了这种限制。 强制要求使用有效 XML 编写模板将会引发大量的人为错误和难以理解的错误信息，而且使用 XML 引擎解析模板也会导致令人无法容忍的模板处理开销。</li>
<li>假定设计师精通 HTML 编码 。模板系统的设计意图并不是为了让模板一定能够很好地显示在 Dreamweaver 这样的所见即所得编辑器中。 这种限制过于苛刻，而且会使得语法不能像目前这样的完美。 Django 要求模板创作人员对直接编辑 HTML 非常熟悉。</li>
<li>假定设计师不是 Python 程序员 。模板系统开发人员认为：模板通常由设计师而非程序员来编写，因此不应被假定拥有Python开发知识</li>
</ol>