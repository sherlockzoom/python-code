
## 迭代器

迭代的意思是重复做一些事很多次，就像在循环中做的那样。python的基础教程里面常见的是对字典和序列进行迭代，但实际上也能对其他对象进行迭代：只要该对象实现了`__iter__`方法。（典型的[鸭子类型](https://zh.wikipedia.org/wiki/%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B)）

`__iter__`方法会返回一个迭代器，也就是具有`__next__`方法的对象。调用next方法就会访问下一个值。

> 迭代器规则的关键是什么？ 为什么不使用列表？

因为列表杀伤力太大了。如果一个函数能够一个接一个的计算值，那么使用时可能是计算一次获取一个值---而不是通过列表获取所有值。好处当然在于不会占用太多内存。其他一些理由：使用迭代器更通用、更简单、更优雅。

看一个经典的”菲波拉契数列“，使用迭代器：

```py
class Fibs:
	def __init__(self):
		self.a = 0
		self.b = 1
	def __next__(self):
		self.a, self.b = self.b, self.a+self.b
	def __iter__(self):
		return self
```

调用过程

	>>>fibs = Fibs()
	>>>for f in fibs:
			if f>1000:
				print f
				break

内建函数`iter`可以从可迭代的对象中获得迭代器

```py
it = iter([1, 2, 3])
it.next() #output: 1
it.next() #output:2
```

除了在迭代器和可迭代对象上进行迭代，还能把它们转换为序列。比如使用list构造方法显式的转化为列表。

## 生成器
生成器是一种用普通的函数语法定义的迭代器。生成器可以帮助我们写出非常优雅的代码。它的工作方式可以例子来很好的展现。让我们看看它是怎样创建和使用的。

```py
nested = [[1, 2], [3, 4], [5, 6]] #没错这是一个列表的列表
# 我们希望能按照顺序打印出列表中的数字

def flatten(nested):
	for sublist in nested:
		for element in sublist:
			yield element   # 注意这里不是print element
```
> 任何包含`yield`语句的函数称为生成器 。除了名字不同以外，它的行为和普通的函数也很有差别，它不像`return`那样返回值，而每次产生多个值。每次产生一个值，函数就会被 **冻结** ：即函数停在那点等待被重新唤醒。唤醒后从停止点开始执行。

	>>>nested = [[1, 2], [3, 4], [5, 6]]
	>>>for num in flatten(nested):
			print num
	1
	2
	3
	...
	6
	or
	>>>list(flatten(nested))
	[1, 2, 3, 4, 5, 6]

### 循环生成器(生成器推导式)
和列表推导式不同在于圆括号的使用方式。更秒的地方在于生成器推导式可以在当前圆括号内直接使用：
`sum(i**2 for i in range(10))`

	>>>g=((i+2)**2 for i in range(2,27))
	>>>g.next()
	16

### 递归生成器
前面创建生成器使用了2层嵌套，那么任意层嵌套呢？

```py
def flatten(nested):
	try:
		for sublist in nested:
			for element in flatten(sublist): # 递归调用flatten
				yield element
	except TypeError:
		yield nested
```

更多的生成器可参考《python基础教程》

---

	The Zen of Python, by Tim Peters

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








> Written with [StackEdit](https://stackedit.io/).