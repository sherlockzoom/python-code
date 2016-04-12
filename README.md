<h1 id="python常用模块">python常用模块</h1>
<div class="toc"><ul><li><a href="#python常用模块">python常用模块</a><ul><li><a href="#os模块">os模块</a></li><li><a href="#sys模块">sys模块</a></li><li><a href="#math-模块">math 模块</a></li><li><a href="#collections模块">collections模块</a></li><li><a href="#heapq模块">heapq模块</a></li></ul></li></ul></div><h2 id="os模块">os模块</h2>
<p><code>os.sep</code>                     可以取代操作系统特定的路径分割符。<br>
<code>os.name</code>                  字符串指示你正在使用的平台。比如对于Windows，它是’nt’，而对于Linux/Unix用户，它是’posix’。<br>
<code>os.getcwd()</code>              函数得到当前工作目录，即当前Python脚本工作的目录路径。<br>
<code>os.getenv()</code>              和<code>os.putenv()</code>函数分别用来读取和设置环境变量。<br>
<code>os.listdir()</code>                返回指定目录下的所有文件和目录名。<br>
<code>os.remove()</code>              函数用来删除一个文件。<br>
<code>os.system()</code>              函数用来运行shell命令。<br>
<code>os.linesep</code>                字符串给出当前平台使用的行终止符。例如，Windows使用<code>'\r\n'</code>，Linux使用’<code>\n'</code>而Mac使用<code>'\r'</code>。<br>
<code>os.listdir(dirname)</code>     列出dirname下的目录和文件<br>
<code>os.getcwd()</code>              获得当前工作目录<br>
<code>os.curdir</code>                   返回当前目录（’.’)<br>
<code>os.chdir(dirname)</code>      改变工作目录到dirname</p>
<p><code>os.path.abspath(path)</code>             返回绝对路径<br>
<code>os.path.basename(path)</code>          返回文件名<br>
<code>os.path.commonprefix(list)</code>       返回list(多个路径)中，所有path共有的最长的路径。<br>
<code>os.path.dirname(path)</code>             返回文件路径<br>
<code>os.path.exists(path)</code>                路径存在则返回True,路径损坏返回False<br>
<code>os.path.lexists</code>                        路径存在则返回True,路径损坏也返回True<br>
<code>os.path.expanduser(path)</code>         把path中包含的"<sub>"和"</sub>user"转换成用户目录<br>
<code>os.path.expandvars(path)</code>        根据环境变量的值替换path中包含的”<code>$name”</code>和<code>”${name}”</code><br>
<code>os.path.getatime(path)</code>           返回最后一次进入此path的时间。<br>
<code>os.path.getmtime(path)</code>          返回在此path下最后一次修改的时间。<br>
<code>os.path.getctime(path)</code>            返回path的大小<br>
<code>os.path.getsize(path)</code>             返回文件大小，如果文件不存在就返回错误<br>
<code>os.path.isabs(path)</code>                判断是否为绝对路径<br>
<code>os.path.isfile(path)</code>                 判断路径是否为文件<br>
<code>os.path.isdir(path)</code>                  判断路径是否为目录<br>
<code>os.path.islink(path)</code>                判断路径是否为链接<br>
<code>os.path.ismount(path)</code>             判断路径是否为挂载点（）<br>
<code>os.path.join(path1[, path2[, ...]])</code>   把目录和文件名合成一个路径<br>
<code>os.path.normcase(path)</code>            转换path的大小写和斜杠<br>
<code>os.path.normpath(path)</code>            规范path字符串形式<br>
<code>os.path.realpath(path)</code>              返回path的真实路径<br>
<code>os.path.relpath(path[, start])</code>     从start开始计算相对路径<br>
<code>os.path.samefile(path1, path2)</code>  判断目录或文件是否相同<br>
<code>os.path.sameopenfile(fp1, fp2)</code>  判断fp1和fp2是否指向同一文件<br>
<code>os.path.samestat(stat1, stat2)</code>  判断stat tuple stat1和stat2是否指向同一个文件<br>
<code>os.path.split(path)</code>                   把路径分割成dirname和basename，返回一个元组<br>
<code>os.path.splitdrive(path)</code>            一般用在windows下，返回驱动器名和路径组成的元组<br>
<code>os.path.splitext(path)</code>              分割路径，返回路径名和文件扩展名的元组<br>
<code>os.path.splitunc(path)</code>             把路径分割为加载点与文件<br>
<code>os.path.walk(path, visit, arg)</code>    遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数<br>
<code>os.path.supports_unicode_filenames</code>   设置是否支持unicode路径名</p>
<h2 id="sys模块">sys模块</h2>
<p>sys常用的有：</p>
<p><code>sys.argv</code>                  命令行参数List，第一个元素是程序本身路径<br>
<code>sys.modules.keys()</code>   返回所有已经导入的模块列表<br>
<code>sys.exc_info()</code>          获取当前正在处理的异常类,<code>exc_type</code>、<code>exc_value</code>、<code>exc_traceback</code>当前处理的异常详细信息<br>
<code>sys.exit(n)</code>              退出程序，正常退出时<code>exit(0)</code><br>
<code>sys.hexversion</code>         获取Python解释程序的版本值，16进制格式如：<code>0x020403F0</code><br>
<code>sys.version</code>              获取Python解释程序的版本信息<br>
<code>sys.maxunicode</code>       最大的<code>Unicode</code>值<br>
<code>sys.modules</code>            返回系统导入的模块字段，key是模块名，value是模块<br>
<code>sys.path</code>                 返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值<br>
<code>sys.platform</code>            返回操作系统平台名称<br>
<code>sys.stdout</code>              标准输出<br>
<code>sys.stdin</code>                标准输入<br>
<code>sys.stderr</code>               错误输出<br>
<code>sys.exc_clear()</code>        用来清除当前线程所出现的当前的或最近的错误信息<br>
<code>sys.exec_prefix</code>       返回平台独立的python文件安装的位置<br>
<code>sys.byteorder</code>          本地字节规则的指示器，big-endian平台的值是’big’,little-endian平台的值是’little’<br>
<code>sys.copyright</code>          记录python版权相关的东西<br>
<code>sys.api_version</code>       解释器的C的API版本<br>
<code>sys.version_info</code>      Python解释器的版本信息<br>
<code>sys.displayhook(value)</code>            如果value非空，这个函数会把他输出到<code>sys.stdout</code>，并且将他保存进<code>__builtin__.</code>.指在python的交互式解释器里，’_'代表上次你输入得到的结果，hook是钩子的意思，将上次的结果钩过来<br>
<code>sys.getdefaultencoding()</code>         返回当前你所用的默认的字符编码格式<br>
<code>sys.getfilesystemencoding()</code>     返回将Unicode文件名转换成系统文件名的编码的名字<br>
<code>sys.setdefaultencoding(name)</code>  用来设置当前默认的字符编码，如果name和任何一个可用的编码都不匹配，抛出<code>LookupError</code>，这个函数只会被site模块的<code>sitecustomize</code>使用，一旦别site模块使用了，他会从sys模块移除<br>
<code>sys.builtin_module_names</code>       Python解释器导入的模块列表<br>
<code>sys.executable</code>                       Python解释程序路径<br>
<code>sys.getwindowsversion()</code>          获取Windows的版本<br>
<code>sys.stdin.readline()</code>                从标准输入读一行，<code>sys.stdout.write("a")</code>  屏幕输出a</p>
<h2 id="math-模块">math 模块</h2>
<p>math模块的函数如下：</p>
<p>0，常量</p>
<p><code>math.pi</code>         π = 3.141592…<br>
<code>math.e</code>        e = 2.718281…</p>
<p>1，数值计算函数</p>
<p><code>math.ceil(x)</code>           返回≥x的最小整数<br>
<code>math.floor(x)</code>          返回≤x的最大整数<br>
<code>math.copysign(x,y)</code>    返回与y同号的x值<br>
<code>math.fabs(x)</code>            返回x的绝对值<br>
<code>math.factorial(x)</code>       返回x的阶乘，即x!，x必须为非负整数<br>
<code>math.fmod(x,y)</code>          返回x对y取模的余数(x决定余数符号)，与x%y不同(y决定余数符号)<br>
例：</p>
<pre><code>     math.fmod(100, -3)   --&gt;  1.0
      math.fmod(-100, 3)   --&gt; -1.0
      100 % -3    --&gt;    -2
     -100 %  3    --&gt;     2
