1用字符串本身的replace方法:

a = 'hello word'
b = a.replace('word','python')
print b

2用正则表达式来完成替换:
import re
a = 'hello word'
strinfo = re.compile('word')
b = strinfo.sub('python',a)
print b


python的字串列表有2种取值顺序
1是从左到右索引默认0开始的，最大范围是字符串长度少1
s = 'ilovepython'
s[0]的结果是i

2是从右到左索引默认-1开始的，最大范围是字符串开头
s = 'ilovepython'
s[-1]的结果是n

上面这个是取得一个字符，如果你的实际要取得一段子串的话，可以用到变量[头下标:尾下标]，就可以截取相应的字符串，其中下标是从0开始算起，可以是正数或负数，下标可以为空表示取到头或尾。

比如
s = 'ilovepython'
s[1:5]的结果是love
当使用以冒号分隔的字符串，python返回一个新的对象，结果包含了以这对偏移标识的连续的内容，左边的开始是包含了下边界，比如
上面的结果包含了s[1]的值l，而取到的最大范围不包括上边界，就是s[5]的值p


info = 'name:haha,age:20$name:python,age:30$name:fef,age:55'
content = info.split('$')
print content


字符串大小写

通过下面的upper(),lower()等方法来转换大小写

S.upper()#S中的字母大写
S.lower() #S中的字母小写
S.capitalize() #首字母大写
S.istitle() #S是否是首字母大写的
S.isupper() #S中的字母是否便是大写
S.islower() #S中的字母是否全是小写
字符串去空格

通过strip(),lstrip(),rstrip()方法去除字符串的空格

S.strip()去掉字符串的左右空格
S.lstrip()去掉字符串的左边空格
S.rstrip()去掉字符串的右边空格
字符串其他方法

字符串相关的其他方法:count(),join()方法等。

S.center(width, [fillchar]) #中间对齐
S.count(substr, [start, [end]]) #计算substr在S中出现的次数
S.expandtabs([tabsize]) #把S中的tab字符替换没空格，每个tab替换为tabsize个空格，默认是8个
S.isalnum() #是否全是字母和数字，并至少有一个字符
S.isalpha() #是否全是字母，并至少有一个字符
S.isspace() #是否全是空白字符，并至少有一个字符
S.join()#S中的join，把列表生成一个字符串对象
S.ljust(width,[fillchar]) #输出width个字符，S左对齐，不足部分用fillchar填充，默认的为空格。
S.rjust(width,[fillchar]) #右对齐
S.splitlines([keepends]) #把S按照行分割符分为一个list，keepends是一个bool值，如果为真每行后而会保留行分割符。
S.swapcase() #大小写互换 