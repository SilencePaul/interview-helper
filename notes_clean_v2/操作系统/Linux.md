# Linux

---

## 速览

- I/O 多路复用三种实现：select（有 fd 上限）、poll（无上限但线性扫描）、epoll（事件驱动，最高效）。
- epoll 核心优势：红黑树注册 + 就绪链表通知，只返回就绪的 fd，O(1) 复杂度。
- epoll 两种触发模式：LT（水平触发，默认，可重复通知）、ET（边缘触发，只通知一次）。
- 软链接 = 路径快捷方式（可跨文件系统，目标删除后失效）；硬链接 = inode 的额外引用（只能在同一文件系统）。
- 端口占用检查：`netstat -tuln`、`lsof -i :端口号`、`ss -tuln`。

---

## I/O 多路复用：select / poll / epoll

> **一句话理解：** select 和 poll 每次调用都要遍历所有 fd；epoll 只需注册一次，有事件才通知，大连接场景碾压前两者。

**核心结论（可背）：**
| 特性 | select | poll | epoll |
|---|---|---|---|
| fd 数量限制 | 有（默认 1024） | 无理论限制 | 无理论限制 |
| 数据结构 | 位图数组 | 结构体数组（pollfd） | 红黑树（注册）+ 就绪链表（通知） |
| 内核扫描方式 | 每次线性扫描所有 fd | 每次线性扫描所有 fd | 事件驱动，O(1) |
| 拷贝开销 | 每次调用都拷贝整个 fd 集合 | 每次调用都拷贝 fd 集合 | 只需一次注册，只返回就绪 fd |
| 边缘触发（ET） | ❌ | ❌ | ✅ |
| 适合场景 | < 1000 连接 | 1000~5000 连接 | 高并发（万级连接以上） |

**工作原理对比：**
```
select / poll 模型：
  用户态 fd 集合 ──拷贝──► 内核遍历所有 fd（线性扫描）
  ◄──返回──  哪些 fd 就绪（需重新扫描找出来）
  缺点：每次调用都全量拷贝 + 全量扫描

epoll 模型（事件驱动）：
  epoll_create()  → 创建 epoll 实例（内核红黑树）
  epoll_ctl()     → 注册感兴趣的 fd 和事件（只注册一次）
  epoll_wait()    → 阻塞等待，有就绪事件时只返回就绪的 fd 列表
  优势：大量 fd 下性能不随连接数增加而下降
```

**LT vs ET 触发模式：**
```
LT（Level Triggered，水平触发）：
  fd 就绪后，如果用户没有读完数据，下次 epoll_wait 仍会通知
  → 更容易编程，不容易漏事件（默认模式）

ET（Edge Triggered，边缘触发）：
  fd 从未就绪变为就绪时只通知一次，之后不再通知
  → 性能更高，但必须一次性读完所有数据（否则丢事件）
  → Nginx 使用 ET 模式
```

**代码示例：**
```c
// epoll 基本使用
int epfd = epoll_create(1024);

struct epoll_event ev;
ev.events = EPOLLIN;     // 监听可读事件
ev.data.fd = sockfd;

epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);  // 注册

struct epoll_event events[MAX_EVENTS];
int n = epoll_wait(epfd, events, MAX_EVENTS, -1);  // 等待
// n 个就绪事件在 events 数组中
```

**面试官常问：**
- epoll 为什么比 select 快？→ 注册一次，不需每次全量拷贝；只返回就绪 fd，不需全量扫描；红黑树 + 就绪链表，O(1) 事件获取。
- Nginx 为什么高性能？→ epoll + ET 模式 + 非阻塞 IO + 单线程事件循环。

🎯 **Interview Triggers:**
- epoll 相比 select 和 poll 的核心优势是什么？（WHY）
- epoll 内部用了哪些数据结构，为什么选这些结构？（MECHANISM）
- LT 和 ET 触发模式分别适合什么场景，各有什么风险？（TRADEOFF）
- 如果 ET 模式下没有一次性读完数据会发生什么？（FAILURE）
- Nginx 为什么选择 epoll 的 ET 模式而不是 LT 模式？（SCENARIO）

🧠 **Question Type:** I/O 多路复用机制对比与底层原理题

🔥 **Follow-up Paths:**
- epoll → 红黑树与就绪链表的协作细节
- epoll → 内核态与用户态数据拷贝优化（mmap）
- ET 模式 → 非阻塞 I/O 配合使用的必要性
- Nginx 架构 → 事件驱动单线程模型
- epoll → 与 kqueue（BSD）、IOCP（Windows）的横向对比
- I/O 多路复用 → 与多线程 I/O 方案的性能权衡

🛠 **Engineering Hooks:**
- 生产环境高并发服务器（如 Redis、Nginx）均基于 epoll，理解 epoll 是读懂这类源码的前提
- ET 模式必须配合非阻塞 socket（`O_NONBLOCK`），否则单次读取阻塞会导致连接卡死
- `epoll_ctl` 的 `EPOLLET` 标志位控制触发模式，线上排查事件丢失时优先检查此标志
- 大量短连接场景下 epoll 的就绪链表优势最明显，长连接且活跃度低的场景 select 开销也可接受
- `epoll_wait` 返回值为 -1 且 errno 为 EINTR 时需重试，常见于信号中断场景

