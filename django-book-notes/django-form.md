<h1 id="表单">表单</h1>
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