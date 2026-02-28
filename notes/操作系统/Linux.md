Linux
说一下 select、poll、epoll的区别和应用场景？
一、基本概念
I/O多路复用是一种在单个线程或进程中处理多个输入和输出操作的机制。它允许单个进程同时监视多个文件描述符(通常是套接字)，当一个或多个文件描述符准备好读或写时，它就可以立即响应。
I/O多路复用通常通过select、poll、epoll等系统调用来实现。
select： select是一个最古老的I/O多路复用机制，它可以监视多个文件描述符的可读、可写和错误状态。然而，但是它的效率可能随着监视的文件描述符数量的增加而降低。
poll： poll是select的一种改进，它使用轮询方式来检查多个文件描述符的状态，避免了select中文件描述符数量有限的问题。但对于大量的文件描述符，poll的性能也可能变得不足够高效。
epoll： epoll是Linux特有的I/O多路复用机制，相较于select和poll，它在处理大量文件描述符时更加高效。epoll使用事件通知的方式，只有在文件描述符就绪时才会通知应用程序，而不需要应用程序轮询。
I/O多路复用允许在一个线程中处理多个I/O操作，避免了创建多个线程或进程的开销，允许在一个线程中处理多个I/O操作，避免了创建多个线程或进程的开销。
二、原理图示意
select / poll 模型
用户态                   内核态
┌──────────┐       ┌──────────────┐
│ fd 数组  │─────►│ 轮询所有 fd   │
└──────────┘       └──────────────┘
       ▲                    │
       └────────<───────────┘
          每次调用都需拷贝整个 fd 集合
epoll 模型（事件驱动）
用户态                   内核态
┌────────────┐      ┌───────────────────────┐
│ epoll_ctl()│────► │ 注册事件到红黑树      │
└────────────┘      └───────────────────────┘
     ▲                         │
     │ epoll_wait()            ▼
     └────────────<────────────┐
   只拷贝就绪的 fd，不轮询所有 fd
