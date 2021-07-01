

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



### 多进程调试

...

