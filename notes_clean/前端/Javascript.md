# JavaScript

---

## 速览

- JS 有 8 种数据类型：7 种原始类型（Number/String/Boolean/Null/Undefined/Symbol/BigInt）+ Object（引用类型）。
- 判断类型：typeof（原始类型）、instanceof（原型链）、Object.prototype.toString（最准确）、constructor。
- 原型链：每个对象有 `__proto__` 指向构造函数的 `prototype`，`prototype.constructor` 指回构造函数，链尾为 `null`。
- 继承最优解：寄生组合继承（ES5）/ class extends（ES6）。
- 闭包：函数 + 函数创建时所在词法环境，可访问外部函数变量，常用于数据私有化，注意内存泄漏。
- this 四种绑定规则：new > 显式(call/apply/bind) > 隐式(对象方法) > 默认(全局)；箭头函数无自己的 this。
- Promise 三种状态：pending → fulfilled / rejected（不可逆）。async/await 是 Promise + Generator 语法糖。
- 事件流三阶段：捕获（顶→目标）→ 目标 → 冒泡（目标→顶）；事件委托利用冒泡减少事件绑定。
- 垃圾回收：标记-清除（现代主流）；常见内存泄漏：全局变量、定时器未清除、闭包引用。
- ES6 核心：let/const、解构、箭头函数、Class、Promise、async/await、Map/Set、Proxy、模块化(import/export)。

---

## 数据类型与判断

> **一句话理解：** JS 有 8 种类型，原始类型存栈，引用类型存堆（栈存指针），typeof 能判断基础类型，Object.prototype.toString 最精确。

**核心结论（可背）：**
```
原始类型（7种，按值传递）：
  Number、String、Boolean、Null、Undefined、Symbol（ES6）、BigInt（ES10）

引用类型（按引用传递）：
  Object（含 Array、Function、Date、RegExp、Map、Set...）
```

**四种类型检测方式：**
| 方式 | 原理 | 局限 |
|---|---|---|
| `typeof` | 返回字符串，检测原始类型 | `null` 返回 `"object"`（历史 bug）；无法区分 Array/Object |
| `instanceof` | 检查原型链上是否存在构造函数的 `prototype` | 不能判断原始类型；跨 iframe 失效 |
| `constructor` | 对象的 `constructor` 属性指向构造函数 | null/undefined 无 constructor |
| `Object.prototype.toString.call(x)` | 返回 `[object Type]`，最准确 | 写法稍麻烦 |

```javascript
typeof null           // "object"（bug，null 是原始类型）
typeof undefined      // "undefined"
typeof function(){}   // "function"
typeof []             // "object"

[] instanceof Array   // true
{} instanceof Object  // true

Object.prototype.toString.call([])        // "[object Array]"
Object.prototype.toString.call(null)      // "[object Null]"
Object.prototype.toString.call(undefined) // "[object Undefined]"
```

**null vs undefined：**
```
null：明确表示"空值/无对象"，是主动赋的值，typeof → "object"（历史 bug）
undefined：变量声明未赋值、函数无返回值、对象属性不存在，typeof → "undefined"
NaN：Not a Number，typeof → "number"；NaN !== NaN，用 Number.isNaN() 判断
```

---

## 类型转换

> **一句话理解：** `==` 会隐式类型转换，`===` 严格比较不转换，面试常考 `== null`、`+` 运算符、`Boolean()` 假值。

**核心结论（可背）：**
```
隐式转换规则（== 比较）：
  null == undefined → true（仅这一对）
  NaN == 任何值    → false（包括自身）
  原始类型 == 对象  → 对象调用 valueOf/toString 转原始类型
  number vs string  → string 转 number 再比较

显式转换：
  转数字：Number()、parseInt()、parseFloat()、+
  转字符串：String()、toString()、模板字符串
  转布尔：Boolean()，以下 6 种为 false：false/0/""/null/undefined/NaN
```

**0.1 + 0.2 精度问题：**
```
0.1 + 0.2 === 0.30000000000000004（不等于 0.3）

原因：IEEE 754 双精度浮点数，0.1 和 0.2 的二进制表示是无限循环小数，存储时被截断，
     运算时产生精度误差。

解决：
  1. Number.EPSILON 误差比较：Math.abs(0.1+0.2-0.3) < Number.EPSILON
  2. toFixed(n) 保留 n 位小数：(0.1+0.2).toFixed(1) === "0.3"
  3. 转整数运算：(0.1*10 + 0.2*10) / 10 = 0.3
```

