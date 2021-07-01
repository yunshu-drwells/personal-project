## Makefile

### 简介

在软件开发中，make是一个工具程序（Utility software），经由读取叫做“makefile”的文件，自动化建构软件。它是一种转化文件形式的工具，转换的目标称为“target”；与此同时，它也检查文件的依赖关系，如果需要的话，它会调用一些外部软件来完成任务。它的依赖关系检查系统非常简单，主要根据依赖文件的修改时间进行判断。大多数情况下，它被用来编译源代码，生成结果代码，然后把结果代码连接起来生成可执行文件或者库文件。它使用叫做“makefile”的文件来确定一个target文件的依赖关系，然后把生成这个target的相关命令传给shell去执行。

许多现代软件的开发中（如Microsoft Visual Studio），集成开发环境已经取代make，但是在Unix环境中，仍然有许多任务程师采用make来协助软件开发。


### 文件命名和规则

1. 命名：makefile/Makefile
2. Makefile规则：一个或者多个规则

```makefile
    目标... : 依赖...
        命令(shell命令)
        ...
```

- 目标：最终要生成的文件(伪目标除外)
- 依赖：生成目标所需要的文件或者目标
- 命令：通过执行命令对依赖操作生成目标(命令前必须Tab缩进)
- Makefile中的其它规则一般都是为第一条规则服务



### Makefile基本原理


#### 1. 命令在执行前，需要先检查规则中的依赖是否存在

a. 如果存在，执行命令

b. 如果不存在，向下检查其它规则，检查有没有一个规则是用来生成这个依赖的，如果找到了，则执行该规则中的命令

#### 2. 检查更新，在执行规则中的命令时，会比较目标和依赖文件的时间


a. 如果依赖的时间比目标时间晚，需要更新生成目标

b. 如果依赖的时间比目标时间早，目标不需要更新，对应规则中的命令不需要被执行




##### 看例子


给<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/practic_Makefile/add.c">add.c</a> <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/practic_Makefile/div.c">div.c</a> <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/practic_Makefile/sub.c">sub.c</a> <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/practic_Makefile/mult.c">mult.c </a><a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/practic_Makefile/main.c">main.c</a>

###### 使用命令编译：

	gcc add.c div.c sub.c mult.c main.c o app


###### <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/blob/master/practic_Makefile/Makefile1">Makefile1</a>:

```
	app: sub.c add.c mult.c div.c main.c
		gcc sub.c add.c mult.c div.c main.c -o app
```

拷贝到Makefile:

	cp Makefile1 Makefile

make一下，执行命令：

	gcc sub.c add.c mult.c div.c main.c -o app

> 符合规则1.a


###### <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/blob/master/practic_Makefile/Makefile2">Makefile2</a>:


```
app: sub.o add.o mult.o div.o main.o
	gcc sub.c add.c mult.c div.c main.c -o app

sub.o:sub.c
	gcc -c sub.c -o sub.o

add.o:add.c
	gcc -c add.c -o add.o

mult.o:mult.c
	gcc -c mult.c -o mult.o

div.o:div.c
	gcc -c div.c -o div.o

main.o:main.c
	gcc -c main.c -o main.o
```



拷贝到Makefile:

	cp Makefile2 Makefile

make一下，执行命令：

    gcc -c sub.c -o sub.o
    gcc -c add.c -o add.o
    gcc -c mult.c -o mult.o
    gcc -c div.c -o div.o
    gcc -c main.c -o main.o
    gcc sub.o add.o mult.o div.o main.o -o app

> 符合基本原理1.b



更改一下add.c文件

add修改时间会比上一次生成app目标文件时间晚，make一下，执行命令：

```
gcc -c add.c -o add.o
gcc sub.o add.o mult.o div.o main.o -o app
```
Makefile工具会检测更新情况，如果依赖文件比目标文件修改时间晚则会重新生成，如果依赖文件没有更新则会提升已经时最新的，不再重新生成