---

## 常用 Linux 命令

> **一句话理解：** 按功能分类记忆，重点掌握文件、进程、网络三大类。

**文件操作：**
| 命令 | 用途 | 示例 |
|---|---|---|
| `ls -l` | 列出目录详细信息 | `ls -la /home` |
| `cp -r` | 复制文件/目录 | `cp -r dir1/ dir2/` |
| `mv` | 移动或重命名 | `mv old.txt new.txt` |
| `rm -rf` | 强制删除目录 | `rm -rf /tmp/dir`（慎用！） |
| `find` | 文件查找 | `find /etc -name "*.conf"` |
| `chmod` | 修改权限 | `chmod 755 script.sh` |
| `chown` | 修改所有者 | `chown user:group file.txt` |

**文件内容查看：**
| 命令 | 用途 | 示例 |
|---|---|---|
| `cat` | 查看文件内容 | `cat file.txt` |
| `tail -f` | 实时追踪日志 | `tail -f app.log` |
| `grep` | 文本搜索 | `grep "error" file.log` |
| `wc -l` | 统计行数 | `wc -l file.txt` |

**进程管理：**
| 命令 | 用途 | 示例 |
|---|---|---|
| `ps aux` | 查看所有进程 | `ps aux | grep java` |
| `top / htop` | 实时进程监控 | `top` |
| `kill -9` | 强制终止进程 | `kill -9 1234` |
| `nice / renice` | 设置进程优先级 | `nice -n 10 ./run.sh` |

**网络管理：**
| 命令 | 用途 | 示例 |
|---|---|---|
| `ping` | 测试连通性 | `ping google.com` |
| `curl` | 请求 URL | `curl -X POST https://api.example.com` |
| `netstat -tuln` | 查看监听端口 | `netstat -tuln` |
| `ss -tuln` | 更快的 netstat 替代 | `ss -tuln | grep 8080` |
| `lsof -i` | 查看端口占用 | `lsof -i :8080` |

**磁盘管理：**
| 命令 | 用途 | 示例 |
|---|---|---|
| `df -h` | 查看磁盘空间 | `df -h` |
| `du -sh` | 查看目录大小 | `du -sh /var/log` |

🎯 **Interview Triggers:**
- 线上服务器 CPU 突然飙高，你会用哪些命令排查？（SCENARIO）
- `ps aux` 和 `top` 有什么区别，分别适合什么场景？（COMPARISON）
- `kill -9` 和 `kill -15` 的区别是什么？（MECHANISM）
- 如何用命令快速找出占用磁盘最多的目录？（IMPLEMENTATION）

🧠 **Question Type:** Linux 运维命令实操与故障排查题

🔥 **Follow-up Paths:**
- `top` 命令 → 各字段含义（%us、%sy、load average）
- 进程管理 → 僵尸进程的产生与清理
- `grep` 命令 → 正则表达式与管道组合使用
- 文件权限 → chmod 数字表示与 rwx 映射
- 网络排查 → `tcpdump` 抓包与 `strace` 系统调用追踪

🛠 **Engineering Hooks:**
- 线上排查优先用 `ss` 替代 `netstat`，前者更快且在新系统中默认可用
- `tail -f` 与 `grep --line-buffered` 组合可实时过滤日志关键字，生产排查常用
- `lsof -p <PID>` 可查看某进程打开的所有文件描述符，排查 fd 泄漏时非常有用
- `awk '{print $NF}' | sort | uniq -c | sort -rn` 是日志统计的万能管道组合
- 使用 `nice -n 19` 启动低优先级批处理任务，避免影响线上服务的 CPU 分配

---

## 端口占用检查

> **一句话理解：** 常用 `lsof -i :端口号` 或 `ss -tuln`，比 netstat 更快更现代。

**核心结论（可背）：**
```bash
# 方法1：netstat（传统，可能需要安装）
netstat -tuln | grep :8080

# 方法2：lsof（显示占用进程详情）
lsof -i :8080

# 方法3：ss（推荐，更快）
ss -tuln | grep :8080

# 方法4：fuser（显示 PID）
fuser 8080/tcp

# 方法5：netcat 测试端口
nc -zv 127.0.0.1 8080
```

🎯 **Interview Triggers:**
- 部署服务时提示端口已被占用，如何快速定位是哪个进程？（SCENARIO）
- `ss` 相比 `netstat` 有哪些优势？（COMPARISON）
- 如何检查远程主机的某个端口是否开放？（IMPLEMENTATION）
- 线上出现大量 TIME_WAIT 连接，应如何排查和处理？（FAILURE）

🧠 **Question Type:** 网络端口排查与 TCP 连接状态诊断题