---

## 原型与原型链

> **一句话理解：** 每个对象有 `__proto__` 链接到父对象，构造函数有 `prototype` 对象，原型链就是 `__proto__` 一级级向上查找属性，直到 null。

**核心结论（可背）：**
```
三个核心概念：
  prototype：函数对象特有，是该构造函数创建的实例的原型
  __proto__：每个对象都有，指向自己的原型（即构造函数的 prototype）
  constructor：原型对象上的属性，指回构造函数自身

关系公式：
  实例.__proto__ === 构造函数.prototype
  构造函数.prototype.constructor === 构造函数
  Object.prototype.__proto__ === null（链尾）
```

```
原型链查找过程：
  obj.prop
    → obj 自身有？返回
    → obj.__proto__ 有？返回
    → obj.__proto__.__proto__ 有？返回
    → ... 直到 null → 返回 undefined
```

**instanceof 原理：**
```javascript
// instanceof 沿 __proto__ 链找 构造函数.prototype
function myInstanceof(obj, Constructor) {
  let proto = Object.getPrototypeOf(obj);
  while (proto) {
    if (proto === Constructor.prototype) return true;
    proto = Object.getPrototypeOf(proto);
  }
  return false;
}
```

---

## 继承（6种方案）

> **一句话理解：** 最优解是寄生组合继承（ES5）或 class extends（ES6），前者通过 Object.create 继承原型而不调用父构造函数，完美解决两次调用问题。

**核心结论（可背）：**
```
① 原型链继承：子.prototype = new 父()
   问题：引用类型属性被所有实例共享

② 构造函数继承：子构造函数中 call 父构造函数
   问题：无法继承父原型上的方法

③ 组合继承：① + ②
   问题：父构造函数被调用两次

④ 原型式继承：Object.create(父实例) 浅拷贝
   问题：同原型链继承，引用类型共享

⑤ 寄生式继承：在原型式基础上给新对象添加方法
   问题：不能复用方法

⑥ 寄生组合继承（最优）：
   - 用 构造函数继承 复制属性（call）
   - 用 Object.create(父.prototype) 继承原型（不调用父构造函数）
```

```javascript
// ✅ 寄生组合继承（面试最重要）
function Parent(name) {
  this.name = name;
}
Parent.prototype.sayName = function() { console.log(this.name); };

function Child(name, age) {
  Parent.call(this, name);  // 继承属性
  this.age = age;
}
// 继承原型（不调用 Parent 构造函数）
Child.prototype = Object.create(Parent.prototype);
Child.prototype.constructor = Child;

// ES6 等价写法
class Child extends Parent {
  constructor(name, age) {
    super(name);
    this.age = age;
  }
}
```

---

## 深拷贝与浅拷贝

> **一句话理解：** 浅拷贝只复制第一层（引用类型仍共享），深拷贝递归复制所有层（完全独立）。

**核心结论（可背）：**
| 方式 | 深/浅 | 局限 |
|---|---|---|
| `=` 赋值（引用类型） | — | 只复制引用，完全共享 |
| `Object.assign({}, obj)` | 浅拷贝 | 只复制第一层 |
| `{...obj}` 展开运算符 | 浅拷贝 | 只复制第一层 |
| `arr.slice()` / `arr.concat()` | 浅拷贝 | 数组元素若为对象仍共享 |
| `JSON.parse(JSON.stringify(obj))` | 深拷贝 | 不支持：函数/Symbol/undefined/循环引用/Date变字符串 |
| 递归手写深拷贝 | 深拷贝 | 需处理循环引用（WeakMap 记录已拷贝对象） |
| `structuredClone(obj)` | 深拷贝 | 现代浏览器原生 API，不支持函数 |

```javascript
// 手写深拷贝（处理循环引用）
function deepClone(obj, map = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (map.has(obj)) return map.get(obj);  // 处理循环引用
  const clone = Array.isArray(obj) ? [] : {};
  map.set(obj, clone);
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key], map);
    }
  }
  return clone;
}
```

