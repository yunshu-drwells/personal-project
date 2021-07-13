## GCC

- GCC原名为GNU C语言编译器（GNU C Compiler）
- GCC （GNU Compiler Collection, GNU编译器套件）是由GNU开发的编程语言译器。GNU编译器套件包括 C、C++、Objective-C、Java、Ada和Go语言前端，也包括了这些语言的库（如libstdc++, libgcj等）
- GCC不仅支持C的许多"方言"，也可以区别不同的C语言标准；可以使用命令行选项来控制编译器在翻译源代码时应该遂循哪个C标准.例如，当使用命令行参数-std=c99启动GCC时，编译器支持C99标准。
- 安装命令 sudo apt install build-essential(gcc/g++/make)
- 查看版本 gcc/g++ -v/-version

### GCC编译流程

<img src="https://img-blog.csdnimg.cn/20210625113417164.png" height=350/>

##### 源码

```c
#include <stdio.h>

#define PI 3.14

int main(){
    //注释

    int num = 10+PI;

    printf("hello, %d", num);cd 
    return 0;
}
```

<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/compile_process/test.c">test.c</a>

##### 预处理生成.i文件

gcc -E test.c -o test.i

<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/compile_process/test.i">test.i</a>


##### 预编译：这个过程主要的处理操作如下：

（1） 将所有的#define删除并替换，展开所有的宏定义

（2） 处理所有的条件预编译指令，如#if、#ifdef

（3） 处理#include预编译指令，将被包含的文件插入到该预编译指令的位置。

（4） 过滤所有的注释

（5） 添加行号和文件名标识。



##### 编译生成.S文件

gcc -S test.i -o test.S

<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/compile_process/test.S">test.S</a>


##### 汇编生成.o文件

gcc -c test.S -o test.o

<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/compile_process/test.o">test.o</a>


##### 链接

gcc test.o -o test.out

<a href="https://github.com/yangzhiyuanDrwells/C-double-plus-learning/tree/master/compile_process/test.out">test.out</a>


### gcc编译选项

|gcc编译选项	|说明|
|:--|:--|
|-E|预处理指定的源文件，不进行编译|
|-S|编译指定的源文件，但是不进行汇编|
|-c|编译、汇编指定的源文件，但是不进行链接|
|-o|-o file1 file2/file1 -o file2 ：将file1编程成file2|
|-I directory|指定include 包含文件的搜索目录|
|-g|在编译的时候，生成调试信息，该程序可以被调试器调试|
|-D|在程序编译的时候，指定一个宏|
|-w|不生产任何警告信息|
|-Wall|生成所有警告信息|
|-On | n的取值范围是：0~3。编译器的优化选项的4个级别，-O0表示没有优化，-O1为缺省值，-O3优化级别最高|
|-l|在程序编译的时候，指定使用的库 eg:-l pthread|
|-L|指定编译的时候，搜索的库的路径|
|-fPIC/fpic|生成与位置无关的代码|
|-shared|生成共享目录文件，通常用在简历共享库时|
|-std|指定C方言，如：-std=c99, gcc默认的方言是GNU C|




### GCC -D选项

编译的时候加入宏常量

test1.c

```c
#include <stdio.h>
int main(){
#ifdef DEBUG
printf("我是一个不会爬树的程序猿！\n");
#endif
printf("hello!");
    return 0;
}
```


gcc test1.c -o test1.out
./test1.out

    输出：
    
    我是一个不会爬树的程序猿！
    hello!

gcc test1.c -o test1.out -D DEBUG
./test1.out

    输出：
    
    hello!

