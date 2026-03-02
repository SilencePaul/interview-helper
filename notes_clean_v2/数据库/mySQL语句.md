# MySQL 常考语句

---

## 速览

- 面试 SQL 考察重点：多表连接、聚合分组、子查询、事务控制、索引使用。
- 高频陷阱：`HAVING` vs `WHERE`、`NULL` 判断、`OFFSET` 分页性能、`IS NULL` 写法。
- 悲观锁用 `FOR UPDATE`，乐观锁用版本号字段 + CAS 更新。

---

## 数据查询（SELECT）

> **一句话理解：** SELECT 是面试最高频考点，重点掌握过滤、排序、分页和去重。

**核心结论（可背）：**
| 需求 | 写法 |
|---|---|
| 基础查询 | `SELECT * FROM users;` |
| 条件过滤 | `WHERE age > 25` |
| 排序 | `ORDER BY age DESC` |
| 去重 | `SELECT DISTINCT city FROM users` |
| 分页 | `LIMIT 10 OFFSET 20` |
| 模糊匹配 | `WHERE name LIKE 'A%'` |
| 范围查询 | `WHERE age BETWEEN 20 AND 30` |
| NULL 判断 | `WHERE phone IS NULL`（不能用 `= NULL`） |
| 别名 | `SELECT name AS username` |

**易错点：**
- ❌ 用 `WHERE phone = NULL` → 必须用 `IS NULL`，`= NULL` 永远返回 false。
- ❌ `LIKE '%A%'` 前置通配符导致索引失效。

🎯 **Interview Triggers:**
- 为什么 `= NULL` 永远返回 false？（MECHANISM）
- `LIKE '%A%'` 为什么会导致索引失效？（MECHANISM）
- 大 OFFSET 分页为什么慢，如何优化？（TRADEOFF）
- `SELECT *` 和 `SELECT 具体列` 有什么区别？（TRADEOFF）
- `DISTINCT` 的实现原理是什么，性能如何？（MECHANISM）

🧠 **Question Type:** principle explanation · mechanism explanation · debugging/failure analysis · comparison/tradeoff

🔥 **Follow-up Paths:**
- `LIKE '%A%'` → 前缀不确定 → B+ 树无法定位起始位置 → 退化为全表扫描
- 大 OFFSET → 扫描并丢弃 OFFSET 条记录 → 数据量越大越慢 → 改用游标分页（WHERE id > last_id）
- `SELECT *` → 读取所有列 → 无法利用覆盖索引 → 增加 IO 和网络传输量

🛠 **Engineering Hooks:**
- 分页接口对外暴露时，禁止允许调用方传入任意 OFFSET，设置最大页数上限防止深分页攻击。
- 模糊搜索需求如果必须前缀通配，考虑引入 Elasticsearch 替代 MySQL LIKE，保持 MySQL 只做结构化查询。
- 覆盖索引可以避免回表：SELECT 的字段全在索引中时，EXPLAIN 的 Extra 列会显示 `Using index`。
- 生产 SQL 禁止 `SELECT *`，明确列名既避免不必要数据传输，也防止表结构变更导致业务逻辑隐性出错。
- NULL 判断统一用 `IS NULL` / `IS NOT NULL`，代码注释中说明该字段是否允许 NULL 及其业务含义。

---

## 多表连接与子查询

> **一句话理解：** 内连接取交集，左连接保左表全量，子查询可替换为 JOIN 提升性能。

**核心结论（可背）：**
| 类型 | 写法 | 结果 |
|---|---|---|
| 内连接 | `JOIN ... ON` | 两表都有才返回 |
| 左连接 | `LEFT JOIN ... ON` | 左表全返回，右表没有补 NULL |
| 右连接 | `RIGHT JOIN ... ON` | 右表全返回，左表没有补 NULL |
| 子查询（WHERE） | `WHERE id IN (SELECT ...)` | 过滤用 |
| 子查询（FROM） | `FROM (SELECT ...) t` | 派生表 |

**面试常见场景：**
```sql
-- 查每个用户的最后一笔订单
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN (
    SELECT user_id, MAX(order_time) AS last_time
    FROM orders GROUP BY user_id
) t ON o.user_id = t.user_id AND o.order_time = t.last_time;

-- 查重复数据
SELECT name, COUNT(*) AS cnt
FROM users
GROUP BY name
HAVING cnt > 1;
```

🎯 **Interview Triggers:**
- 子查询和 JOIN 在性能上有什么区别？（TRADEOFF）
- LEFT JOIN 中 WHERE 条件和 ON 条件的区别？（SCENARIO）
- `IN` 子查询和 `EXISTS` 子查询分别适合什么场景？（COMPARISON）
- 如何查找每组中的最大值记录？（SCENARIO）
- 关联字段没有索引时 JOIN 性能会怎样？（FAILURE）

