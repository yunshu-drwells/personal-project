<!--
 * @Descripttion: 
 * @Author: 杨致远
 * @version: 
 * @Date: 2021-06-27 15:49:34
 * @LastEditTime: 2021-07-14 08:00:39
 * Copyright (C) 2021 yangzhiyuan. All rights reserved.
-->


## GDB

### gdb参数


|功能|命令|
|:--|:--|
|启动和退出|gdb可执行程序</br>quit/q|
|给程序设宵参数/获取设置参数|set args 10 20</br>show args|
|GDB使用帮助|help|
|查看当前文件代码|list/l （从默认位置显示）</br>list/l 行号（显示指定的行(居中)）</br>list/l 函数名（从指定的函数显示）|
|查看非当前文件代码|list/l文件名:行号</br>list/l文件名:函数名|
|设置显示的行数|show list/listsize</br>set list/listsize 行数|
|设置断点|b/break 行号</br>b/break函数名</br>b/break文件名:行号</br>b/break文件名:函数|
|查看断点|i/info b/break|
|删除断点|d/del/delete断点编号|
|设置断点无效|dis/disable断点编号|
|设置断点生效|ena/enable断点编号|
|设置条件断点（一般用在循环的位置）|b/break 10 if i==5|
|运行GDB程序|start （程序停在第一行） </br> run （遇到断点才停）|
|继续运行，到下一个断点停|c/continue|
|向下执行一行代码（不会进入函数体）|n/next|
|变量操作|p/print 变量名（打印变量值） </br>ptype 变量名（打印变量类型）|
|向下单步调试（遇到函数进入函数体）|s/step</br>finish （跳出函数体）|
|自动变量操作|display变量名（自动打印指定变量的值）</br>i/info display</br>undisplay 编号|
|其它操作|set var变量名=变量值（循环中用的较多）</br>until （跳出循环）|



### 给定测试文件：bubble.cpp main.cpp select.cpp sort.h main.cpp test.c演示调试

#### GDB C

gcc加上-g选项，编译的时候会加入调试信息

    gcc test.c -o test -g

启动gdb:

    gdb test

运行时可以加上命令行参数：

    ./test 10 20

同样使用gdb set args可以设置调试的命令行参数,whow args可以展示命令行参数：

    (gdb) set args 10 20
    (gdb) show args
    Argument list to give program being debugged when it is started is "10 20".

退出gdb:

    quit/q

#### GDB C++

    g++ bubble.cpp select.cpp main.cpp -o app1 -g

查看指定cpp的指定行：

    l bubble.cpp:6

查看指定cpp的指定函数：

    l select.cpp:selectSort


给main源文件打断点

    b 8
    b 15

查看断点信息

    i b

给指定文件的指定行数打断点

    b select.cpp:8

查看main.cpp

    l main.cpp:main

运行到第一个断点处

    run

> 运行到main:8

继续运行到下一个断点

    c

> 运行到main:15

下一步(遇到函数进入函数)

    s

> 进入selectSort函数



### 多进程多线程调试


##### 多线程

1、info threads： 

　　这条命令显示的是当前可调试的所有线程,GDB会给每一个线程都分配一个ID。前面有*的线程是当前正在调试的线程。 

2、thread ID： 

　　切换到当前调试的线程为指定为ID的线程。 

3、thread apply all command： 

　　让所有被调试的线程都执行command命令 

4、thread apply ID1 ID2 … command： 

　　这条命令是让线程编号是ID1，ID2…等等的线程都执行command命令 

5、set scheduler-locking off|on|step： 

　　在使用step或continue命令调试当前被调试线程的时候，其他线程也是同时执行的，如果我们只想要被调试的线程执行，而其他线程停止等待，那就要锁定要调试的线程，只让它运行。 
- off:不锁定任何线程，所有线程都执行。 
- on:只有当前被调试的线程会执行。 
- step:阻止其他线程在当前线程单步调试的时候抢占当前线程。只有当next、continue、util以及finish的时候，其他线程才会获得重新运行的。 


6、show scheduler-locking： 

　　这条命令是为了查看当前锁定线程的模式。 

7.i threads

　　实现线程间切换

9.-g -rdynamic

　　在生成调试信息的时候加入 -g -rdynamic选项，然后gdb启动调试程序时，直接run，就能找出错误信息所在的地方

    一个小提示：
    在输入gdb xx时，进入gdb命令，这时会输出一些信息。如上所示，这些信息大多都是关于gdb的一些信息，可以不让他输出，
    如：gdb -q xx
    这里面xx是我生成的调试信息的文件名。


##### 多进程

默认设置下, 在调试多进程程序时 GDB 只会调试主进程. 但是 GDB > V7.0 支持多进程的分别以及同时调试, 换句话说, GDB 可以同时调试多个程序. 只需要设置 follow-fork-mode (默认值 parent) 和 detach-on-fork (默认值 on )即可.

| follow-fork-mode | detach-on-fork | 说明                                      |
|------------------|----------------|-----------------------------------------|
| parent           | on             | 只调试主进程(GDB默认)                           |
| child            | on             | 只调试子进程                                  |
| parent           | off            | 同时调试两个进程,gdb 跟主进程, 子进程 block 在 fork 位置  |
| child            | off            | 同时调试两个进程, gdb 跟子进程, 主进程 block 在 fork 位置 |

###### 命令练习

- 进入gdb调试模式

    gcc process.c -o process -g
    gdb process

- 查看系统默认的follow-fork-mode 和 detach-on-fork：

    show follow-fork-mode
    show detach-on-fork

- 设置follow-fork-mode 和 detach-on-fork：

    set follow-fork-mode [parent|child]   
    set detach-on-fork [on|off]

    set follow-fork-mode child
    set detach-on-fork off
    //主进程阻塞

- 用l/list命令查看源代码（按enter翻页），分别在子进程和父进程相应位置下断点：

    b 22
    b 25

