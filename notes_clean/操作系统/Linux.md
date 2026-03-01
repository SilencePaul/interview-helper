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
