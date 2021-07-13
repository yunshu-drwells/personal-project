# WebServer
用C++实现的高性能WEB服务器，经过webbenchh压力测试可以实现上万的QPS

## 功能
* 利用IO复用技术Epoll与线程池实现多线程的Reactor高并发模型；
* 利用正则与状态机解析HTTP请求报文，实现处理静态资源的请求；
* 利用标准库容器封装char，实现自动增长的缓冲区；
* 基于小根堆实现的定时器，关闭超时的非活动连接；
* 利用单例模式与阻塞队列实现异步的日志系统，记录服务器运行状态；
* 利用RAII机制实现了数据库连接池，减少数据库连接建立与关闭的开销，同时实现了用户注册登录功能。

## 环境要求
* Linux
* C++14
* MySql

## 目录树
```
.
├── bin
│   ├── log
│   │   ├── 2021_07_10.log
│   │   ├── 2021_07_11.log
│   │   └── 2021_07_12.log
│   └── server
├── build
│   └── Makefile
├── code
│   ├── buffer
│   │   ├── buffer.cpp
│   │   └── buffer.h
│   ├── http
│   │   ├── httpconn.cpp
│   │   ├── httpconn.h
│   │   ├── httprequest.cpp
│   │   ├── httprequest.h
│   │   ├── httpresponse.cpp
│   │   └── httpresponse.h
│   ├── log
│   │   ├── blockqueue.h
│   │   ├── log.cpp
│   │   └── log.h
│   ├── main.cpp
│   ├── pool
│   │   ├── sqlconnpool.cpp
│   │   ├── sqlconnpool.h
│   │   ├── sqlconnRAII.h
│   │   └── threadpool.h
│   ├── server
│   │   ├── epoller.cpp
│   │   ├── epoller.h
│   │   ├── webserver.cpp
│   │   └── webserver.h
│   └── timer
│       ├── heaptimer.cpp
│       └── heaptimer.h
├── log
│   ├── 2021_03_17-1.log
│   ├── 2021_03_17-2.log
│   ├── 2021_03_17.log
│   ├── 2021_03_18.log
│   ├── 2021_03_21-1.log
│   ├── 2021_03_21.log
│   ├── 2021_07_12.log
│   └── 2021_07_13.log
├── Makefile
├── readme.md
├── resources
│   ├── 400.html
│   ├── 403.html
│   ├── 404.html
│   ├── 405.html
│   ├── css
│   │   ├── animate.css
│   │   ├── bootstrap.min.css
│   │   ├── font-awesome.min.css
│   │   ├── magnific-popup.css
│   │   └── style.css
│   ├── error.html
│   ├── fonts
│   │   ├── FontAwesome.otf
│   │   ├── fontawesome-webfont.eot
│   │   ├── fontawesome-webfont.svg
│   │   ├── fontawesome-webfont.ttf
│   │   ├── fontawesome-webfont.woff
│   │   └── fontawesome-webfont.woff2
│   ├── images
│   │   ├── favicon.ico
│   │   ├── instagram-image1.jpg
│   │   ├── instagram-image2.jpg
│   │   ├── instagram-image3.jpg
│   │   ├── instagram-image4.jpg
│   │   ├── instagram-image5.jpg
│   │   └── profile-image.jpg
│   ├── index.html
│   ├── js
│   │   ├── bootstrap.min.js
│   │   ├── custom.js
│   │   ├── jquery.js
│   │   ├── jquery.magnific-popup.min.js
│   │   ├── magnific-popup-options.js
│   │   ├── smoothscroll.js
│   │   └── wow.min.js
│   ├── login.html
│   ├── picture.html
│   ├── register.html
│   ├── video
│   │   └── xxx.mp4
│   ├── video.html
│   └── welcome.html
└── webbench-1.5
    ├── Makefile
    ├── socket.c
    ├── webbench
    ├── webbench.c
    └── webbench.o
```

---

## 开发环境搭建

#### 安装Linux(虚拟机、云主机)

https://releases.ubuntu.com/bionici

#### 安装Xshell、XFTP

https://www.netsarang.com/zh/free-for-home-school/