---

## 闭包

> **一句话理解：** 闭包 = 函数 + 其创建时的词法环境，让内层函数可以访问并"记住"外层函数的变量，常用于数据私有化和函数工厂。

**核心结论（可背）：**
```
闭包产生条件：
  1. 函数嵌套
  2. 内层函数引用了外层函数的变量
  3. 内层函数在外层函数作用域之外被调用

闭包的应用：
  ① 数据私有化（模拟私有变量）
  ② 函数工厂（柯里化）
  ③ 防抖/节流
  ④ 模块化（IIFE 模式）

闭包的问题：
  外层函数执行完后，内层函数仍引用其变量 → 变量不被 GC 回收 → 内存泄漏
  解决：使用完后将闭包引用置为 null
```

```javascript
// 经典闭包：计数器（数据私有化）
function makeCounter() {
  let count = 0;  // 私有变量
  return {
    increment() { count++; },
    decrement() { count--; },
    getCount()  { return count; }
  };
}

// 经典面试题：for 循环 + 闭包
for (var i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 0);  // 输出 3 3 3
}
// 修复方案1：let 替换 var（块级作用域）
for (let i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 0);  // 输出 0 1 2
}
// 修复方案2：IIFE 创建闭包
for (var i = 0; i < 3; i++) {
  (function(j) { setTimeout(function() { console.log(j); }, 0); })(i);
}
```

---

## 作用域与执行上下文

> **一句话理解：** 作用域是变量的"有效范围"（词法的，编写时确定），执行上下文是代码"运行时的环境"，包含变量对象/作用域链/this。

**核心结论（可背）：**
```
作用域（Scope）——静态，编译时确定：
  全局作用域：整个脚本范围内有效
  函数作用域：函数内部有效（var 声明的变量）
  块级作用域：{} 块内有效（let/const，ES6）

词法作用域（静态作用域）：函数的作用域在函数定义时就已确定，不是在调用时确定

执行上下文（Execution Context）——动态，运行时创建：
  全局执行上下文（只有一个）
  函数执行上下文（每次调用创建一个）
  Eval 执行上下文

执行上下文包含：
  变量对象(VO)：存储变量/函数声明
  作用域链(SC)：当前变量对象 + 所有父级变量对象
  this 绑定
```

**变量提升与暂时性死区：**
```javascript
// var 变量提升（声明提升，赋值不提升）
console.log(a); // undefined（不报错）
var a = 1;

// 函数声明整体提升
sayHello();     // "Hello"（正常调用）
function sayHello() { console.log("Hello"); }

// let/const 暂时性死区（TDZ）
console.log(b); // ReferenceError: Cannot access 'b' before initialization
let b = 2;
```

---

## this 指向

> **一句话理解：** this 不是定义时确定，而是调用时确定，四种绑定优先级：new > 显式(call/apply/bind) > 隐式(对象方法) > 默认(全局/undefined)。

**核心结论（可背）：**
| 绑定方式 | 规则 | this 指向 |
|---|---|---|
| **new 绑定** | `new Foo()` | 新创建的对象 |
| **显式绑定** | `call/apply/bind` | 第一个参数指定的对象 |
| **隐式绑定** | `obj.fn()` | 调用对象 obj |
| **默认绑定** | 普通函数调用 `fn()` | 全局对象（严格模式为 undefined） |
| **箭头函数** | 无自己的 this | 继承外层词法作用域的 this（定义时确定） |

```javascript
// 隐式丢失（面试常考）
const obj = { name: 'obj', fn: function() { console.log(this.name); } };
const fn = obj.fn;
fn();  // undefined（this 变成全局，丢失 obj）

// 箭头函数 this
const obj2 = {
  name: 'obj2',
  fn: function() {
    const arrow = () => console.log(this.name);  // this 继承 fn 的 this
    arrow();
  }
};
obj2.fn();  // "obj2"
```

---

## call / apply / bind

> **一句话理解：** 三者都能改变 this，call/apply 立即执行，bind 返回新函数；call 逐个传参，apply 传数组。