🧠 **Question Type:** comparison/tradeoff · scenario application · debugging/failure analysis · mechanism explanation

🔥 **Follow-up Paths:**
- IN 子查询 → 外表小内表大时效率低 → 改用 EXISTS → 内表走索引逐条验证，更高效
- LEFT JOIN 过滤条件写在 WHERE → NULL 行被过滤 → 语义变为 INNER JOIN → 结果与预期不符
- 派生表子查询 → MySQL 5.7 之前不能物化 → 每次外层查询都执行一遍内层 → 改写为 WITH 或临时表

🛠 **Engineering Hooks:**
- `IN (子查询)` 数据量大时考虑改写为 JOIN，MySQL 对 JOIN 的优化比 IN 子查询更成熟。
- 子查询结果集小于 1000 行时 IN 性能尚可；超过万行必须评估是否改为 JOIN 或分批处理。
- EXISTS 适合外表小、内表大且内表有索引的场景；IN 适合内表结果集小的场景。
- 复杂子查询用 WITH（CTE）重写，提升可读性同时让优化器有更多优化空间（MySQL 8.0+）。
- 关联字段必须建索引，用 EXPLAIN 确认 JOIN 类型不是 `ALL`，否则数据量稍大即出现性能问题。

---

## 聚合与分组

> **一句话理解：** GROUP BY 分组，HAVING 过滤分组结果，WHERE 过滤原始行。

**核心结论（可背）：**
| 函数 | 用途 | 示例 |
|---|---|---|
| `COUNT(*)` | 总行数（含 NULL） | `SELECT COUNT(*) FROM users` |
| `COUNT(col)` | 非 NULL 行数 | `SELECT COUNT(phone) FROM users` |
| `SUM / AVG` | 求和 / 平均 | `SELECT AVG(age) FROM users` |
| `MAX / MIN` | 最大 / 最小 | `SELECT MAX(age) FROM users` |
| `GROUP BY` | 分组 | `GROUP BY city` |
| `HAVING` | 过滤分组后的结果 | `HAVING COUNT(*) > 10` |

**WHERE vs HAVING（必考）：**
```
WHERE  → 在分组前过滤原始行（可以走索引）
HAVING → 在分组后过滤聚合结果（不能用非聚合列且不走索引）
```

**易错点：**
- ❌ 用 WHERE 过滤聚合函数结果 → 必须用 HAVING。
- ❌ SELECT 中出现非聚合、非 GROUP BY 的列 → 语义不明确，严格模式下报错。

🎯 **Interview Triggers:**
- WHERE 和 HAVING 的本质区别是什么？（MECHANISM）
- `COUNT(*)` 和 `COUNT(列名)` 有什么不同？（COMPARISON）
- GROUP BY 之后 SELECT 出现非聚合列为什么会报错？（WHY）
- 聚合查询如何优化，索引能起到什么作用？（TRADEOFF）
- 如何统计每个分组中不重复值的数量？（SCENARIO）

🧠 **Question Type:** principle explanation · comparison/tradeoff · mechanism explanation · scenario application

🔥 **Follow-up Paths:**
- WHERE 先过滤行 → 减少参与 GROUP BY 的数据量 → 聚合计算更快 → 尽量用 WHERE 前置过滤
- GROUP BY 字段有索引 → 利用索引顺序分组 → 避免额外排序 → Extra 不出现 `Using filesort`
- 严格模式关闭 → 非聚合列取值不确定 → 不同 MySQL 版本结果不一致 → 生产环境必须开启严格模式

🛠 **Engineering Hooks:**
- 统计去重数量用 `COUNT(DISTINCT col)`，但大数据量下性能差，可改用 HyperLogLog 估算（Redis PFCOUNT）。
- GROUP BY 字段建索引可避免额外排序，EXPLAIN 中 Extra 出现 `Using filesort` 是优化信号。
- 生产环境开启 `sql_mode=STRICT_TRANS_TABLES`，强制 SELECT 中不能出现非聚合非 GROUP BY 的列。
- HAVING 不走索引，数据量大时先用 WHERE 减少分组前的行数，再用 HAVING 过滤分组结果。
- 聚合查询结果缓存在 Redis 中（如排行榜），避免每次请求都触发全表扫描聚合。

---

## 数据写入与更新

> **一句话理解：** 写操作注意幂等性，批量插入效率远高于逐条插入。

