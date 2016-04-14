<h1 id="表单">表单</h1>
<div class="toc"><ul><li><a href="#表单">表单</a><ul><li><ul><li><a href="#从request对象中获取数据">从Request对象中获取数据</a><ul><li><a href="#url相关信息">URL相关信息</a></li><li><a href="#有关request的其它信息">有关request的其它信息</a></li><li><a href="#提交的数据信息">提交的数据信息</a></li><li><a href="#一个简单的表单处理示例">一个简单的表单处理示例</a></li><li><a href="#改进表单">改进表单</a></li><li><a href="#简单的验证">简单的验证</a></li><li><a href="#编写contact表单">编写Contact表单</a></li></ul></li><li><a href="#第一个form类">第一个Form类</a></li></ul></li></ul></li></ul></div><p><a href="http://djangobook.py3k.cn/2.0/chapter07/">http://djangobook.py3k.cn/2.0/chapter07/</a></p>
<p>这里介绍如何用django对用户通过表单提交的数据进行访问、有效性检查以及其他处理。</p>
<h3 id="从request对象中获取数据">从<code>Request</code>对象中获取数据</h3>
<blockquote>
<p>每个view函数的第一个参数是一个HttpRequest对象，就像下面这个hello()函数:</p>
</blockquote>
<pre><code>from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world")
</code></pre>
<h4 id="url相关信息">URL相关信息</h4>
<table>
<thead>
<tr>
<th>属性/方法</th>
<th>说明</th>
<th>举例</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>request.path</code></td>
<td>除域名以外的请求路径</td>
<td><code>/hello/</code></td>
</tr>
<tr>
<td><code>request.get_host()</code></td>
<td>主机名（比如，通常说的域名）</td>
<td><code>127.0.0.1:8000</code> or <code>www.example.com</code></td>
</tr>
<tr>
<td><code>request.get_full_path()</code></td>
<td>请求路径，可能包含查询字符串</td>
<td><code>/hello/?print=true</code></td>
</tr>
<tr>
<td><code>request.is_secure()</code></td>
<td>如果通过HTTPS访问，则此方法返回true，否则 false</td>
<td><code>True</code> or <code>False</code></td>
</tr>
</tbody>
</table>
<h4 id="有关request的其它信息">有关request的其它信息</h4>
<p><code>request.META</code> 是一个Python字典，包含了所有本次HTTP请求的Header信息，比如用户IP地址和用户Agent（通常是浏览器的名称和版本号）。 注意，Header信息的完整列表取决于用户所发送的Header信息和服务器端设置的Header信息。</p>
<ul>
<li><code>HTTP_REFERER</code>，进站前链接网页，如果有的话。</li>
<li><code>HTTP_USER_AGENT</code>，用户浏览器的user-agent字符串，如果有的话。 例如： "<code>Mozilla/5.0 (X11; U; Linux i686; fr-FR; rv:1.8.1.17) Gecko/20080829 Firefox/2.0.0.17"</code> .</li>
<li><code>REMOTE_ADDR</code> 客户端IP，如：<code>12.345.67.89</code>"。(如果申请是经过代理服务器的话，那么它可能是以逗号分割的多个IP地址，如：<code>12.345.67.89,23.456.78.90</code> 。)</li>
</ul>
<p>当你试图访问一个不存在的键时，会触发一个<code>KeyError</code>异常。</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token comment" spellcheck="true"># BAD!
</span><span class="token keyword">def</span> ua_display_bad<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    ua <span class="token operator">=</span> request<span class="token punctuation">.</span>META<span class="token punctuation">[</span><span class="token string">'HTTP_USER_AGENT'</span><span class="token punctuation">]</span>  <span class="token comment" spellcheck="true"># Might raise KeyError!
</span>    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span><span class="token string">"Your browser is %s"</span> <span class="token operator">%</span> ua<span class="token punctuation">)</span>

