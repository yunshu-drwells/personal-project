## 文件IO





### 标准C库IO函数

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210627160758261.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzODA4NzAw,size_16,color_FFFFFF,t_70)






### 标准C库IO和Linux系统IO的关系

<a href="https://blog.csdn.net/qq_43808700/article/details/115855164?utm_source=app">IO标准库和系统调用接口</a>


- 第一：**系统IO是更底层的接口**，因此任何设备和文件最终都是可以通过系统IO来操作。**系统IO不提供缓冲区**，意味着每次读写都必须进入内核，对于大数据量的读写操作会影响效率。

- 第二：**标准IO是由标准库提供的接口**，因此功能更加丰富，而且**标准IO提供缓冲区，增加数据处理的吞吐量**。标准IO还对读写操作提供更加丰富的操作方式，例如按字节、按行、按块、按数据格式读写。但是有些特殊文件无法使用标准IO，比如socket套接口，比如LCD显示屏。

- 第三：在能使用标准IO的场合，我们尽量使用它，毕竟它功能丰富效率高，但在无法使用标准IO的场合，我们还是只能用系统IO。

- 第四：

- - 所谓的系统IO，就是指这样的一堆函数：open()、read()、wirte()、lseek()、ioctl()、close()等等

- - 所谓的标准IO，指的是这一堆函数：fopen()、fgets()、fread()、scanf()、getchar()、fputs()、fwrite()、printf()、fseek()、fclose()



![在这里插入图片描述](https://img-blog.csdnimg.cn/20210627162021438.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzODA4NzAw,size_16,color_FFFFFF,t_70)






### 虚拟地址空间

![在这里插入图片描述](https://img-blog.csdnimg.cn/2021062716301734.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzODA4NzAw,size_16,color_FFFFFF,t_70)







### 文件描述符

参考：<a href="https://blog.csdn.net/qq_43808700/article/details/115941000?utm_source=app">IO1-->文件描述符</a>

文件描述符本质：文件描述符,就是一个文件描述信息结构体数组files_struct的fd_array的下标。进程通过pcb的指针*files找到files_struct,进而找到fd_arry,再通过描述符找到具体的文件描述信息元素


![在这里插入图片描述](https://img-blog.csdnimg.cn/20210627164639179.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzODA4NzAw,size_16,color_FFFFFF,t_70)














### 系统IO函数(系统调用)

- int open (const char pathname, int flags);
- int open(const char pathname, int flags, mode_t mode);
- int close(int fd);
- ssize_t read(int fd, void *buf, size_t count);
- ssize_t write(int fd, const void -buf, size_t count);
- off_t lseek(int fd, off_t offset, int whence);
- int stat(const char ^pathname, struct stat *statbuf);
- int 1 sial (const: char * pathname, struct stat *statbuf);


> flags:O_RDONLY,O_WRONLY,O_RDWR
> mode:文件权限，u:所有者, g:所属组,o:其他人
> fd:文件描述符

> man手册(Manual)第2章是系统调用；第二章是库函数


#### stat结构体

```
struct stat  
{   
    dev_t       st_dev;     /* ID of device containing file -文件所在设备的ID*/  
    ino_t       st_ino;     /* inode number -inode节点号*/    
    mode_t      st_mode;    /* protection -保护模式?*/    
    nlink_t     st_nlink;   /* number of hard links -链向此文件的连接数(硬连接)*/    
    uid_t       st_uid;     /* user ID of owner -user id*/    
    gid_t       st_gid;     /* group ID of owner - group id*/    
    dev_t       st_rdev;    /* device ID (if special file) -设备号，针对设备文件*/    
    off_t       st_size;    /* total size, in bytes -文件大小，字节为单位*/    
    blksize_t   st_blksize; /* blocksize for filesystem I/O -系统块的大小*/    
    blkcnt_t    st_blocks;  /* number of blocks allocated -文件所占块数*/    
    time_t      st_atime;   /* time of last access -最近存取时间*/    
    time_t      st_mtime;   /* time of last modification -最近修改时间*/    
    time_t      st_ctime;   /* time of last status change - */    
};
```











### 文件属性操作函数

- int access(const char "pathname, int mode);
判断某个文件是否有某个权限，或者判断文件是否存在
- int chmod(consr char *filename, int mode);
修改文件的权限
- int chown(const char *path, uid_t owner, gid_t group);
改变文件的所有者和组
- int truncate(const char *path, off_t length);
缩减或者扩展文件的尺寸至指定的大小












### 目录遍历函数

- DIR *opendir(const char *name); 
- struct dirent *readdir(DIR *dirp); 
- int closedir(DIR *dirp);

#### dirent结构体

```
struct dirent
{
　　long d_ino; /* inode number 索引节点号 */
    off_t d_off; /* offset to this dirent 在目录文件中的偏移 */
    unsigned short d_reclen; /* length of this d_name 文件名长 */
    unsigned char d_type; /* the type of d_name 文件类型 */
    char d_name [NAME_MAX+1]; /* file name (null-terminated) 文件名，最长255字符 */
}
```

#### d_type

```
enum
{
    DT_UNKNOWN = 0,         //未知类型
# define DT_UNKNOWN DT_UNKNOWN
    DT_FIFO = 1,            //管道
# define DT_FIFO DT_FIFO
    DT_CHR = 2,             //字符设备
# define DT_CHR DT_CHR
    DT_DIR = 4,             //目录
# define DT_DIR DT_DIR
    DT_BLK = 6,             //块设备
# define DT_BLK DT_BLK
    DT_REG = 8,             //常规文件
# define DT_REG DT_REG
    DT_LNK = 10,            //符号链接
# define DT_LNK DT_LNK
    DT_SOCK = 12,           //套接字
# define DT_SOCK DT_SOCK
    DT_WHT = 14             //链接
# define DT_WHT DT_WHT
};
```











### dup、dup2函数

- int dup(int oldfd);
复制文件描述符
- int dup2(int oldfd, int newfd);
更定向文件描述符














### fcntl函数

- int fcntl (int fd, int cmd, . . . /* arg */ );
夏制文件描述符、设置/获取义件的状态标志