**核心结论（可背）：**
| 操作 | 写法 |
|---|---|
| 插入 | `INSERT INTO users(name, age) VALUES('Alice', 30)` |
| 批量插入 | `VALUES ('Bob', 25), ('Cathy', 22)` |
| 冲突时更新 | `ON DUPLICATE KEY UPDATE name='Tom'` |
| 更新 | `UPDATE users SET age = 28 WHERE id = 1` |
| 删除 | `DELETE FROM users WHERE age < 18` |
| 清空表 | `TRUNCATE TABLE users`（比 DELETE 快，不写 binlog 每行） |

🎯 **Interview Triggers:**
- TRUNCATE 和 DELETE 的区别是什么？（COMPARISON）
- `ON DUPLICATE KEY UPDATE` 的使用场景和注意事项？（SCENARIO）
- 批量插入为什么比逐条插入效率高得多？（MECHANISM）
- UPDATE 不带 WHERE 条件会怎样？如何防止？（FAILURE）
- 大批量 DELETE 为什么要分批执行？（TRADEOFF）

🧠 **Question Type:** comparison/tradeoff · mechanism explanation · debugging/failure analysis · scenario application

🔥 **Follow-up Paths:**
- 逐条 INSERT → 每条都有网络往返 + 事务提交开销 → 批量合并为一条 INSERT → 性能提升数十倍
- TRUNCATE → 直接释放数据页 → 不记录每行 binlog → 速度快但无法回滚也不触发 DELETE 触发器
- 大批量 DELETE 一次执行 → 持有行锁时间过长 → 阻塞其他读写 → 改为 `LIMIT 1000` 循环分批删除

🛠 **Engineering Hooks:**
- 批量插入单次建议不超过 1000 行，过大会导致 binlog 单条事件过大，影响主从复制延迟。
- `ON DUPLICATE KEY UPDATE` 在自增主键场景下会消耗主键 ID（即使未插入成功），高并发下会导致 ID 跳跃。
- 危险操作（DELETE/UPDATE 无 WHERE）在生产环境用 `sql_safe_updates=ON` 模式强制拦截。
- 大表数据归档用 `INSERT INTO archive SELECT ... LIMIT 1000` + `DELETE ... LIMIT 1000` 循环，控制锁持有时间。
- 软删除（is_deleted 标记）比物理删除更安全，可恢复，但需配合索引过滤和定期归档清理。

---

## 索引与性能优化

> **一句话理解：** EXPLAIN 是诊断慢查询的第一工具，务必掌握。

**核心结论（可背）：**
| 操作 | 写法 |
|---|---|
| 查看索引 | `SHOW INDEX FROM users` |
| 创建索引 | `CREATE INDEX idx_age ON users(age)` |
| 删除索引 | `DROP INDEX idx_age ON users` |
| 执行计划 | `EXPLAIN SELECT * FROM users WHERE age > 30` |
| 强制指定索引 | `FORCE INDEX (idx_age)` |
| 慢查询日志 | `SHOW VARIABLES LIKE 'slow_query_log%'` |

**EXPLAIN 关键字段：**
| 字段 | 含义 | 关注值 |
|---|---|---|
| `type` | 访问类型 | `ALL`（全表扫）→ 需优化；`ref`/`range` 较好；`const` 最好 |
| `key` | 实际使用的索引 | NULL 说明没走索引 |
| `rows` | 估计扫描行数 | 越小越好 |
| `Extra` | 额外信息 | `Using filesort`、`Using temporary` 需优化 |

🎯 **Interview Triggers:**
- EXPLAIN 中 type 为 ALL 说明什么，如何优化？（DEBUGGING）
- 什么情况下索引会失效？（FAILURE）
- 覆盖索引是什么，为什么能提升性能？（MECHANISM）
- 联合索引的最左前缀原则是什么？（PRINCIPLE）
- `Using filesort` 和 `Using temporary` 分别代表什么问题？（MECHANISM）

🧠 **Question Type:** debugging/failure analysis · mechanism explanation · principle explanation · scenario application

🔥 **Follow-up Paths:**
- 索引列做函数运算 → 索引失效 → 改为对常量侧做运算 → 保持索引列干净
- `Using filesort` → ORDER BY 字段不在索引中 → 内存/磁盘额外排序 → 在 ORDER BY 字段上建索引
- 联合索引跳过最左列 → B+ 树无法定位起始节点 → 索引失效 → 重新规划联合索引列顺序