继续make一下，提示：

    make: 'app' is up to date.

> 符合基本原理2.a，2.b

make时遇到Makefile:2: *** missing separator.  Stop.问题请参考文章：<a href="https://blog.csdn.net/qq_43808700/article/details/118241610">Makefile:2: *** missing separator. Stop.</a>







### 变量

#### 1.自定义变量

变量名=变量值

```
var=hello
# 获取变量值：$(variable name)
$(var)
```

##### 还是以上面的app例子为例

###### <a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/blob/master/practic_Makefile/Makefile3">编写Makefile3</a>：

```
# 定义变量
src=sub.o add.o mult.o div.o main.o
target=app
$(target):$(src)
	$(CC) $(src) -o $(target)

sub.o:sub.c
	gcc -c sub.c -o sub.o

add.o:add.c
	gcc -c add.c -o add.o

mult.o:mult.c
	gcc -c mult.c -o mult.o

div.o:div.c
	gcc -c div.c -o div.o

main.o:main.c
	gcc -c main.c -o main.o
```


拷贝到Makefile:

	cp Makefile3 Makefile

make一下，执行命令：

    gcc -c sub.c -o sub.o
    gcc -c add.c -o add.o
    gcc -c mult.c -o mult.o
    gcc -c div.c -o div.o
    gcc -c main.c -o main.o
    cc sub.o add.o mult.o div.o main.o -o app



#### 2.预定义变量

AR：归档维护程序的名称，默认值为ar
CC：C编译器的名称，默认值为cc
CXX：C++编译器的名称，默认值为g++
\$@：目标的完整名称
\$<：依赖文件的名称
\$^：所有的依赖文件

    app:main.c a.c b.c
        gcc -c main.c a.c b.c

    # 自动变量只能在规则的命令中使用
    app:main.c a.c b.c
        $(CC) -C $^ -o $@



### 模式匹配


#### %.o:%.c

- %：通配符，匹配一个字符串
- 一行命令中两个%匹配的是同一个字符串

```
%.o:%.c
    gcc -c $^ -o $@
```

##### 还是以上面的app例子为例

###### 简化Makefile3-><a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/blob/master/practic_Makefile/Makefile4">Makefile4</a>

```
src=sub.o add.o mult.o div.o main.o
target=app
$(target):$(src)
	$(CC) $(src) -o $(target)

%.o:%.c
   $(CC) -c $< -o $@
```


拷贝到Makefile:

	cp Makefile4 Makefile

make一下，执行命令：

    cc -c sub.c -o sub.o
    cc -c add.c -o add.o
    cc -c mult.c -o mult.o
    cc -c div.c -o div.o
    cc -c main.c -o main.o
    cc sub.o add.o mult.o div.o main.o -o app


### 函数


#### $(wildcard PATTERN...)

- 功能：获取指定目录下的指定类型的文件列表
- 参数：PATTERN指的是某个或多个目录下的对应的某种类型的文件，如果有多个目录，一般使用空格间隔
- 返回：得到匹配到的若干个文件的文件列表，文件名之间使用空格分割
- 示例：$(wildcard ./sub/.c) 返回值格式：a.c b.c c.c d.c

#### $(patsubst <pattern>, <replacement>, <text>)

- 功能：查找<text>中的单词(单词以"空格"、"Tab"、"回车"或者换行分隔)是否符合模式<pattern>，如果匹配的话，则以<replacement>替换
- <pattern>可以包括通配符%，表示任意长度的字符串，如果<replacement>中也包含%，那么，<replacement>中的这个%将是<pattern>中的那个%所代表的字符串。(可以用\来转义，用来表示字符%)
- 返回：函数返回被替换过后的字符串
- 示例：$(patsubst %.c, %.o, x.c y.c) 返回值格式：x.o y.o


##### 还是以上面的app例子为例

###### 使用函数<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/blob/master/practic_Makefile/Makefile5">Makefile5</a>




