# Sliding Window 滑动窗口

## 适用场景

- 求子数组/子字符串的最大/最小值
- 固定窗口大小的统计
- 满足某条件的最长/最短连续子序列

## 核心思路

维护一个可变或固定大小的窗口 `[left, right]`，通过移动右指针扩展窗口，条件不满足时移动左指针收缩窗口。

## 模板

```python
def sliding_window(s):
    left = 0
    window = {}   # 窗口内的状态
    result = 0

    for right in range(len(s)):
        # 扩展窗口：将 s[right] 加入窗口
        window[s[right]] = window.get(s[right], 0) + 1

        # 收缩条件：窗口不合法时移动 left
        while 窗口不合法:
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1

        # 更新结果
        result = max(result, right - left + 1)

    return result
```

## 复杂度

- 时间：O(n)，每个元素最多进出窗口各一次
- 空间：O(k)，k 为字符集大小或窗口最大元素数

## 常见变体

| 变体 | 说明 |
|------|------|
| 固定窗口 | 窗口大小固定为 k，直接移动 |
| 可变窗口（最长） | right 不断扩展，left 在不满足时才收缩 |
| 可变窗口（最短） | left 在满足条件时收缩以求最小值 |

## 经典题目

- LC 3: 无重复字符最长子串
- LC 76: 最小覆盖子串（hard）
- LC 567: 字符串的排列
- LC 438: 找所有字母异位词
