<h1 id="迭代器和生成器简介">迭代器和生成器简介</h1>
<div class="toc"><ul><li><a href="#迭代器和生成器简介">迭代器和生成器简介</a><ul><li><a href="#迭代器">迭代器</a></li><li><a href="#生成器">生成器</a><ul><li><a href="#循环生成器生成器推导式">循环生成器(生成器推导式)</a></li><li><a href="#递归生成器">递归生成器</a></li></ul></li></ul></li></ul></div><h2 id="迭代器">迭代器</h2>
<p>迭代的意思是重复做一些事很多次，就像在循环中做的那样。python的基础教程里面常见的是对字典和序列进行迭代，但实际上也能对其他对象进行迭代：只要该对象实现了<code>__iter__</code>方法。（典型的<a href="https://zh.wikipedia.org/wiki/%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B">鸭子类型</a>）</p>
<p><code>__iter__</code>方法会返回一个迭代器，也就是具有<code>__next__</code>方法的对象。调用next方法就会访问下一个值。</p>
<blockquote>
<p>迭代器规则的关键是什么？ 为什么不使用列表？</p>
</blockquote>
<p>因为列表杀伤力太大了。如果一个函数能够一个接一个的计算值，那么使用时可能是计算一次获取一个值—而不是通过列表获取所有值。好处当然在于不会占用太多内存。其他一些理由：使用迭代器更通用、更简单、更优雅。</p>
<p>看一个经典的”菲波拉契数列“，使用迭代器：</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">class</span> Fibs<span class="token punctuation">:</span>
	<span class="token keyword">def</span> __init__<span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
		self<span class="token punctuation">.</span><span class="token number">a</span> <span class="token operator">=</span> <span class="token number">0</span>
		self<span class="token punctuation">.</span><span class="token number">b</span> <span class="token operator">=</span> <span class="token number">1</span>
	<span class="token keyword">def</span> __next__<span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
		self<span class="token punctuation">.</span><span class="token number">a</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span><span class="token number">b</span> <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token number">b</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span><span class="token number">a</span><span class="token operator">+</span>self<span class="token punctuation">.</span><span class="token number">b</span>
	<span class="token keyword">def</span> __iter__<span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
		<span class="token keyword">return</span> self
</code></pre>
<p>调用过程</p>
<pre><code>&gt;&gt;&gt;fibs = Fibs()
&gt;&gt;&gt;for f in fibs:
		if f&gt;1000:
			print f
			break
</code></pre>
<p>内建函数<code>iter</code>可以从可迭代的对象中获得迭代器</p>
<pre class=" language-py"><code class="prism  language-py">it <span class="token operator">=</span> iter<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">3</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
it<span class="token punctuation">.</span>next<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment" spellcheck="true">#output: 1
</span>it<span class="token punctuation">.</span>next<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment" spellcheck="true">#output:2
</span></code></pre>
<p>除了在迭代器和可迭代对象上进行迭代，还能把它们转换为序列。比如使用list构造方法显式的转化为列表。</p>
<h2 id="生成器">生成器</h2>
<p>生成器是一种用普通的函数语法定义的迭代器。生成器可以帮助我们写出非常优雅的代码。它的工作方式可以例子来很好的展现。让我们看看它是怎样创建和使用的。</p>
<pre class=" language-py"><code class="prism  language-py">nested <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">6</span><span class="token punctuation">]</span><span class="token punctuation">]</span> <span class="token comment" spellcheck="true">#没错这是一个列表的列表
</span><span class="token comment" spellcheck="true"># 我们希望能按照顺序打印出列表中的数字
</span>
<span class="token keyword">def</span> flatten<span class="token punctuation">(</span>nested<span class="token punctuation">)</span><span class="token punctuation">:</span>
	<span class="token keyword">for</span> sublist <span class="token keyword">in</span> nested<span class="token punctuation">:</span>
		<span class="token keyword">for</span> element <span class="token keyword">in</span> sublist<span class="token punctuation">:</span>
			<span class="token keyword">yield</span> element   <span class="token comment" spellcheck="true"># 注意这里不是print element
</span></code></pre>
<blockquote>
<p>任何包含<code>yield</code>语句的函数称为生成器 。除了名字不同以外，它的行为和普通的函数也很有差别，它不像<code>return</code>那样返回值，而每次产生多个值。每次产生一个值，函数就会被 <strong>冻结</strong> ：即函数停在那点等待被重新唤醒。唤醒后从停止点开始执行。</p>
</blockquote>
<pre><code>&gt;&gt;&gt;nested = [[1, 2], [3, 4], [5, 6]]
&gt;&gt;&gt;for num in flatten(nested):
		print num
1
2
3
...
6
or
&gt;&gt;&gt;list(flatten(nested))
[1, 2, 3, 4, 5, 6]
</code></pre>
<h3 id="循环生成器生成器推导式">循环生成器(生成器推导式)</h3>
<p>和列表推导式不同在于圆括号的使用方式。更秒的地方在于生成器推导式可以在当前圆括号内直接使用：<br>
<code>sum(i**2 for i in range(10))</code></p>
<pre><code>&gt;&gt;&gt;g=((i+2)**2 for i in range(2,27))
&gt;&gt;&gt;g.next()
16
</code></pre>
<h3 id="递归生成器">递归生成器</h3>
<p>前面创建生成器使用了2层嵌套，那么任意层嵌套呢？</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">def</span> flatten<span class="token punctuation">(</span>nested<span class="token punctuation">)</span><span class="token punctuation">:</span>
	<span class="token keyword">try</span><span class="token punctuation">:</span>
		<span class="token keyword">for</span> sublist <span class="token keyword">in</span> nested<span class="token punctuation">:</span>
			<span class="token keyword">for</span> element <span class="token keyword">in</span> flatten<span class="token punctuation">(</span>sublist<span class="token punctuation">)</span><span class="token punctuation">:</span> <span class="token comment" spellcheck="true"># 
</span>				<span class="token keyword">yield</span> element
	<span class="token keyword">except</span> TypeError<span class="token punctuation">:</span>
		<span class="token keyword">yield</span> nested
</code></pre>
<p>更多的生成器可参考《python基础教程》</p>
<hr>
<pre><code>The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
</code></pre>