```
src=$(wildcard ./*.c) # 通过wildcard函数在./路径下找和*.c匹配的内容
objs=$(patsubst %.c, %.o, $(src)) # 通过patsubst将src中的字符串匹配到的%.o替换成%.o
# 依赖文件过多书写起来不美观而且容易遗漏，这种方式在增加某个依赖文件时可以自动搜索到简洁又快捷
target=app
$(target):$(objs)
	$(CC) $(objs) -o $(target)

%.o:%.c
	$(CC) -c $< -o $@

.PHONY:clean 
clean:
	rm $(objs) -f # 删除所有生成的.o依赖文件;-f 强制删除

# 后面的规则都是为第一条规则服务的，可以在bash中make clean随时执行clean命令，
# 但是如果Makefile路径下有一个时间比较新的clean文件,clean命令后面没有依赖文件，因此时间是比较老的
# 这时在bash中make clean就会提示clean已经是最新的了，clean命令就不能执行了
# 因此需要.PYONY声明一下clean是伪目标，意思不会生成目标文件
```

拷贝到Makefile:

    cp Makefile5 Makefile

make一下，执行命令：

```
cc -c mult.c -o mult.o
cc -c main.c -o main.o
cc -c add.c -o add.o
cc -c div.c -o div.o
cc -c sub.c -o sub.o
cc  ./mult.o  ./main.o  ./add.o  ./div.o  ./sub.o  -o app
```

没有执行rm $(objs) -f命令，因为后面的规则都是为第一条规则服务的

可以在bash中调用指定命令：make clean

    rm  ./add.o  ./mult.o  ./main.o  ./div.o  ./sub.o  -f # 删除所有生成的.o依赖文件;-f 强制删除

> 不是第一条规则依赖的规则，就可以在bash中执行了，持续make clean命令都是可以正常执行的

如果在Makefile同一路径下执行touch clean，会创建一个clean的文件，此时make clean就会发现提示：

    make: 'clean' is up to date.

> clean命令是没有依赖文件的，因此时间是比较老的时间，touch clean的时机又是比较新的，touch clean之后，clean文件的时机太新了，因此clean就不再执行了

此时就需要.PHONY声明clean是伪目标，意思不会生成文件

此时再在bash中make clean，就可以正常调用clean命令了：

    rm  ./add.o  ./mult.o  ./main.o  ./div.o  ./sub.o  -f # 删除所有生成的.o依赖文件;-f 强制删除



### make参数选项