**核心结论（可背）：**
```
fn.call(thisArg, arg1, arg2)      → 立即执行，参数逐个传
fn.apply(thisArg, [arg1, arg2])   → 立即执行，参数传数组
fn.bind(thisArg, arg1, arg2)      → 返回新函数，不立即执行，参数可提前绑定（柯里化）

注意：
  箭头函数的 this 无法被 call/apply/bind 改变
  bind 多次调用，this 仍指向第一次绑定的对象：fn.bind(1).bind(2)() → this 为 1
```

```javascript
// 手写 call
Function.prototype.myCall = function(context, ...args) {
  context = context || window;
  const key = Symbol();
  context[key] = this;
  const result = context[key](...args);
  delete context[key];
  return result;
};

// 手写 bind
Function.prototype.myBind = function(context, ...args) {
  const fn = this;
  return function(...newArgs) {
    return fn.apply(context, [...args, ...newArgs]);
  };
};
```

---

## 箭头函数 vs 普通函数

> **一句话理解：** 箭头函数没有自己的 this/arguments/prototype，不能作构造函数，不能 new，适合回调场景。

**核心结论（可背）：**
| 对比 | 普通函数 | 箭头函数 |
|---|---|---|
| this | 动态绑定（调用时确定） | 词法绑定（定义时继承外层 this） |
| arguments | 有 | 无（用 rest 参数替代） |
| prototype | 有 | 无 |
| new | 可以（构造函数） | 不可以（报错） |
| Generator | 可用 yield | 不可以 |

---

## ES6 核心特性

> **一句话理解：** ES6 是 JS 最重要的版本更新，let/const 解决变量作用域，Promise 解决回调地狱，class 提供更清晰的面向对象写法。

**核心结论（可背）：**

**let / const vs var：**
```
var：函数作用域，变量提升，可重复声明，可重新赋值
let：块级作用域，暂时性死区，不可重复声明，可重新赋值
const：块级作用域，暂时性死区，不可重复声明，不可重新赋值（引用类型属性可改）
```

**解构 & 扩展运算符：**
```javascript
const [a, b, ...rest] = [1, 2, 3, 4];   // 数组解构
const { name, age = 18 } = obj;          // 对象解构（带默认值）
const merged = { ...obj1, ...obj2 };     // 浅合并
const arr2 = [...arr1, 4, 5];            // 数组扩展
```

**Map vs Object / Set vs Array：**
```
Map：
  键可以是任何类型（Object 键只能是字符串/Symbol）
  记忆插入顺序，直接有 .size 属性
  适合频繁增删改查

Set：
  存储唯一值（无重复）
  常用于数组去重：[...new Set([1,1,2,3])] → [1,2,3]
  并集/交集/差集操作

WeakMap / WeakSet：
  键只能是对象，弱引用（不阻止 GC），不可遍历
  适合存储 DOM 元素相关数据，避免内存泄漏
```

**Symbol：**
```
Symbol()：创建唯一值，不可枚举，不可被 for...in 遍历
Symbol.iterator：自定义可迭代协议
Symbol.for('key')：全局 Symbol 注册表（同 key 返回同一 Symbol）
```

**Proxy：**
```javascript
// 拦截对象的读写操作
const proxy = new Proxy(target, {
  get(target, prop) { return Reflect.get(target, prop); },
  set(target, prop, value) { return Reflect.set(target, prop, value); }
});
// Vue3 用 Proxy 替代 Object.defineProperty 实现响应式
// 优点：可监听新增/删除属性，可监听数组索引，无需逐属性递归
```

---

## Promise & async/await

> **一句话理解：** Promise 解决回调地狱，有 pending/fulfilled/rejected 三种不可逆状态；async/await 是 Promise + Generator 的语法糖，让异步代码看起来像同步。

**核心结论（可背）：**
```
Promise 状态机：
  pending → fulfilled（resolve 触发）
  pending → rejected（reject 触发 / 抛出异常）
  状态一旦改变不可逆

Promise 链式调用：
  .then(onFulfilled, onRejected)  → 返回新 Promise
  .catch(onRejected)              → 等价于 .then(null, onRejected)
  .finally(fn)                    → 无论成功失败都执行，不改变状态
  错误具有"冒泡"性，会沿链传递直到被 catch 捕获

Promise 静态方法：
  Promise.all([p1, p2])      → 全部成功才成功，一个失败即失败
  Promise.allSettled([p1,p2]) → 全部结束（无论成败），返回每个结果状态
  Promise.race([p1, p2])     → 第一个状态改变的 Promise 的结果
  Promise.any([p1, p2])      → 第一个 fulfilled（全部 rejected 才 rejected）
```