<span class="token comment" spellcheck="true"># GOOD (VERSION 1)
</span><span class="token keyword">def</span> ua_display_good1<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">try</span><span class="token punctuation">:</span>
        ua <span class="token operator">=</span> request<span class="token punctuation">.</span>META<span class="token punctuation">[</span><span class="token string">'HTTP_USER_AGENT'</span><span class="token punctuation">]</span>
    <span class="token keyword">except</span> KeyError<span class="token punctuation">:</span>
        ua <span class="token operator">=</span> <span class="token string">'unknown'</span>
    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span><span class="token string">"Your browser is %s"</span> <span class="token operator">%</span> ua<span class="token punctuation">)</span>

<span class="token comment" spellcheck="true"># GOOD (VERSION 2)
</span><span class="token keyword">def</span> ua_display_good2<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    ua <span class="token operator">=</span> request<span class="token punctuation">.</span>META<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'HTTP_USER_AGENT'</span><span class="token punctuation">,</span> <span class="token string">'unknown'</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span><span class="token string">"Your browser is %s"</span> <span class="token operator">%</span> ua<span class="token punctuation">)</span>
</code></pre>
<p>写一个简单的view函数来显示 request.META 的所有数据，这样你就知道里面有什么了</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">def</span> display_meta<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    values <span class="token operator">=</span> request<span class="token punctuation">.</span>META<span class="token punctuation">.</span>items<span class="token punctuation">(</span><span class="token punctuation">)</span>
    values<span class="token punctuation">.</span>sort<span class="token punctuation">(</span><span class="token punctuation">)</span>
    html <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
    <span class="token keyword">for</span> k<span class="token punctuation">,</span> v <span class="token keyword">in</span> values<span class="token punctuation">:</span>
        html<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'&lt;tr&gt;&lt;td&gt;%s&lt;/td&gt;&lt;td&gt;%s&lt;/td&gt;&lt;/tr&gt;'</span> <span class="token operator">%</span> <span class="token punctuation">(</span>k<span class="token punctuation">,</span> v<span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> HttpResponse<span class="token punctuation">(</span><span class="token string">'&lt;table&gt;%s&lt;/table&gt;'</span> <span class="token operator">%</span> <span class="token string">'\n'</span><span class="token punctuation">.</span>join<span class="token punctuation">(</span>html<span class="token punctuation">)</span><span class="token punctuation">)</span>
</code></pre>
<h4 id="提交的数据信息">提交的数据信息</h4>
<blockquote>
<ul>
<li>除了基本的元数据，HttpRequest对象还有两个属性包含了用户所提交的信息： request.GET 和 request.POST。二者都是类字典对象，你可以通过它们来访问GET和POST数据</li>
<li>POST数据是来自HTML中的〈form〉标签提交的，而GET数据可能来自〈form〉提交也可能是URL中的查询字符串(the query string)</li>
</ul>
</blockquote>
<h4 id="一个简单的表单处理示例">一个简单的表单处理示例</h4>
<p>views</p>
<pre><code># views.py

def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
</code></pre>
<p><code>search_form.html</code></p>
<pre><code>&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Search&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;form action="/search/" method="get"&gt;
        &lt;input type="text" name="q"&gt;
        &lt;input type="submit" value="Search"&gt;
    &lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p><code>urls.py</code></p>
<pre class=" language-py"><code class="prism  language-py">	<span class="token keyword">from</span> mysite<span class="token punctuation">.</span>books <span class="token keyword">import</span> views

	urlpatterns <span class="token operator">=</span> patterns<span class="token punctuation">(</span><span class="token string">''</span><span class="token punctuation">,</span>
	    <span class="token comment" spellcheck="true"># ...
</span>	    <span class="token punctuation">(</span>r<span class="token string">'^search-form/$'</span><span class="token punctuation">,</span> views<span class="token punctuation">.</span>search_form<span class="token punctuation">)</span><span class="token punctuation">,</span>
	    <span class="token comment" spellcheck="true"># ...
</span>	<span class="token punctuation">)</span>
</code></pre>
<p>获取使用POST方法的数据与GET的相似，只是使用request.POST代替了request.GET。那么，POST与GET之间有什么不同？当我们提交表单仅仅需要获取数据时就可以用GET； 而当我们提交表单时需要更改服务器数据的状态，或者说发送e-mail，或者其他不仅仅是获取并显示数据的时候就使用POST</p>
<h4 id="改进表单">改进表单</h4>
<p>检测到空字符串时更好的解决方法是重新显示表单，并在表单上面给出错误提示以便用户立刻重新填写。<br>
<code>views.py</code></p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>http <span class="token keyword">import</span> HttpResponse
<span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render_to_response
<span class="token keyword">from</span> mysite<span class="token punctuation">.</span>books<span class="token punctuation">.</span>models <span class="token keyword">import</span> Book

<span class="token keyword">def</span> search_form<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_form.html'</span><span class="token punctuation">)</span>

<span class="token keyword">def</span> search<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">if</span> <span class="token string">'q'</span> <span class="token keyword">in</span> request<span class="token punctuation">.</span>GET <span class="token operator">and</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">[</span><span class="token string">'q'</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
        q <span class="token operator">=</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">[</span><span class="token string">'q'</span><span class="token punctuation">]</span>
        books <span class="token operator">=</span> Book<span class="token punctuation">.</span>objects<span class="token punctuation">.</span>filter<span class="token punctuation">(</span>title__icontains<span class="token operator">=</span>q<span class="token punctuation">)</span>
        <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_results.html'</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span><span class="token string">'books'</span><span class="token punctuation">:</span> books<span class="token punctuation">,</span> <span class="token string">'query'</span><span class="token punctuation">:</span> q<span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token keyword">else</span><span class="token punctuation">:</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_form.html'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">'error'</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token operator">*</span><span class="token operator">*</span>
</code></pre>
<p>进来<code>search()</code>视图：在字符串为空时重新显示<code>search_form.html</code>。 并且给这个模板传递了一个变量error，记录着错误提示信息<br>
<code>search_form.html</code></p>
<pre class=" language-py"><code class="prism  language-py"><span class="token operator">&lt;</span>html<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>head<span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span>title<span class="token operator">&gt;</span>Search<span class="token operator">&lt;</span><span class="token operator">/</span>title<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>head<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>body<span class="token operator">&gt;</span>
    <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> error <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token operator">&lt;</span>p style<span class="token operator">=</span><span class="token string">"color: red;"</span><span class="token operator">&gt;</span>Please submit <span class="token number">a</span> search term<span class="token punctuation">.</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token operator">&lt;</span>form action<span class="token operator">=</span><span class="token string">"/search/"</span> method<span class="token operator">=</span><span class="token string">"get"</span><span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"text"</span> name<span class="token operator">=</span><span class="token string">"q"</span><span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"submit"</span> value<span class="token operator">=</span><span class="token string">"Search"</span><span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span><span class="token operator">/</span>form<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>body<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>html<span class="token operator">&gt;</span>
</code></pre>
<p>通过上面的一些修改，现在程序变的好多了，但是现在出现一个问题： 是否有必要专门编写search_form()来显示表单？ 按实际情况来说，当一个请求发送至/search/（未包含GET的数据）后将会显示一个空的表单（带有错误信息）。 所以，只要我们改变search()视图：当用户访问/search/并未提交任何数据时就隐藏错误信息，这样就移去search_form()视图以及对应的URLpattern。</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">def</span> search<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    error <span class="token operator">=</span> <span class="token boolean">False</span>
    <span class="token keyword">if</span> <span class="token string">'q'</span> <span class="token keyword">in</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">:</span>
        q <span class="token operator">=</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">[</span><span class="token string">'q'</span><span class="token punctuation">]</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> q<span class="token punctuation">:</span>
            error <span class="token operator">=</span> <span class="token boolean">True</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            books <span class="token operator">=</span> Book<span class="token punctuation">.</span>objects<span class="token punctuation">.</span>filter<span class="token punctuation">(</span>title__icontains<span class="token operator">=</span>q<span class="token punctuation">)</span>
            <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_results.html'</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span><span class="token string">'books'</span><span class="token punctuation">:</span> books<span class="token punctuation">,</span> <span class="token string">'query'</span><span class="token punctuation">:</span> q<span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_form.html'</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span><span class="token string">'error'</span><span class="token punctuation">:</span> error<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre>
<p>最后，我们再稍微改进一下这个表单，去掉冗余的部分。 既然已经将两个视图与URLs合并起来，/search/视图管理着表单的显示以及结果的显示，那么在search_form.html里表单的action值就没有必要硬编码的指定URL。 原先的代码是这样：</p>
<pre><code>&lt;form action="/search/" method="get"&gt;
</code></pre>
<p>现在改成这样：</p>
<pre><code>&lt;form action="" method="get"&gt;
</code></pre>
<blockquote>
<p><code>action=""</code>意味着表单将提交给与当前页面相同的URL。这样修改之后，如果<code>search（）</code>视图不指向其他页面的话，你将不必再修改<code>action</code></p>
</blockquote>
<h4 id="简单的验证">简单的验证</h4>
<ul>
<li>HTML表单包含着比检测值是否为空更为复杂的验证</li>
<li>可以使用Javascript在客户端浏览器里对数据进行验证</li>
</ul>
<pre class=" language-py"><code class="prism  language-py"><span class="token comment" spellcheck="true"># views.py
</span><span class="token keyword">def</span> search<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token operator">*</span><span class="token operator">*</span>errors <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token keyword">if</span> <span class="token string">'q'</span> <span class="token keyword">in</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">:</span>
        q <span class="token operator">=</span> request<span class="token punctuation">.</span>GET<span class="token punctuation">[</span><span class="token string">'q'</span><span class="token punctuation">]</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> q<span class="token punctuation">:</span>
            <span class="token operator">*</span><span class="token operator">*</span>errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a search term.'</span><span class="token punctuation">)</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token keyword">elif</span> len<span class="token punctuation">(</span>q<span class="token punctuation">)</span> <span class="token operator">&gt;</span> <span class="token number">20</span><span class="token punctuation">:</span>
            <span class="token operator">*</span><span class="token operator">*</span>errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Please enter at most 20 characters.'</span><span class="token punctuation">)</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            books <span class="token operator">=</span> Book<span class="token punctuation">.</span>objects<span class="token punctuation">.</span>filter<span class="token punctuation">(</span>title__icontains<span class="token operator">=</span>q<span class="token punctuation">)</span>
            <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_results.html'</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span><span class="token string">'books'</span><span class="token punctuation">:</span> books<span class="token punctuation">,</span> <span class="token string">'query'</span><span class="token punctuation">:</span> q<span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'search_form.html'</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span><span class="token operator">*</span><span class="token operator">*</span><span class="token string">'errors'</span><span class="token punctuation">:</span> errors<span class="token operator">*</span><span class="token operator">*</span> <span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token comment" spellcheck="true"># search_form.html
</span><span class="token operator">&lt;</span>html<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>head<span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span>title<span class="token operator">&gt;</span>Search<span class="token operator">&lt;</span><span class="token operator">/</span>title<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>head<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>body<span class="token operator">&gt;</span>
    <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> errors <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token operator">&lt;</span>ul<span class="token operator">&gt;</span><span class="token operator">*</span><span class="token operator">*</span>
            <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">for</span> error <span class="token keyword">in</span> errors <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
            <span class="token operator">*</span><span class="token operator">*</span><span class="token operator">&lt;</span>li<span class="token operator">&gt;</span><span class="token punctuation">{</span><span class="token punctuation">{</span> error <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token operator">&lt;</span><span class="token operator">/</span>li<span class="token operator">&gt;</span><span class="token operator">*</span><span class="token operator">*</span>
            <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> endfor <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token operator">&lt;</span><span class="token operator">/</span>ul<span class="token operator">&gt;</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token operator">&lt;</span>form action<span class="token operator">=</span><span class="token string">"/search/"</span> method<span class="token operator">=</span><span class="token string">"get"</span><span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"text"</span> name<span class="token operator">=</span><span class="token string">"q"</span><span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"submit"</span> value<span class="token operator">=</span><span class="token string">"Search"</span><span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span><span class="token operator">/</span>form<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>body<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>html<span class="token operator">&gt;</span>
</code></pre>
<h4 id="编写contact表单">编写Contact表单</h4>
<blockquote>
<p>这个表单包括用户提交的反馈信息，一个可选的e-mail回信地址。 当这个表单提交并且数据通过验证后，系统将自动发送一封包含题用户提交的信息的e-mail给站点工作人员<br>
<code>contact_form.html</code></p>
</blockquote>
<pre class=" language-html"><code class="prism  language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>head</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>title</span><span class="token punctuation">&gt;</span></span>Contact us<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>title</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>head</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>body</span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>h1</span><span class="token punctuation">&gt;</span></span>Contact us<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>h1</span><span class="token punctuation">&gt;</span></span>

    {% if errors %}
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>ul</span><span class="token punctuation">&gt;</span></span>
            {% for error in errors %}
            <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>li</span><span class="token punctuation">&gt;</span></span>{{ error }}<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>li</span><span class="token punctuation">&gt;</span></span>
            {% endfor %}
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>ul</span><span class="token punctuation">&gt;</span></span>
    {% endif %}

    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>form</span> <span class="token attr-name">action</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>/contact/<span class="token punctuation">"</span></span> <span class="token attr-name">method</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>post<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Subject: <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>input</span> <span class="token attr-name">type</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text<span class="token punctuation">"</span></span> <span class="token attr-name">name</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>subject<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Your e-mail (optional): <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>input</span> <span class="token attr-name">type</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text<span class="token punctuation">"</span></span> <span class="token attr-name">name</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>email<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span>Message: <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>textarea</span> <span class="token attr-name">name</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>message<span class="token punctuation">"</span></span> <span class="token attr-name">rows</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>10<span class="token punctuation">"</span></span> <span class="token attr-name">cols</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>50<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>textarea</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>input</span> <span class="token attr-name">type</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>submit<span class="token punctuation">"</span></span> <span class="token attr-name">value</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>Submit<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>
    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>form</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>body</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span>
</code></pre>
<p>contact视图应该是下面这个样子的：</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django<span class="token punctuation">.</span>core<span class="token punctuation">.</span>mail <span class="token keyword">import</span> send_mail
<span class="token keyword">from</span> django<span class="token punctuation">.</span>http <span class="token keyword">import</span> HttpResponseRedirect
<span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render_to_response

<span class="token keyword">def</span> contact<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    errors <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
    <span class="token keyword">if</span> request<span class="token punctuation">.</span>method <span class="token operator">==</span> <span class="token string">'POST'</span><span class="token punctuation">:</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'subject'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a subject.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'message'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a message.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'email'</span><span class="token punctuation">)</span> <span class="token operator">and</span> <span class="token string">'@'</span> <span class="token operator">not</span> <span class="token keyword">in</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'email'</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a valid e-mail address.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> errors<span class="token punctuation">:</span>
            send_mail<span class="token punctuation">(</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'subject'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'message'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'email'</span><span class="token punctuation">,</span> <span class="token string">'noreply@example.com'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                <span class="token punctuation">[</span><span class="token string">'siteowner@example.com'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token punctuation">)</span>
            <span class="token keyword">return</span> HttpResponseRedirect<span class="token punctuation">(</span><span class="token string">'/contact/thanks/'</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'contact_form.html'</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span><span class="token string">'errors'</span><span class="token punctuation">:</span> errors<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre>
<p>下面来分析一下上面的代码：</p>
<ul>
<li>
<p>确认request.method的值是’POST’。用户浏览表单时这个值并不存在，当且仅当表单被提交时这个值才出现。 （在后面的例子中，request.method将会设置为’GET’，因为在普通的网页浏览中，浏览器都使用GET，而非POST）。判断request.method的值很好地帮助我们将表单显示与表单处理隔离开来。</p>
</li>
<li>
<p>我们使用request.POST代替request.GET来获取提交过来的数据。 这是必须的，因为contact_form.html里表单使用的是method=”post”。如果在视图里通过POST获取数据，那么request.GET将为空。1</p>
</li>
<li>
<p>这里，有两个必填项，subject 和 message，所以需要对这两个进行验证。 注意，我们使用request.POST.get()方法，并提供一个空的字符串作为默认值；这个方法很好的解决了键丢失与空数据问题。</p>
</li>
<li>
<p>虽然email非必填项，但如果有提交她的值则我们也需进行验证。 我们的验证算法相当的薄弱，仅验证值是否包含@字符。 在实际应用中，需要更为健壮的验证机制（Django提供这些验证机制，稍候我们就会看到）。</p>
</li>
<li>
<p>我们使用了django.core.mail.send_mail函数来发送e-mail。 这个函数有四个必选参数： 主题，正文，寄信人和收件人列表。 send_mail是Django的EmailMessage类的一个方便的包装，EmailMessage类提供了更高级的方法，比如附件，多部分邮件，以及对于邮件头部的完整控制。</p>
</li>
<li>
<p>注意，若要使用send_mail()函数来发送邮件，那么服务器需要配置成能够对外发送邮件，并且在Django中设置出站服务器地址。 参见规范：<a href="http://docs.djangoproject.com/en/dev/topics/email/">http://docs.djangoproject.com/en/dev/topics/email/</a></p>
</li>
<li>
<p>当邮件发送成功之后，我们使用HttpResponseRedirect对象将网页重定向至一个包含成功信息的页面。 包含成功信息的页面这里留给读者去编写（很简单 一个视图/URL映射/一份模板即可），但是我们要解释一下为何重定向至新的页面，而不是在模板中直接调用render_to_response()来输出。</p>
</li>
<li>
<p>原因就是： 若用户刷新一个包含POST表单的页面，那么请求将会重新发送造成重复。 这通常会造成非期望的结果，比如说重复的数据库记录；在我们的例子中，将导致发送两封同样的邮件。 如果用户在POST表单之后被重定向至另外的页面，就不会造成重复的请求了。</p>
</li>
<li>
<p>我们应每次都给成功的POST请求做重定向。 这就是web开发的最佳实践</p>
</li>
</ul>
<blockquote>
<p>一个问题是表单的重新显示。若数据验证失败后，返回客户端的表单中各字段最好是填有原来提交的数据</p>
</blockquote>
<pre class=" language-py"><code class="prism  language-py"><span class="token comment" spellcheck="true"># views.py
</span>
<span class="token keyword">def</span> contact<span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span>
    errors <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
    <span class="token keyword">if</span> request<span class="token punctuation">.</span>method <span class="token operator">==</span> <span class="token string">'POST'</span><span class="token punctuation">:</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'subject'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a subject.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'message'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a message.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'email'</span><span class="token punctuation">)</span> <span class="token operator">and</span> <span class="token string">'@'</span> <span class="token operator">not</span> <span class="token keyword">in</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'email'</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
            errors<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token string">'Enter a valid e-mail address.'</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> <span class="token operator">not</span> errors<span class="token punctuation">:</span>
            send_mail<span class="token punctuation">(</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'subject'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">[</span><span class="token string">'message'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'email'</span><span class="token punctuation">,</span> `<span class="token string">'noreply@example.com`_'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                <span class="token punctuation">[</span>`<span class="token string">'siteowner@example.com`_'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token punctuation">)</span>
            <span class="token keyword">return</span> HttpResponseRedirect<span class="token punctuation">(</span><span class="token string">'/contact/thanks/'</span><span class="token punctuation">)</span>
    <span class="token keyword">return</span> render_to_response<span class="token punctuation">(</span><span class="token string">'contact_form.html'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
        <span class="token string">'errors'</span><span class="token punctuation">:</span> errors<span class="token punctuation">,</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token string">'subject'</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'subject'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">,</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token string">'message'</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'message'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">,</span><span class="token operator">*</span><span class="token operator">*</span>
        <span class="token operator">*</span><span class="token operator">*</span><span class="token string">'email'</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>POST<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'email'</span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">,</span><span class="token operator">*</span><span class="token operator">*</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>

<span class="token comment" spellcheck="true"># contact_form.html
</span>
<span class="token operator">&lt;</span>html<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>head<span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span>title<span class="token operator">&gt;</span>Contact us<span class="token operator">&lt;</span><span class="token operator">/</span>title<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>head<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span>body<span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span>h1<span class="token operator">&gt;</span>Contact us<span class="token operator">&lt;</span><span class="token operator">/</span>h1<span class="token operator">&gt;</span>

    <span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">if</span> errors <span class="token operator">%</span><span class="token punctuation">}</span>
        <span class="token operator">&lt;</span>ul<span class="token operator">&gt;</span>
            <span class="token punctuation">{</span><span class="token operator">%</span> <span class="token keyword">for</span> error <span class="token keyword">in</span> errors <span class="token operator">%</span><span class="token punctuation">}</span>
            <span class="token operator">&lt;</span>li<span class="token operator">&gt;</span><span class="token punctuation">{</span><span class="token punctuation">{</span> error <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token operator">&lt;</span><span class="token operator">/</span>li<span class="token operator">&gt;</span>
            <span class="token punctuation">{</span><span class="token operator">%</span> endfor <span class="token operator">%</span><span class="token punctuation">}</span>
        <span class="token operator">&lt;</span><span class="token operator">/</span>ul<span class="token operator">&gt;</span>
    <span class="token punctuation">{</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">}</span>

    <span class="token operator">&lt;</span>form action<span class="token operator">=</span><span class="token string">"/contact/"</span> method<span class="token operator">=</span><span class="token string">"post"</span><span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Subject<span class="token punctuation">:</span> <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"text"</span> name<span class="token operator">=</span><span class="token string">"subject"</span> <span class="token operator">*</span><span class="token operator">*</span>value<span class="token operator">=</span><span class="token string">"{{ subject }}"</span><span class="token operator">*</span><span class="token operator">*</span> <span class="token operator">&gt;</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Your <span class="token number">e</span><span class="token operator">-</span>mail <span class="token punctuation">(</span>optional<span class="token punctuation">)</span><span class="token punctuation">:</span> <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"text"</span> name<span class="token operator">=</span><span class="token string">"email"</span> <span class="token operator">*</span><span class="token operator">*</span>value<span class="token operator">=</span><span class="token string">"{{ email }}"</span><span class="token operator">*</span><span class="token operator">*</span> <span class="token operator">&gt;</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>p<span class="token operator">&gt;</span>Message<span class="token punctuation">:</span> <span class="token operator">&lt;</span>textarea name<span class="token operator">=</span><span class="token string">"message"</span> rows<span class="token operator">=</span><span class="token string">"10"</span> cols<span class="token operator">=</span><span class="token string">"50"</span><span class="token operator">&gt;</span><span class="token operator">*</span><span class="token operator">*</span><span class="token punctuation">{</span><span class="token punctuation">{</span> message <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token operator">*</span><span class="token operator">*</span><span class="token operator">&lt;</span><span class="token operator">/</span>textarea<span class="token operator">&gt;</span><span class="token operator">&lt;</span><span class="token operator">/</span>p<span class="token operator">&gt;</span>
        <span class="token operator">&lt;</span>input type<span class="token operator">=</span><span class="token string">"submit"</span> value<span class="token operator">=</span><span class="token string">"Submit"</span><span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span><span class="token operator">/</span>form<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>body<span class="token operator">&gt;</span>
<span class="token operator">&lt;</span><span class="token operator">/</span>html<span class="token operator">&gt;</span>
</code></pre>
<blockquote>
<p>这看起来杂乱，且写的时候容易出错。 希望你开始明白使用高级库的用意——<strong>负责处理表单</strong>及<strong>相关校验任务</strong>。</p>
</blockquote>
<h3 id="第一个form类">第一个Form类</h3>
<blockquote>
<p>表单框架最主要的用法是，为每一个将要处理的HTML的<code>&lt;Form&gt;</code> 定义一个Form类</p>
</blockquote>
<p>社区的惯例是把Form类都放到一个文件中：<code>forms.py</code>。在存放<code>views.py</code> 的目录中，创建这个文件，然后输入：</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">from</span> django <span class="token keyword">import</span> forms

<span class="token keyword">class</span> ContactForm<span class="token punctuation">(</span>forms<span class="token punctuation">.</span>Form<span class="token punctuation">)</span><span class="token punctuation">:</span>
    subject <span class="token operator">=</span> forms<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span><span class="token punctuation">)</span>
    email <span class="token operator">=</span> forms<span class="token punctuation">.</span>EmailField<span class="token punctuation">(</span>required<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
    message <span class="token operator">=</span> forms<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>