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
