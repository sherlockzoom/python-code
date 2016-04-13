<h1 id="django模型"><a href="http://djangobook.py3k.cn/2.0/chapter05/">django模型</a></h1>
<blockquote>
<p>时下大多数网站都是<code>数据库驱动</code> 的：网站的内容都是存储在关系型数据库中。 这使得数据和逻辑能够彻底地分开（视图和模板也以同样方式对逻辑和显示进行了分隔。)</p>
</blockquote>
<h3 id="在视图中进行数据库查询的笨方法">在视图中进行数据库查询的笨方法</h3>
<p>正如在视图中输出 HTML 的笨方法（通过在视图里对文本直接硬编码HTML），在视图中也有笨方法可以从数据库中获取数据</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render_to_response
<span class="token keyword">import</span> MySQLdb

<span class="token keyword">def</span> book_list<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token number">db</span> <span class="token operator">=</span> MySQLdb<span class="token punctuation">.</span>connect<span class="token punctuation">(</span>user<span class="token operator">=</span><span class="token string">'me'</span><span class="token punctuation">,</span> <span class="token number">db</span><span class="token operator">=</span><span class="token string">'mydb'</span><span class="token punctuation">,</span> passwd<span class="token operator">=</span><span class="token string">'secret'</span><span class="token punctuation">,</span> host<span class="token operator">=</span><span class="token string">'localhost'</span><span class="token punctuation">)</span>
    cursor <span class="token operator">=</span> <span class="token number">db.</span>cursor<span class="token punctuation">(</span><span class="token punctuation">)</span>
    cursor<span class="token punctuation">.</span>execute<span class="token punctuation">(</span><span class="token string">'SELECT name FROM books ORDER BY name'</span><span class="token punctuation">)</span>
    names <span class="token operator">=</span> <span class="token punctuation">[</span>row<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token keyword">for</span> row <span class="token keyword">in</span> cursor<span class="token punctuation">.</span>fetchall<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span>
    <span class="token number">db.</span>close<span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'book_list.html'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">'names'</span><span class="token punctuation">:</span> names<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre>
<blockquote>
<p>这样我们不得不重复同样的代码： 创建数据库连接、创建数据库游标、执行某个语句、然后关闭数据库</p>
</blockquote>
<p>django数据库层致力于解决这些问题。django数据库API重写上面视图</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render_to_response
<span class="token keyword">from</span> mysite<span class="token punctuation">.</span>books<span class="token punctuation">.</span>models <span class="token keyword">import</span> Book

<span class="token keyword">def</span> book_list<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    books <span class="token operator">=</span> Book<span class="token punctuation">.</span>objects<span class="token punctuation">.</span>order_by<span class="token punctuation">(</span><span class="token string">'name'</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'book_list.html'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">'books'</span><span class="token punctuation">:</span> books<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre>
<h3 id="mtv-开发模式">MTV 开发模式</h3>
<p>在钻研更多代码之前，让我们先花点时间考虑下 Django 数据驱动 Web 应用的<strong>总体设计</strong> 。</p>
<blockquote>
<ul>
<li>Django 的设计鼓励松耦合及对应用程序中不同部分的严格分割. 遵循这个理念的话，要想修改应用的某部分而不影响其它部分就比较容易了</li>
<li>把数据存取逻辑、业务逻辑和表现逻辑组合在一起的概念有时被称为软件架构的 <code>Model-View-Controller (MVC)</code>模式。 在这个模式中， Model 代表数据存取层，View 代表的是系统中选择显示什么和怎么显示的部分，Controller 指的是系统中根据用户输入并视需要访问模型，以决定使用哪个视图的那部分</li>
</ul>
</blockquote>
<p>Django 紧紧地遵循这种 MVC 模式，可以称得上是一种 MVC 框架。 以下是 Django 中 M、V 和 C 各自的含义：</p>
<ul>
<li>
<p>M ，数据存取部分，由django数据库层处理，本章要讲述的内容。</p>
</li>
<li>
<p>V ，选择显示哪些数据要显示以及怎样显示的部分，由视图和模板处理。3</p>
</li>
<li>
<p>C ，根据用户输入委派视图的部分，由 Django 框架根据 URLconf 设置，对给定 URL 调用适当的 Python 函数。</p>
</li>
</ul>
<p>由于 C 由框架自行处理，而 Django 里更关注的是模型（Model）、模板(Template)和视图（Views），Django 也被称为 MTV 框架 。在 <code>MTV</code> 开发模式中：</p>
<ul>
<li>
<p>M 代表模型（Model），即数据存取层。 该层处理与数据相关的所有事务： 如何存取、如何验证有效性、包含哪些行为以及数据之间的关系等。</p>
</li>
<li>
<p>T 代表模板(Template)，即表现层。 该层处理与表现相关的决定： 如何在页面或其他类型文档中进行显示。</p>
</li>
<li>
<p>V 代表视图（View），即业务逻辑层。 该层包含存取模型及调取恰当模板的相关逻辑。 你可以把它看作模型与模板之间的桥梁。</p>
</li>
</ul>