</code></pre>
<p><code>math.frexp(x)</code>          返回元组(m,e)，根据 <code>x = m*(2**e)</code><br>
<code>math.fsum(iterable)</code>    返回数组的和，比内置函数sum要精确<br>
<code>math.isfinite(x)</code>        若x是有限数，返回True<br>
<code>math.isinf(x)</code>         若x是无穷大，返回True<br>
<code>math.isnan(x)</code>        若x非数，返回True<br>
<code>math.ldexp(x,i)</code>       返回<code>x*(2**i)</code>的结果<br>
<code>math.modf(x)</code>           返回元组<code>(fractional,integer)</code>，分别为x的小数部分和整数部分<br>
<code>math.trunc(x)</code>         返回x的整数部分</p>
<p>2，乘方/对数函数</p>
<p><code>math.exp(x)</code>            返回e<strong>x<br>
<code>math.expm1(x)</code>         返回e</strong>x - 1<br>
<code>math.log(x[,base])</code>    返回x的对数，base默认的是e<br>
<code>math.log1p(x)</code>           返回x+1的对数，base是e<br>
<code>math.log2(x)</code>            返回x关于2的对数<br>
<code>math.log10(x)</code>           返回x关于10的对数<br>
<code>math.pow(x,y)</code>        返回x**y<br>
<code>math.sqrt(x)</code>          返回x的平方根</p>
<p>3，三角函数</p>
<p><code>math.sin(x)</code>           返回x的正弦，x用弧度制表示<br>
<code>math.cos(x)</code>            返回x的余弦<br>
<code>math.tan(x)</code>             返回x的正切<br>
<code>math.asin(x)</code>            返回x的反正弦，结果用弧度制表示<br>
<code>math.acos(x)</code>            返回x的反余弦<br>
<code>math.atan(x)</code>            返回x的反正切<br>
<code>math.atan2(y,x)</code>         返回<code>atan(y/x)</code><br>
<code>math.hypot(x,y)</code>         返回<code>sqrt(x*x + y*y)</code></p>
<p>4，角度，弧度转换函数</p>
<p><code>math.degrees(x)</code>         弧度 –&gt; 角度<br>
<code>math.radians(x)</code>         角度 -&gt; 弧度</p>
<p>5，双曲线函数</p>
<p><code>math.acosh(x)</code>           返回x的反双曲余弦<br>
<code>math.asinh(x)</code>           返回x的反双曲正弦<br>
<code>math.atanh(x)</code>           返回x的反双曲正切<br>
<code>math.cosh(x)</code>            返回x的双曲余弦<br>
<code>math.sinh(x)</code>            返回x的双曲正弦<br>
<code>math.tanh(x)</code>            返回x的双曲正切</p>
<p>6，特殊函数</p>
<p><code>math.erf(x)</code>           # 不知道这几个是干啥的……原谅我吧……<br>
<code>math.erfc(x)</code>          # 不知道这几个是干啥的……原谅我吧……<br>
<code>math.gamma(x)</code>         # 不知道这几个是干啥的……原谅我吧……<br>
<code>math.lgamma(x)</code>        # 不知道这几个是干啥的……原谅我吧……</p>
<h2 id="collections模块">collections模块</h2>
<p>Python拥有一些内置的数据类型，比如str,int, list, tuple, dict等， collections模块在这些内置数据类型的基础上，提供了几个额外的数据类型：</p>
<ol>
<li>namedtuple   生成可以使用名字来访问元素内容的tuple子类</li>
<li>deque   双端队列，可以快速的从另外一侧追加和推出对象</li>
<li>Counter   计数器，主要用来计数</li>
<li>OrderedDict   有序字典</li>
<li>defaultdict   带有默认值的字典</li>
</ol>
<h2 id="heapq模块">heapq模块</h2>
<p><a href="https://docs.python.org/2/library/heapq.html">https://docs.python.org/2/library/heapq.html</a></p>
<p>这个模块(build-in)实现了一个堆的数据结构，完美的解决了Top-K问题，以后解决Top-K问题的时候，直接把这个模块拿来用就可以了<br>
注意，默认的heap是一个小顶堆！</p>
<p>heapq模块提供了如下几个函数：</p>
<p><code>heapq.heappush(heap, item)</code>把item添加到heap中（heap是一个列表）<br>
<code>heapq.heappop(heap)</code> 把堆顶元素弹出，返回的就是堆顶<br>
<code>heapq.heappushpop(heap, item)</code> 先把item加入到堆中，然后再pop，比heappush()再heappop()要快得多<br>
<code>heapq.heapreplace(heap, item)</code>先pop，然后再把item加入到堆中，比heappop()再heappush()要快得多<br>
<code>heapq.heapify(x)</code>将列表x进行堆调整，默认的是小顶堆<br>
<code>heapq.merge(*iterables)</code>将多个列表合并，并进行堆调整，返回的是合并后的列表的迭代器<br>
<code>heapq.nlargest(n, iterable, key=None)</code> 返回最大的n个元素（Top-K问题）<br>
<code>heapq.nsmallest(n, iterable, key=None)</code>返回最小的n个元素（Top-K问题</p>