🛠 **Engineering Hooks:**
- 索引失效六大场景：对索引列使用函数、隐式类型转换、前缀通配符 LIKE、OR 条件、NOT IN/!=、NULL 判断（部分情况）。
- 联合索引设计口诀：区分度高的列放左边，查询频率高的列放左边，排序列和过滤列对齐。
- 在线加索引用 `ALTER TABLE ... ALGORITHM=INPLACE`（MySQL 5.6+），避免锁表，大表也能不停服操作。
- EXPLAIN rows 只是估算，实际行数可能偏差较大，对关键 SQL 用 `EXPLAIN ANALYZE`（MySQL 8.0+）获取真实执行数据。
- 定期执行 `pt-duplicate-key-checker` 检查重复索引，删除冗余索引减少写操作维护开销。

---

## 事务与锁操作

> **一句话理解：** 显式事务 + 悲观锁/乐观锁，是高并发写入的标配。

**核心结论（可背）：**
| 操作 | 语句 |
|---|---|
| 开启事务 | `BEGIN` 或 `START TRANSACTION` |
| 提交 | `COMMIT` |
| 回滚 | `ROLLBACK` |
| 设置隔离级别 | `SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ` |
| 查看隔离级别 | `SELECT @@transaction_isolation` |
| 悲观锁（排他锁） | `SELECT * FROM users WHERE id = 1 FOR UPDATE` |
| 悲观锁（共享锁） | `SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE` |

**乐观锁模板：**
```sql
-- 读取版本号
SELECT stock, version FROM products WHERE id = 1;

-- 带版本号更新，版本号不匹配则影响 0 行，需重试
UPDATE products
SET stock = stock - 1, version = version + 1
WHERE id = 1 AND version = 3;
```

🎯 **Interview Triggers:**
- 悲观锁和乐观锁分别适合什么场景？（COMPARISON）
- 事务隔离级别有哪些，分别解决什么问题？（MECHANISM）
- 死锁是如何产生的，如何排查和预防？（FAILURE）
- `FOR UPDATE` 锁的是行还是表，什么情况下会退化为表锁？（MECHANISM）
- 乐观锁 CAS 更新影响 0 行后如何处理？（SCENARIO）

🧠 **Question Type:** comparison/tradeoff · mechanism explanation · debugging/failure analysis · scenario application · principle explanation

🔥 **Follow-up Paths:**
- FOR UPDATE 查询条件不走索引 → 行锁退化为表锁 → 并发全部串行化 → 系统吞吐骤降
- 两个事务互相等待对方的锁 → 死锁 → InnoDB 自动检测并回滚代价小的事务 → 业务层需重试
- 乐观锁高并发下冲突率高 → 大量重试 → CPU 空转 → 改用悲观锁或队列串行化写入

🛠 **Engineering Hooks:**
- 事务中操作多张表时，所有事务保持相同的加锁顺序（如先锁 A 表再锁 B 表），可消灭死锁。
- `FOR UPDATE` 必须在事务中使用，事务外的 FOR UPDATE 立即释放锁，起不到保护作用。
- 乐观锁适合读多写少、冲突概率低的场景；悲观锁适合写多、冲突概率高、不能接受重试的场景。
- 死锁日志在 `SHOW ENGINE INNODB STATUS` 的 LATEST DETECTED DEADLOCK 段，记录死锁的两个事务详情。
- 长事务是锁持有时间过长的根因，生产环境用 `information_schema.innodb_trx` 监控并告警超过 5 秒的活跃事务。

---

## 高频场景题汇总

| 场景 | 解法关键点 |
|---|---|
| 每个用户的最后一笔订单 | `GROUP BY user_id` + `MAX(order_time)` 再 JOIN |
| 查重复数据 | `GROUP BY` + `HAVING COUNT(*) > 1` |
| 查某字段为空 | `WHERE col IS NULL`（不能用 `= NULL`） |
| 查某天的记录 | `WHERE DATE(create_time) = '2024-01-01'`（注意索引失效）|
| 分页优化（大 OFFSET） | 改为 `WHERE id > last_id LIMIT 10`（游标分页） |
| 统计不重复值数量 | `COUNT(DISTINCT col)` |

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| WHERE vs HAVING？ | WHERE 过滤行（分组前），HAVING 过滤分组（分组后） |
| NULL 怎么判断？ | `IS NULL` / `IS NOT NULL`，不能用 `=` |
| 大 OFFSET 分页为什么慢？ | 需扫描并丢弃 OFFSET 条记录，改用游标分页 |
| EXPLAIN 看什么？ | type（访问类型）、key（是否走索引）、rows（扫描行数）|
| 悲观锁和乐观锁实现？ | `FOR UPDATE` vs 版本号字段 |
| TRUNCATE vs DELETE？ | TRUNCATE 不逐行写 binlog，速度更快，但不可回滚 |
