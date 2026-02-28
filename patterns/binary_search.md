# Binary Search 二分查找

## 适用场景

- 有序数组中查找目标值
- 查找左/右边界
- 在单调函数上查找满足条件的最小/最大值（二分答案）

## 核心思路

每次将搜索空间缩小一半，前提是搜索空间具有单调性（一侧满足条件，另一侧不满足）。

## 三种模板

### 基础：精确查找

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 查找左边界

```python
def left_bound(nums, target):
    left, right = 0, len(nums)   # 左闭右开
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid          # 继续向左收缩
    return left  # 检查 left 是否越界且等于 target
```

### 查找右边界

```python
def right_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1       # 继续向右收缩
        else:
            right = mid
    return left - 1  # 检查是否等于 target
```

## 关键细节对比

| 问题 | left/right 初值 | 循环条件 | mid 计算 |
|------|----------------|---------|---------|
| 精确查找 | `0, n-1` (闭区间) | `left <= right` | `left + (right-left)//2` |
| 左边界 | `0, n` (左闭右开) | `left < right` | 同上 |
| 右边界 | `0, n` | `left < right` | 同上 |

## 二分答案

当答案具有单调性时，可对答案范围做二分：

```python
# "最小化最大值" / "最大化最小值" 类题型
def binary_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if check(mid):   # mid 满足条件
            hi = mid     # 尝试更小的答案
        else:
            lo = mid + 1
    return lo
```

## 复杂度

- 时间：O(log n)
- 空间：O(1)

## 经典题目

- LC 704: 二分查找（基础）
- LC 34: 在排序数组中查找元素的第一个和最后一个位置
- LC 33: 搜索旋转排序数组
- LC 875: 爱吃香蕉的珂珂（二分答案）
