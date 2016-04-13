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
<h3 id="数据库配置">数据库配置</h3>
<p>要使用数据库，首先需要做些初始配置；我们需要告诉Django使用什么数据库以及如何连接数据库。<br>
数据库的配置是在<code>settings.py</code><br>
一般包括如下配置：</p>
<pre><code>DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
</code></pre>
<h3 id="在python代码里定义模型">在Python代码里定义模型</h3>
<p>MTV里的M代表模型。Django模型是用Python代码形式表述的数据在数据库中的定义。<br>
Django也使用模型来呈现SQL无法处理的高级概念。<br>
django这样做有下面几个原因：</p>
<ol>
<li>
<p>自省（运行时自动识别数据库）会导致过载和有数据完整性问题。 为了提供方便的数据访问API， Django需要以 某种方式 知道数据库层内部信息，有两种实现方式。 第一种方式是用Python明确地定义数据模型，第二种方式是通过自省来自动侦测识别数据模型。7</p>
</li>
<li>
<p>第二种方式看起来更清晰，因为数据表信息只存放在一个地方-数据库里，但是会带来一些问题。 首先，运行时扫描数据库会带来严重的系统过载。 如果每个请求都要扫描数据库的表结构，或者即便是 服务启动时做一次都是会带来不能接受的系统过载。 （有人认为这个程度的系统过载是可以接受的，而Django开发者的目标是尽可能地降低框架的系统过载）。第二，某些数据库，尤其是老版本的MySQL,并未完整存储那些精确的自省元数据。1</p>
</li>
<li>
<p>编写Python代码是非常有趣的，保持用Python的方式思考会避免你的大脑在不同领域来回切换。 尽可能的保持在单一的编程环境/思想状态下可以帮助你提高生产率。 不得不去重复写SQL，再写Python代码，再写SQL，…，会让你头都要裂了。</p>
</li>
<li>
<p>把数据模型用代码的方式表述来让你可以容易对它们进行版本控制。 这样，你可以很容易了解数据层 的变动情况。</p>
</li>
<li>
<p>SQL只能描述特定类型的数据字段。 例如，大多数数据库都没有专用的字段类型来描述Email地址、URL。 而用Django的模型可以做到这一点。 好处就是<strong>高级的数据类型带来更高的效率和更好的代码复用</strong>。</p>
</li>
<li>
<p>SQL还有在不同数据库平台的兼容性问题。 发布Web应用的时候，使用Python模块描述数据库结构信息可以避免为MySQL, PostgreSQL, and SQLite编写不同的CREATE TABLE。</p>
</li>
</ol>
<blockquote>
<p>当然，这个方法也有一个缺点，就是Python代码和数据库表的同步问题</p>
</blockquote>
<h4 id="第一个模型">第一个模型</h4>
<p>我们来假定下面的这些概念、字段和关系：</p>
<ul>
<li>
<p>一个作者有姓，有名及email地址。</p>
</li>
<li>
<p>出版商有名称，地址，所在城市、省，国家，网站。</p>
</li>
<li>
<p>书籍有书名和出版日期。 它有一个或多个作者（和作者是多对多的关联关系[many-to-many]）， 只有一个出版商（和出版商是一对多的关联关系[one-to-many]，也被称作外键[foreign key]）</p>
</li>
</ul>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span><span class="token number">db</span> <span class="token keyword">import</span> models

<span class="token keyword">class</span> Publisher<span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span>
    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span>
    address <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
    city <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">60</span><span class="token punctuation">)</span>
    state_province <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span>
    country <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">)</span>
    website <span class="token operator">=</span> models<span class="token punctuation">.</span>URLField<span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token keyword">class</span> Author<span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span>
    first_name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span>
    last_name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">40</span><span class="token punctuation">)</span>
    email <span class="token operator">=</span> models<span class="token punctuation">.</span>EmailField<span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token keyword">class</span> Book<span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span>
    title <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">100</span><span class="token punctuation">)</span>
    authors <span class="token operator">=</span> models<span class="token punctuation">.</span>ManyToManyField<span class="token punctuation">(</span>Author<span class="token punctuation">)</span>
    publisher <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span>Publisher<span class="token punctuation">)</span>
    publication_date <span class="token operator">=</span> models<span class="token punctuation">.</span>DateField<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
<p>每个模型相当于单个数据库表，每个属性也是这个表中的一个字段。 属性名就是字段名，它的类型（例如 CharField ）相当于数据库的字段类型 （例如 varchar ）。</p>
<blockquote>
<p>一旦你创建了模型，Django自动为这些模型提供了高级的Python API。 运行 python <a href="http://manage.py">manage.py</a> shell</p>
</blockquote>
<h4 id="添加模块的字符串表现">添加模块的字符串表现</h4>
<p>在使用<code>python manage.py shell</code>访问数据进行打印的时候出现下面的问题：<br>
<code>[&lt;Publisher: Publisher object&gt;, &lt;Publisher: Publisher object&gt;]</code></p>
<p>出现这种情况只需要为Publisher 对象添加一个方法 <code>__unicode__()</code> 。 <code>__unicode__()</code> 方法告诉Python如何将对象以unicode的方式显示出来。 为以上三个模型添加<code>__unicode__()</code>方法后，就可以看到效果了</p>
<p>这里讲到了<code>Unicode对象</code>。<br>
什么是unicode呢？</p>
<ul>
<li>你可以认为unicode对象就是一个Python字符串，它可以处理上百万不同类别的字符——从古老版本的Latin字符到非Latin字符，再到曲折的引用和艰涩的符号。</li>
</ul>