```javascript
// async/await 基本用法
async function fetchData() {
  try {
    const res = await fetch('/api/data');  // await 暂停，等 Promise resolve
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);  // 捕获 rejected
  }
}

// await 阻塞原理：
// await 将后续代码放入微任务队列，先执行 async 函数外部的同步代码，
// 同步代码完成后，再回到 await 之后继续执行
```

**Generator 简介：**
```javascript
function* gen() {
  yield 1;  // 断点，每次 next() 执行到下一个 yield
  yield 2;
  return 3;
}
const iter = gen();
iter.next(); // { value: 1, done: false }
iter.next(); // { value: 2, done: false }
iter.next(); // { value: 3, done: true }
// async/await 是 Generator + 自动执行器 的语法糖
```

---

## 事件流与事件委托

> **一句话理解：** 事件流三阶段：捕获（从顶到目标）→ 目标 → 冒泡（从目标到顶）；事件委托将子元素事件委托给父元素，利用冒泡减少监听器数量。

**核心结论（可背）：**
```
事件流三阶段：
  1. 捕获阶段：window → document → html → ... → 目标的父元素
  2. 目标阶段：事件在目标元素处理
  3. 冒泡阶段：目标父元素 → ... → document → window

addEventListener(type, handler, useCapture)：
  useCapture = false（默认）：在冒泡阶段触发
  useCapture = true：在捕获阶段触发

阻止：
  event.stopPropagation()  → 阻止冒泡
  event.preventDefault()   → 阻止默认行为

e.target vs e.currentTarget：
  e.target：真正触发事件的元素（点击的元素）
  e.currentTarget：绑定事件处理程序的元素

不支持冒泡的事件：blur、focus、mouseenter、mouseleave、load
```

**事件委托：**
```javascript
// ❌ 每个 li 都绑定（性能差）
document.querySelectorAll('li').forEach(li => li.addEventListener('click', fn));

// ✅ 委托给父元素（推荐）
document.querySelector('ul').addEventListener('click', function(e) {
  if (e.target.tagName === 'LI') {
    console.log(e.target.textContent);  // e.target 就是点击的 li
  }
});
// 优点：减少事件监听器数量，动态添加的子元素自动继承事件
```

---

## 防抖与节流

> **一句话理解：** 防抖 = 操作停止后才执行（搜索联想）；节流 = 固定频率执行（滚动/resize）。

**核心结论（可背）：**
```
防抖（Debounce）：
  事件触发后等待 n 毫秒，如果期间再次触发则重新计时
  适用：搜索框输入、窗口 resize、表单提交防重复

节流（Throttle）：
  单位时间内只执行一次
  适用：scroll 事件、mousemove、游戏帧更新
```

```javascript
// 防抖
function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// 节流（时间戳版）
function throttle(fn, interval) {
  let last = 0;
  return function(...args) {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn.apply(this, args);
    }
  };
}
```

---

## 垃圾回收（GC）

> **一句话理解：** JS 引擎自动管理内存，现代 V8 使用标记-清除（老生代）+ Scavenge 复制算法（新生代）+ 分代回收策略。

**核心结论（可背）：**
```
标记-清除（Mark-Sweep）——现代主流算法：
  1. 从根（root）出发，标记所有可达对象（活动对象）
  2. 清除未被标记的对象（非活动对象）
  缺点：产生内存碎片

V8 分代回收：
  新生代（小/短生命，1~8M）：Scavenge 复制算法（from-space / to-space 互换）
  老生代（大/长生命）：标记-清除 + 标记-整理
  新生代对象经过多次 GC 存活 → 晋升到老生代

常见内存泄漏场景：
  ① 意外的全局变量（忘写 var/let）
  ② 闭包持有大对象引用
  ③ 定时器（setInterval）未清除
  ④ 事件监听器未移除
  ⑤ 已移除的 DOM 节点被 JS 变量引用
```

---

## 模块化（CommonJS / ES Module）

> **一句话理解：** CommonJS（require/module.exports）运行时同步加载，用于 Node.js；ES Module（import/export）编译时静态分析，是浏览器和现代 Node.js 标准。