#### 安装Visual Studio Code

https://code.visualstudio.com/

#### 安装MySQL数据库

https://segmentfault.com/a/1190000023081074

##### 安装MySQL

sudo apt-get install mysql-server 
sudo apt-get install mysql-client 
sudo apt-get install libmysqlclient-dev

##### 更改默认密码

- 查看默认配置文件

sudo cat /etc/mysql/debian.cnf

有‘user=debian-sys-maint’，即为自动配置的默认用户；‘password=LzOhAjxVRn2GAKjG’，即为自动配置的密码

- 以默认配置登陆mysql

mysql -u debian-sys-maint -p // 用户名以自己的配置文件为准

提示输入密码，这里要输入的就是上一步的‘password=LzOhAjxVRn2GAKjG’（密码以自己的配置文件为准）

- 更改密码

use mysql; 
// 下一行，密码改为了yourpassword，可以设置成其他的 
update mysql.user set authentication_string=password('yourpassword') where user='root' and Host ='localhost'; 
update user set plugin="mysql_native_password"; 
flush privileges; 
quit;

- 重启MySQL服务

sudo service mysql restart mysql -u root -p 新密码


##### 配置远程访问

- 编辑配置文件，注释掉bind-address = 127.0.0.1：

sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf

- 进入mysql服务，执行授权命令

grant all on *.* to root@'%' identified by '你的密码' with grant option; flush privileges;


- 重启服务

sudo service mysql restart



#### 阿里镜像

https://developer.aliyun.com/mirrorl


#### 安装sshd服务

sudo apt install openssh-server

#### 安装gcc/g++/make工具

sudo apt install build-essential

> 查看版本 gcc/g++ -v/--version


#### 安装gdb

    sudo apt install gdb

#### 安装tree

    sudo apt install tree

---

## 项目启动


##### 修改或者查看密码

sudo cat /etc/mysql/debian.cnf

    [client]
    host     = localhost
    user     = debian-sys-maint
    password = LzOhAjxVRn2GAKjG
    socket   = /var/run/mysqld/mysqld.sock
    [mysql_upgrade]
    host     = localhost
    user     = debian-sys-maint
    password = LzOhAjxVRn2GAKjG
    socket   = /var/run/mysqld/mysqld.sock


##### 登录数据库

    mysql -u root -p
    root




##### 需要先配置好对应的数据库


```bash
// 建立yourdb库
create database yourdb;

// 创建user表
USE yourdb;
CREATE TABLE user(
    username char(50) NULL,
    password char(50) NULL
)ENGINE=InnoDB;

// 添加数据
INSERT INTO user(username, password) VALUES('name', 'password');
```

> database:webserver
> table:user

##### 启动

```bash
make
./bin/server
```

## 单元测试
```bash
cd test
make
./test
```

## 压力测试

```bash
./webbench -c 500 -t 5 http://1.15.5.78:1316/index
./webbench -c 1000 -t 5 http://1.15.5.78:1316/index
./webbench -c 5000 -t 5 http://1.15.5.78:1316/index
./webbench -c 9000 -t 5 http://1.15.5.78:1316/index
```
* 测试环境: 云服务器Ubuntu Server 18.04.1 LTS 64位 
* CPU:1核 内存:2GB
* QPS 9000+


```bash
./webbench -c 9000 -t 5 http://192.168.214.128:1316/index
./webbench -c 10000 -t 5 http://192.168.214.128:1316/index
./webbench -c 15000 -t 5 http://192.168.214.128:1316/index
```
* 测试环境: Ubuntu Server 18.04.1 LTS 64位 
* CPU:4核 内存:8GB
* QPS 15000+

---

## 常用命令


##### 查看启动的server程序

ps -A -ostat,ppid,pid,cmd | head -1;ps -A -ostat,ppid,pid,cmd | grep server

##### 查看占用端口的通信

netstat -anp | grep 1316


##### webbench压力测试

./webbench -c 10000 -t 5 http://1.15.5.78:1316/index

./webbench -c 10000 -t 5 http://192.168.214.128:1316/index

##### 启动服务器

./bin/server
