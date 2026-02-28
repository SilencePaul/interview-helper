# Two Pointers 双指针

## 适用场景

- 有序数组中的两数之和/差
- 链表中点、环检测
- 数组原地去重、移除元素
- 回文串判断

## 核心思路

使用两个指针（相向或同向）遍历数据结构，避免嵌套循环，将 O(n²) 降至 O(n)。

## 两种模式

### 对撞指针（相向）

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
```

**使用条件**：数组已排序，寻找满足某关系的两个元素。

### 快慢指针（同向）

```python
def remove_duplicates(nums):
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

**使用条件**：链表中点/环检测，数组原地修改。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 链表中的双指针

| 问题 | 技巧 |
|------|------|
| 找中点 | 快指针走2步，慢指针走1步 |
| 找倒数第k个 | 快指针先走k步，再同速移动 |
| 检测环 | 快慢指针，相遇则有环 |
| 找环入口 | 相遇后一指针回头，同速再次相遇 |

## 经典题目

- LC 21: 合并两个有序链表
- LC 141/142: 环形链表
- LC 167: 两数之和 II（有序数组）
- LC 26: 删除有序数组中的重复项