|make参数选项	|功能|
|:--|:--|
|-b，-m	|忽略，提供其他版本 make 的兼容性
|-B，--always-make	|强制重建所有的规则目标，不根据规则的依赖描述决定是否重建目标文件。
|-C DIR，--directory=DIR	|在读取 Makefile 之前，进入到目录 DIR，然后执行 make。当存在多个 "-C" 选项的时候，make 的最终工作目录是第一个目录的相对路径。
|-d	|make 在执行的过程中打印出所有的调试信息，包括 make 认为那些文件需要重建，那些文件需要比较最后的修改时间、比较的结果，重建目标是用的命令，遗憾规则等等。使用 "-d" 选项我们可以看到 make 构造依赖关系链、重建目标过程中的所有的信息。
|--debug[=OPTIONS]	|make 执行时输出调试信息，可以使用 "OPTIONS" 控制调试信息的级别。默认是 "OPTIONS=b" ，"OPTIONS" 的可值为以下这些，首字母有效：all、basic、verbose、implicit、jobs、makefile。
|-e，--enveronment -overrides	|使用环境变量定义覆盖 Makefile 中的同名变量定义。
|-f=FILE，--file=FILE，--makefile=FILE	|指定文件 "FILE" 为 make 执行的 Makefile 文件
|-p，--help	|打印帮助信息。
|-i，--ignore-errors	|执行过程中忽略规则命令执行的错误。
|-I DIR，--include-dir=DIR	|指定包含 Makefile 文件的搜索目录，在Makefile中出现另一个 "include" 文件时，将在 "DIR" 目录下搜索。多个 "-i" 指定目录时，搜索目录按照指定的顺序进行。
|-j [JOBS]，--jobs[=JOBS]	|可指定同时执行的命令数目，爱没有 "-j" 的情况下，执行的命令数目将是系统允许的最大可能数目，存在多个 "-j" 目标时，最后一个目标指定的 JOBS 数有效。
|-k，--keep-going	|执行命令错误时不终止 make 的执行，make 尽最大可能执行所有的命令，直至出现知名的错误才终止。
|-l load，--load-average=[=LOAD]，--max-load[=LOAD]	|告诉 make 在存在其他任务执行的时候，如果系统负荷超过 "LOAD"，不在启动新的任务。如果没有指定 "LOAD" 的参数  "-l" 选项将取消之前 "-l" 指定的限制。
|-n，--just-print，--dry-run	|只打印执行的命令，但是不执行命令。
|-o FILE，--old-file=FILE，--assume-old=FILE	|指定 "FILE"文件不需要重建，即使是它的依赖已经过期；同时不重建此依赖文件的任何目标。注意：此参数不会通过变量 "MAKEFLAGS" 传递给子目录进程。
|-p，--print-date-base	|命令执行之前，打印出 make 读取的 Makefile 的所有数据，同时打印出 make 的版本信息。如果只需要打印这些数据信息，可以使用 "make -qp" 命令，查看 make 执行之前预设的规则和变量，可使用命令 "make -p -f /dev/null"
|-q，-question	|称为 "询问模式" ；不运行任何的命令，并且无输出。make 只返回一个查询状态。返回状态 0 表示没有目标表示重建，返回状态 1 表示存在需要重建的目标，返回状态 2 表示有错误发生。
|-r，--no-builtin-rules	|取消所有的内嵌函数的规则，不过你可以在 Makefile 中使用模式规则来定义规则。同时选项 "-r" 会取消所有后缀规则的隐含后缀列表，同样我们可以在 Makefile 中使用 ".SUFFIXES"，定义我们的后缀名的规则。"-r" 选项不会取消 make 内嵌的隐含变量。
|-R，--no-builtin-variabes	|取消 make 内嵌的隐含变量，不过我们可以在 Makefile 中明确定义某些变量。注意："-R" 和 "-r" 选项同时打开，因为没有了隐含变量，所以隐含规则将失去意义。
|-s，--silent，--quiet	|取消命令执行过程中的打印。
|-S，--no-keep-going，--stop	|取消 "-k" 的选项在递归的 make 过程中子 make 通过 "MAKEFLAGS" 变量继承了上层的命令行选项那个。我们可以在子 make 中使用“-S”选项取消上层传递的 "-k" 选项，或者取消系统环境变量 "MAKEFLAGS" 中 "-k"选项。
|-t，--touch	|和 Linux 的 touch 命令实现功能相同，更新所有的目标文件的时间戳到当前系统时间。防止 make 对所有过时目标文件的重建。
|-v，version	|查看make的版本信息。
|-w，--print-directory	|在 make 进入一个子目录读取 Makefile 之前打印工作目录，这个选项可以帮助我们调试 Makefile，跟踪定位错误。使用 "-C" 选项时默认打开这个选项。
|--no-print-directory	|取消 "-w" 选项。可以是 用在递归的 make 调用的过程中 ，取消 "-C" 参数的默认打开 "-w" 的功能。
|-W FILE，--what-if=FILE，--new-file=FILE，--assume-file=FILE	|设定文件 "FILE" 的时间戳为当前的时间，但不更改文件实际的最后修改时间。此选项主要是为了实现对所有依赖于文件 "FILE" 的目标的强制重建。
|--warn-undefined-variables	|在发现 Makefile 中存在没有定义的变量进行引用时给出告警信息。此功能可以帮助我们在调试一个存在多级嵌套变量引用的复杂 Makefile。但是建议在书写的时候尽量避免超过三级以上的变量嵌套引用。