🔥 **Follow-up Paths:**
- 端口占用 → TCP 连接状态机（TIME_WAIT、CLOSE_WAIT 的产生原因）
- `ss` 命令 → `-s` 选项查看连接统计摘要
- 端口检测 → 防火墙规则（iptables / firewalld）对端口可达性的影响
- `lsof` → 结合 `-p` 参数排查进程资源泄漏
- 端口扫描 → `nmap` 在安全审计和连通性测试中的使用

🛠 **Engineering Hooks:**
- 大量 TIME_WAIT 通常因短连接频繁建立导致，可通过开启 `tcp_tw_reuse` 缓解
- `ss -s` 一行命令输出各状态连接数统计，监控脚本中比 `netstat | wc -l` 更高效
- 容器环境中 `lsof` 可能看不到宿主机进程，需进入对应 namespace 或使用 `nsenter`
- 端口被占用但 `lsof` 无输出时，考虑内核 socket 未完全释放，重启网络服务或等待超时
- 生产脚本中用 `nc -z host port` 做健康检查比 `telnet` 更易于脚本化处理

---

## 软链接 vs 硬链接

> **一句话理解：** 软链接是路径快捷方式，目标删了就失效；硬链接是 inode 的另一个名字，不受原文件删除影响。

**核心结论（可背）：**
| 维度 | 软链接（Symbolic Link） | 硬链接（Hard Link） |
|---|---|---|
| 本质 | 独立文件，存储目标路径 | 目录项直接指向同一 inode |
| 跨文件系统 | ✅ 可以 | ❌ 不可以 |
| 链接目录 | ✅ 可以 | ❌ 不可以 |
| 原文件删除后 | 链接失效（悬空链接） | 链接仍然有效（inode 引用计数不为 0） |
| inode 计数 | 不增加原文件 inode 引用计数 | 增加 inode 引用计数（计数为 0 才释放） |
| 创建命令 | `ln -s target link_name` | `ln target link_name` |

**机制解释：**
```
硬链接原理：
  文件系统中，文件名 → inode → 数据块
  硬链接 = 新增一个文件名 → 指向同一个 inode
  删除原文件名 → inode 引用计数 -1，计数 > 0 时数据不会被删除

软链接原理：
  软链接文件本身是一个独立 inode，内容是目标文件的路径字符串
  访问软链接 → 读取路径 → 跳转到目标文件
  目标删除后软链接成为"悬空链接"（dangling link）

使用场景：
  软链接：版本管理（/usr/bin/python → /usr/bin/python3.11）、跨目录引用
  硬链接：备份文件（不占额外空间），确保文件不被意外删除
```

🎯 **Interview Triggers:**
- 软链接和硬链接的本质区别是什么？（CONCEPT）
- 为什么硬链接不能跨文件系统，而软链接可以？（MECHANISM）
- inode 引用计数什么时候归零，文件数据才会被真正删除？（MECHANISM）
- 生产环境中软链接的典型使用场景是什么？（SCENARIO）
- 如果误删了原文件，硬链接还能访问数据吗？（FAILURE）

🧠 **Question Type:** 文件系统 inode 机制与链接类型原理题

🔥 **Follow-up Paths:**
- inode → inode 包含哪些元数据（权限、时间戳、数据块指针）
- 硬链接 → 为什么目录不能创建硬链接（防止目录图成环）
- 软链接 → 软链接链式引用（链接指向链接）的处理机制
- 文件系统 → ext4 中 inode 表的组织方式
- 文件删除 → `unlink` 系统调用与 inode 引用计数的关系
- 版本管理 → 软链接在多版本软件切换中的工程实践

🛠 **Engineering Hooks:**
- 系统升级 Python 版本时常用软链接切换 `/usr/bin/python`，`pyenv` 底层也依赖此机制
- `ls -li` 可查看 inode 号，验证两个文件是否为同一 inode（硬链接关系）
- 容器镜像构建中大量使用硬链接共享基础层文件，节省磁盘空间（如 Docker overlay2）
- 软链接悬空问题可用 `find /path -xtype l` 批量检测，CI 部署后可加入健康检查
- 日志轮转（logrotate）依赖 inode 不变性：rename 日志文件后进程仍写入同一 inode，直到收到 SIGHUP 重新打开

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| select vs poll vs epoll 区别？ | fd 限制（有/无/无）；扫描方式（线性/线性/事件驱动）；适合连接数（小/中/大） |
| epoll 为什么高效？ | 红黑树注册（一次性），就绪链表通知（O(1)），只返回就绪 fd |
| LT vs ET 模式？ | LT：持续通知直到处理完（默认，安全）；ET：只通知一次（高效，需一次读完） |
| 软链接 vs 硬链接？ | 软：路径快捷方式，目标删除失效；硬：inode 别名，目标删除不影响 |
| 如何查看端口占用？ | `lsof -i :端口` 或 `ss -tuln | grep 端口` |
| Nginx 为什么高并发？ | epoll + ET 边缘触发 + 非阻塞 IO + 事件驱动单线程模型 |