三、详细对比
特性	select	poll	epoll
fd 数量限制	有（默认 1024）	无理论限制	无理论限制
数据结构	位图数组	结构体数组	红黑树（注册）+ 就绪链表（通知）
拷贝开销	每次调用都拷贝 fd 集	每次调用都拷贝 fd 集	仅一次注册，等待时只返回就绪集合
内核开销	每次线性扫描所有 fd	每次线性扫描所有 fd	O(1)，事件驱动
支持边缘触发	否	否	支持（ET 模式）
适合场景	小规模并发连接	中等连接规模	高并发、大量连接
四、应用场景建议
场景	推荐方式
并发连接 < 1000	select
并发连接 1000 - 5000	poll
高并发服务器（上万连接）	epoll
支持异步事件驱动模型	epoll
五、代码风格对比（C）
select 示例：
fd_set rfds;
FD_ZERO(&rfds);
FD_SET(sockfd, &rfds);
select(sockfd+1, &rfds, NULL, NULL, NULL);
epoll 示例：
int epfd = epoll_create(1024);
struct epoll_event ev = {EPOLLIN, {.fd = sockfd}};
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);
epoll_wait(epfd, events, MAX_EVENTS, -1);
熟悉哪些Linux命令？
文件操作类
命令	用途	示例
ls	列出目录内容	ls -l /home
cd	切换目录	cd /var/log
pwd	显示当前路径	pwd
mkdir	创建目录	mkdir newdir
rm	删除文件或目录	rm file.txt，rm -rf dir/
cp	复制文件或目录	cp a.txt b.txt，cp -r dir1/ dir2/
mv	移动或重命名文件	mv old.txt new.txt
touch	创建空文件或修改时间戳	touch file.txt
文件内容查看
命令	用途	示例
cat	查看文件内容	cat file.txt
less / more	分页查看文件内容	less file.txt
head	查看前 N 行	head -n 10 file.txt
tail	查看后 N 行或实时追踪	tail -n 20 file.txt，tail -f file.txt
wc	统计行数/字数/字符数	wc -l file.txt
grep	文本搜索	grep "error" file.log
find	文件查找	find /etc -name "*.conf"
file	查看文件类型	file image.jpg
权限与用户管理
命令	用途	示例
chmod	修改文件权限	chmod 755 script.sh
chown	更改文件所有者	chown user:group file.txt
umask	设置默认权限掩码	umask 022
whoami	显示当前用户名	whoami
id	显示当前用户ID信息	id
sudo	以超级用户权限执行命令	sudo apt update
passwd	修改用户密码	passwd
adduser / useradd	添加用户	adduser newuser
usermod / deluser	修改/删除用户	usermod -aG sudo user，deluser user
网络管理
命令	用途	示例
ping	测试网络连通性	ping google.com
curl / wget	下载网络资源	curl https://example.com
ifconfig / ip	查看/配置网络接口	ip a
netstat / ss	查看网络连接	netstat -tuln，ss -tuln
traceroute	路由追踪	traceroute google.com
nslookup / dig	DNS 查询	nslookup baidu.com
telnet / nc	测试端口连接	nc -zv 127.0.0.1 80
进程管理
命令	用途	示例
ps	查看进程	ps aux
top / htop	实时进程监控	top（htop 更美观）
kill	终止进程	kill 1234
killall	按名称终止进程	killall firefox
nice / renice	设置进程优先级	nice -n 10 ./run.sh
bg / fg	后台/前台任务切换	fg %1
jobs	查看当前 shell 的作业	jobs
磁盘与文件系统管理
命令	用途	示例
df	查看磁盘空间	df -h
du	查看目录/文件大小	du -sh /var/log
mount / umount	挂载/卸载设备	mount /dev/sdb1 /mnt
lsblk	查看磁盘分区结构	lsblk
blkid	查看设备UUID等信息	blkid
fdisk / parted	分区工具	fdisk /dev/sda
mkfs	格式化文件系统	mkfs.ext4 /dev/sdb1
fsck	检查并修复文件系统	fsck /dev/sda1
软件包管理
命令	用途	示例
apt update	更新软件源	sudo apt update
apt upgrade	升级系统包	sudo apt upgrade
apt install	安装软件	sudo apt install vim
apt remove	删除软件	sudo apt remove nginx
dpkg -i	安装 .deb 包	sudo dpkg -i pkg.deb
如何查看某个端口有没有被占用？
在 Linux 中可以使用多种方法来查看端口是否被占用：
netstat：使用 netstat -tuln | grep :<端口号>。
lsof：使用 lsof -i :<端口号> 查看端口占用情况。
ss：使用 ss -tuln | grep :<端口号>。
netcat：使用 nc -zv 127.0.0.1 <端口号>。
fuser：使用 fuser <端口号>/tcp。
Linux中的软链接和硬链接有什么区别？
物理实现：
软链接： 软链接是一个独立的文件，它包含了指向目标文件或目录的路径。软链接实际上是一个特殊的文件，其中包含有关目标文件的引用。
硬链接： 硬链接是目标文件的一个额外的目录项。目录项指向相同的物理数据块，实际上只是文件系统中的两个或多个目录项指向相同的inode。
链接的目标：
软链接： 软链接可以链接到文件或目录，甚至可以链接到不存在的文件。
硬链接： 硬链接只能链接到文件，而且必须是同一文件系统中的。
对链接的影响：
软链接： 如果原始文件被删除或移动，软链接仍然存在，但链接将失效。软链接可以跨文件系统，但如果目标文件被删除，软链接将成为坏链接（dangling link）。
硬链接： 删除或移动原始文件并不会影响硬链接，因为硬链接只是inode的另一个引用。只有当所有硬链接都被删除后，inode的数据块才会被释放。
创建方式：
软链接： 使用ln -s命令创建软链接。例如，ln -s target_file link_name。
硬链接： 使用ln命令创建硬链接。例如，ln target_file link_name。
链接数量：
软链接： 软链接只会增加目标文件的链接计数，而不会增加inode的链接计数。
硬链接： 硬链接会增加目标文件的链接计数，也会增加inode的链接计数。当链接计数为零时，文件系统才会释放相关的数据块。