**核心结论（可背）：**
| 对比 | CommonJS | ES Module |
|---|---|---|
| 语法 | `require()` / `module.exports` | `import` / `export` |
| 加载时机 | 运行时动态加载 | 编译时静态分析 |
| 导出 | 值拷贝（导出后变化不影响导入） | 值引用（实时绑定，同一内存） |
| 同步/异步 | 同步（适合 Node.js 本地文件） | 异步（适合浏览器） |
| 适用 | Node.js 服务端 | 浏览器 + 现代 Node.js |

```javascript
// CommonJS
const path = require('path');
module.exports = { add: (a, b) => a + b };

// ES Module
import { useState } from 'react';
export const add = (a, b) => a + b;
export default class App {}

// 动态 import（懒加载）
const module = await import('./heavy.js');
```

---

## Ajax / Fetch / Axios

> **一句话理解：** Ajax（XHR）是基础，Fetch 是原生 Promise API，Axios 是基于 XHR 的 Promise 封装库，三者都用于异步请求。

**核心结论（可背）：**
| 对比 | Ajax(XHR) | Fetch | Axios |
|---|---|---|---|
| 基于 | XMLHttpRequest | 原生 API（Promise） | XMLHttpRequest 封装 |
| Promise | 需封装 | 原生支持 | 原生支持 |
| 默认携带 Cookie | 是 | 否（需配置 credentials） | 是 |
| 请求拦截 | 否 | 否 | 是（interceptors） |
| 自动 JSON 解析 | 否 | 需手动 `.json()` | 是 |
| 超时配置 | 支持 | 需 AbortController | 直接配置 |
| 适用场景 | 原生兼容 | 简单请求 | 生产项目推荐 |

```javascript
// Fetch 基本用法
const data = await fetch('/api/user', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' }),
  credentials: 'include',  // 携带 Cookie
}).then(res => res.json());

// Axios 基本用法
const { data } = await axios.post('/api/user', { name: 'Alice' });
```

---

## 面试高频考点汇总

| 考点 | 核心答案 |
|---|---|
| JS 数据类型有哪些？ | 7 种原始类型（Number/String/Boolean/Null/Undefined/Symbol/BigInt）+ Object 引用类型 |
| typeof null 为什么是 "object"？ | JS 早期 bug，null 二进制以 000 开头被误判为对象，已沿用至今 |
| == 和 === 的区别？ | == 会隐式类型转换，=== 不转换；面试注意 null==undefined 为 true |
| 0.1+0.2 !== 0.3 的原因？ | IEEE 754 双精度浮点数表示有精度限制，二进制无限循环被截断产生误差 |
| 原型链是什么？ | 对象通过 `__proto__` 链接到原型，查找属性时逐级向上，直到 null |
| 深拷贝和浅拷贝的区别？ | 浅拷贝只复制第一层，引用类型仍共享；深拷贝递归复制所有层 |
| 闭包是什么，有什么问题？ | 函数+词法环境，可记住外层变量；问题：持有引用可能导致内存泄漏 |
| this 指向如何确定？ | new > call/apply/bind > obj.fn() > 全局；箭头函数继承外层词法 this |
| call/apply/bind 区别？ | call/apply 立即执行（前者逐参，后者数组），bind 返回函数不立即执行 |
| var/let/const 区别？ | var：函数作用域+变量提升；let：块级作用域+TDZ；const：同 let 但不可重赋值 |
| Promise 状态有哪些？ | pending/fulfilled/rejected，状态不可逆；all/allSettled/race/any |
| async/await 原理？ | 基于 Promise + Generator；await 将后续放入微任务队列 |
| 事件委托是什么？ | 将子元素事件监听委托给父元素，利用事件冒泡，减少监听器，支持动态元素 |
| 防抖和节流的区别？ | 防抖：停止触发后 n 毫秒执行（搜索）；节流：单位时间只执行一次（滚动）|
| CommonJS vs ES Module？ | CJS 运行时值拷贝同步；ESM 编译时值引用异步，是现代标准 |
| 垃圾回收机制？ | 标记-清除为主（V8 分代：新生代 Scavenge，老生代标记整理），避免内存泄漏 |
