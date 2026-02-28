JavaScript
数据类型和运算符
有哪些数据类型
原始类型
Undefined, Null, Boolean, Number, String
ES6新增了Symbol和BigInt.
Symbol 代表独一无二的值,最大的用法是为对象定义唯一的属性名
BigInt 可表示任意大小的整数, 指安全存储、操作大整数。
数据处理
parseInt(5.4) 只保留整数部分，有基模式
解析一个字符串，并返回一个整数。parseInt相比Number，就没那么严格了，parseInt函数逐个解析字符，遇到不能转换的字符就停下来。
parseInt(string, radix)
string 必需，表示要被解析的字符串。radix 可选，表示要解析的数字的基数。该值介于 2 ~ 36 之间。
如果省略该参数或其值为 ‘0‘，则数字将以 10 为基础来解析。如果它以 ‘”0x”‘ 或 ‘”0X”‘ 开头，将以 16 为基数。
如果该参数小于 2 或者大于 36，则 ‘parseInt()‘ 将返回 ‘NaN‘。
parseFloat() 把值转换成浮点数,没有基模式
Number() 把给定的值转换成数字（可以是整数或浮点数）,Number()的强制类型转换与parseInt()和parseFloat()方法的处理方式相似，只是它转换的是整个值，而不是部分值。
Math.floor(4.33) 向下取整
Math.ceil(6.7) 向上取整
Math.round(6.19) 四舍五入
Math.abs(-1) 绝对值
String() 把给定的值转换成字符串
toFixed(2) 四舍五入
null&undefined
这两个基本数据类型分别都只有一个值，就是 undefined 和 null。
undefined 代表的含义是未定义，null 代表的含义是空对象。一般变量声明了但还没有定义的时候会返回 undefined,null 主要用于赋值给一些可能会返回对象的变量，作为初始化。
undefined 在 js 中不是一个保留字，这意味着我们可以使用 undefined 来作为一个变量名，这样的做法是非常危险的，它会影响我们对 undefined 值的判断。但是我们可以通过一些方法获得安全的 undefined 值，比如说 void 0。
当我们对两种类型使用 typeof 进行判断的时候，Null 类型化会返回 “object”，这是一个历史遗留的问题。当我们使用双等号对两种类型的值进行比较时会返回 true，使用三个等号时会返回 false。
typeof null为"Object"
在第一版JS中，变量的值被设计保存在一个32位内存单元中。该单元包含一个1或3位的类型标标志，和实际数据值。类型标志存储在单元的最后。包括以下2几种情况
000：object，数据为对象的引用
1：int，数据为 31 位的有符号整型
010：double，数据为一个双精度浮点数的引用
100：string，数据为一个字符串的引用
110：boolean，数据为布尔类型的值
特殊情况：
undefined 负的 2 的 30 次方（超出当时整型取值范围的一个数）
null 空指针
null的存储单元最后三位(即 标志位)和object一样，所以被误判为Object
引用类型
Object
Date
Array
RegExp
判断数据类型
一、常见判断：typeof
这个方法很常见，一般用来 判断基本数据类型，如：string，number，boolean，symbol，bigint（es10新增一种基本数据类型bigint），undefined等。返回数据类型的字符串形式
typeof 目前能返回string，number，boolean，symbol，bigint，unfined，object，function这八种判断类型，但是注意 null 返回的是 Object 。而且对于引用类型返回的是 object 因为所有的对象的原型最终都是 Object。
//例子
typeof "safsadff"; //"string"
typeof 145; //"number"
typeof false; //"boolean"
typeof undefined; //"undefined"
typeof function () {}; //"function"
typeof {}; //"object"
typeof Symbol(); //"symbol"
typeof null; //"object"
typeof[]; //"object"
typeof new Date(); //"object"
typeof new RegExp(); //"object"
typeof new Number(33) //"object"
typeof Null //"undefined"
为什么typeof null 是 Object 答：因为在JavaScript中，不同的对象都是使用二进制存储的，如果二进制前三位都是0的话，系统会判断为是Object类型，而null的二进制全是0，自然也就判断为Object 这个bug是初版本的JavaScript中留下的，扩展一下其他五种标识位：
000 对象
1 整型
010 双精度类型
100字符串
110布尔类型
二、 已知对象判断：instanceof
用来 判断引用数据类型的，判断基本数据类型无效 ，如：Object，Function，Array，Date，RegExp等，instanceof主要的作用就是判断一个实例是否属于某种类型
instanceof也可以判断一个实例是否是其父类型或者祖先类型
instanceof原理实际上就是查找目标对象的原型链
//例子
[]instanceof Array; // true
[]instanceof Object; // true
[1, 2, 3]instanceof Array // true
new Date()instanceof Date // true
手写实现一个：
//手写实现
function myInstance(L, R) { //L代表instanceof左边，R代表右边
    var RP = R.prototype
        var LP = L.__proto__ 
        while (true) {
            if (LP == null) {
                return false
            }
            if (LP == RP) {
                return true
            }
            LP = LP.__proto__
        }
}
console.log(myInstance({}, Object));
三、根据对象的构造器：constructor
与 instanceof 相似，但是对于 instanceof 只能再检测引用类型， 而 constructor 还可以检测基本类型，因为 constructor是原型对象的属性指向构造函数。
注意
null 和 undefined是无效的对象，因此是不会有 constructor 存在的，所以无法根据 constructor 来判断。
JS对象的 constructor 是不稳定的，这个主要体现在自定义对象上，当开发者重写prototype 后，原有的 constructor 会丢失，constructor 会默认为Object
类继承的也会出错，因为 Object 被覆盖了，检测结果就不对了
四 、对象原型链判断：Object.prototype.toString.call（这个是判断类型最准的方法）
toString 是Object 原型对象上的一个方法，该方法默认返回其调用者的具体类型，更严格的讲，是 toString运行时this指向的对象类型, 返回的类型格式为[object,xxx]，xxx是具体的数据类型，其中包括：String，Number，Boolean，Undefined，Null，Function，Date，Array，RegExp，Error，HTMLDocument… 基本上所有对象的类型都可以通过这个方法获取到。
必须通过 Object.prototype.toString.call 来获取，而不能直接 new Date().toString()， 从原型链的角度讲，所有对象的原型链最终都指向了Object，按照JS变量查找规则，其他对象应该也可以直接访问到Object的 toString 方法，而事实上，大部分的对象都实现了自身的 toString 方法，这样就可能会导致 Object 的 toString 被终止查找，因此要用 call 来强制执行 Object 的 toString 方法。
缺点：不能再细分
//例子
Object.prototype.toString.call("a")
"[object String]"
Object.prototype.toString.call(undefined)
"[object Undefined]"
Object.prototype.toString.call(null)
"[object Null]"
Object.prototype.toString.call(new Date())
"[object Date]"
简单来说，JavaScript 中我们有四种方法来判断数据类型。
一般使用 typeof 来判断基本数据类型，不过需要注意当遇到null的问题，这里不足就是不能判断对象具体类型（typeof xjj 只是Object不能看出是person）；
而在要判断一个对象的具体类型，就可以用 instanceof，但是也可能不准确，对于一些基础数据类型，数组等会被判断为object。
结合 typeof 和 instanceof 的特点，还能使用 constructor 来判断，他能判断基本类型和引用类型，但是对于 null 和 undefined 是无效的，以及 constructor 不太稳定。
最后如果需要判断准确的内置类型，就可以使用 object.prototype.toString.call，是根据原型对象上的 tostring 方法获取的，该方法默认返回其调用者的具体类型。
类型转换
类型
6种基本类型 null undefined number stringify boolean symbol
1种引用类型 object
对象转换为基本类型
对象转换为字符串
// 模拟 toString 返回的不是基本类型值，valueOf 返回的基本类型值
var obj = {

    toString: function () {
        return {}
    },

    valueOf: function () {
        return null
    }
}

String(obj) // "null"
对象转换为数字
先判断valueOf方法，再判断toString方法
// valueOf 和 toString 返回的都不是基本类型值
var obj = {

    valueOf: function () {
        return {}
    },

    toString: function () {
        return {}
    }
}

Number(obj) // Uncaught TypeError: Cannot convert object to primitive value
Object.create(null)创建的对象没有valueOf和toString方法，因此转换报错
一般情况，我们不会重写valueOf和toString，大部分对象valueOf返回的仍然是对象，因此对象转换为基本类型值可以直接看toString返回的值
显式强制类型转换
转换为字符串
如果对象有自定义toString方法，则返回toString方法的结果，若是toString返回的结果不是基本类型值，报错TypeError
var obj = {

    toString: function () {
        return {}
    }
}

String(obj) // Uncaught TypeError: Cannot convert object to primitive value

obj + "" // Uncaught TypeError: Cannot convert object to primitive value

obj.toString() // {}
转换为布尔类型
null undefined false +0 -0 NaN ""
其他情况都是真值
转换为数字类型
Number('') // 0

Number(null) // 0

Number(undefined) // NaN

Number(true) // 1

Number(false) // 0
对象首先被转换为相应基本类型值，再转换
Number([]) // 0

// [] valueOf 返回的是 []，因此继续调用 toString 得到基本类型值 ""，转换为数字为 0
隐式强制类型转换
转换为字符串
x+""，会将x转换为字符串，+ 运算符其中一个操作数是字符串，会执行字符串拼接操作
对象和字符串拼接时，**对象转为基本类型按转为数字转换，**先判断valueOf，再判断toString
var obj = {

    valueOf: function () {
        return 1
    },

    toString: function () {
        return 2
    }
}

obj + '' // '1'
转换为布尔值
发生布尔值隐式强制类型转换的情况
if (..)语句中的条件判断表达式
for ( .. ; .. ; .. )语句中的条件判断表达式（第二个）
while (..)和do..while(..)循环中的条件判断表达式
? :中的条件判断表达式
逻辑运算符 ||（逻辑或）和 &&（逻辑与）左边的操作数（作为条件判断表达式）
转换为数字类型
+ '2' // 2

'2' - 0 // 2

'2' / 1 // 2

'2' * 1 // 2

+ 'x' // NaN

'x' - 0 // NaN

'x' / 1 // NaN

'x' * 1 // NaN

1 + '2' // '12'

1 + + '2' // 3 即：1 + (+ '2')
== 和 ===
== 允许在相等比较中进行强制类型转换，而 === 不允许
比较规则
1、字符串和数字比较，字符串先转换为数字，再比较
2、其他类型和布尔类型比较，布尔类型转换为数字，再比较
3、对象和非对象比较，对象转换成基本类型值，按转换为数字的流程转换后进行比较。对象转换优先级最高
4、null 和 undefined，null == undefined， 其他类型和 null 均不相等，undefined 也是如此
5、特殊情况
NaN == NaN // false

-0 == +0 // true
两个对象比较，判断的是两个对象是否是同一个引用
"0" == false // true

// 第2条规则，false 转换为数字，结果为 0，等式变为 "0" == 0

// 两边类型不一致，继续转换，第1条规则，"0" 转换为数字，结果为 0，等式变为 0 == 0

false == [] // true

// 第3条规则，[] 转换基本类型值，[].toString()，结果为 ""，等式变为 "" == false

// 两边类型不一致，继续转换，第2条规则，false 转换为数字，结果为 0，等式变为 "" == 0

// 两边类型不一致，继续转换，第1条规则，"" 转换为数字，结果为 0，等式变为 0 == 0

0 == [] // true

// 第3条规则，[] 转换基本类型值，[].toString()，结果为 ""，等式变为 0 == ""

// 两边类型不一致，继续转换，第1条规则，"" 转换为数字，结果为 0，等式变为 0 == 0
parseInt&parseFloat
+和Number()转换数字是严格的，若一个值不完全是数字，就会失败
console.log(+"100px");//NaN

console.log(+" ");//0
从"100px"，"12pt"中将数值提取出来，parseInt和parseFloat派上用场，它们可以从字符串中读取数字，直到无法读取位置，若出现error，则返回收集到的数字
parseInt("100px");//100

parseInt("11.22px");//11

parseFloat("12.33px");//12.33

parseFloat("12.3.4");//12.3
没有数字可读取时，返回NaN
parseInt("a123");//NaN

parseInt(str,radix)

alert( parseInt('0xff', 16) ); // 255

alert( parseInt('ff', 16) ); // 255，没有 0x 仍然有效

alert( parseInt('2n9c', 36) ); // 123456
浮点数求和步骤
对阶
求和
规格化
对阶
判断指数位是否相同，即小数位是否对其，若指数位不同，需要对阶保证指数相同。
对阶时遵守小阶向大阶看齐原则，尾数向右移位，每移动一位，指数位加 1 直到指数位相同，即完成对阶。
本示例，0.1 的阶码为 -4 小于 0.2 的阶码 -3，故对 0.1 做移码操作
// 0.1 移动之前
0 + 011 1111 1011+ 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1010 

// 0.1 右移 1 位之后尾数最高位空出一位，（0 舍 1 入，此处舍去末尾 0）
0 + 011 1111 1100 +1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 101(0) 

// 0.1 右移 1 位完成
0 +011 1111 1100 +1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1101
尾数求和
// 0.1 和 0.2 都转化成二进制后再进行运算
0+011 1111 1100+1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1100 1101 // 0.1 
(+) 0+011 1111 1100+1001  1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1010 // 0.2
= 0+011 1111 1100+10 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0111 // 产生进位，待处理
规格化和舍入
由于产生进位，阶码需要+1，原阶码为011 1111 1100，+1后得到1000 10，转换为十进制，即1021，此时阶码为1021-1023= -2，此时符号位，指数位分别为0 + 011 1111 1101
尾部进位2位，去除最高位默认的1，因为最低位为1需要进行舍入操作，即在最低有效位上+1，若为0则直接舍去，若为1继续+1
  10 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0111 // + 1
=  0 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 1000 // 去除最高位默认的 1
=  0 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 0110 1000 // 最后一位 0 舍去
=  0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0100  // 尾数最后结果      
因此 IEE 754最终存储如下：
0+011 1111 1101+0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0100
最高位为1，得到二进制
2^-2 * 1.0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0100
转换为十进制
0.3 0000 0000 0000 0004
总结
精度损失 0.1和0.2转换为二进制出现无限循环情况，JS以64位双精度格式存储数字，最大可存储53位有效数字，超过此长度会被截取掉，造成精度损失
对2个64位双精度格式数据计算时，首先进行对阶处理(将阶码对齐，将小数点位置对齐),因此，小阶数在对齐时，有效数字会向右移动，超过有效位数的位被截取掉
当两个数据阶码对齐后进行加运算，得到的结果可能超过53位有效数字，超过的位会被截取掉
相加后因浮点数小数位限制截断的二进制数字转换为十进制时变成0.30000000000000004(15个0)
如何让其相等
设置一个误差范围(将结果与右边相减，若结果小于一个极小数，则正确)
极小数可以是 ES6 的 Number.EPSILON实质是一个可接受的最小误差范围, 一般来说为 Math.pow(2, -52)
function isEqual(a, b) {
    return Math.abs(a - b) < Number.EPSILON;
}
console.log(isEqual(0.1 + 0.2, 0.3)); // true
转成字符串,对字符串做加法运算
parseFloat((0.1 + 0.2).toFixed(10))
//toFixed四舍五入
toPrecision转换成数字
function strip(num, precision = 12) {
    return parseFloat(num.toPrecision(precision));
}
let x = strip(0.30000000000000004, 18)
    console.log(x)
    //toPrecision以指定的精度返回该数值对象的字符串表示，四舍五入到 precision 参数指定的显示数字位数。
    //默认去掉最低位的0
将计算数字提升10的N次方，即，将其转换为整数，结果转换为对应小数
(0.1*1000+0.2*1000)/1000==0.3
//true
十进制小数转二进制
十进制小数转二进制，具体做法是：用2乘十进制小数，可以得到积，将积的整数部分取出，再用2乘余下的小数 部分，又得到一个积，再将积的整数部分取出，如此进行，直到积中的小数部分为零，或者达到所要求的精度为止。
然后把取出的整数部分按顺序排列起来，先取的整数作为二进制小数的高位有效位，后取的整数作为低位有效位。（乘2取整，顺序排列）
举个例子：
27.0转化成二进制为11011.0
先把0.5转换为二进制小数
0.5*2=1.0 //积中小数部分为0

(27) 10=(11011) 2
(0.5) 10=(1.0) 2
合并整数和小数部分可得
(27.5) 10=(11011.1) 2
现在回到我们的主题，那么0.1转为二进制是多少呢？
0.1 * 2 = 0.2 --------------- 取整数 0，小数 0.2
0.2 * 2 = 0.4 --------------- 取整数 0，小数 0.4
0.4 * 2 = 0.8 --------------- 取整数 0，小数 0.8
0.8 * 2 = 1.6 --------------- 取整数 1，小数 0.6
0.6 * 2 = 1.2 --------------- 取整数 1，小数 0.2
0.2 * 2 = 0.4 --------------- 取整数 0，小数 0.4
0.4 * 2 = 0.8 --------------- 取整数 0，小数 0.8
0.8 * 2 = 1.6 --------------- 取整数 1，小数 0.6
0.6 * 2 = 1.2 --------------- 取整数 1，小数 0.2
...
所以0.1的二进制可以表示为0.000110011……(0011无限循环)，因此二进制无法精确保存类似0.1这样的小数。
因为javaScript存储方式是IEEE 754 标准浮点数表示常用的 双精度浮点数 表示法，其长度为8个字节，即64位比特
64位比特又可分为三个部分：
符号位S：第 1 位是正负数符号位（sign），0代表正数，1代表负数
指数位E：阶码，中间的 11 位存储指数（exponent），用来表示次方数，可以为正负数。在双精度浮点数中，指数的固定偏移量为1023
尾数位M：最后的 52 位是尾数（mantissa），超出的部分自动进一舍零。(能够真正决定数字精度)
0.1+0.2 为什么不等于 0.3
看下面的输出：
console.log(0.1 + 0.2)  // 结果是0.30000000000000004，而不是3
那么为什么不是呢~主要是因为在 JavaScript 中，数字是采用的IEEE 754的双精度标准进行存储。比如其中小数使用64位固定长度来表示的，其中的1位表示符号位，11位用来表示指数位，剩下的52位尾数位。
而其中，比如 0.1 转换为二进制是一个无限循环的数的，就会超过 52 位，就会导致精度缺少，所以在计算机中 0.1 只能存储成一个近似值
所以同理的， 0.1 + 0.2 会先分别转换为二进制然后进行相加后存储，最后取出来的时候转化为十进制，而这个值不够近似于0.3，所以就会出现不相等的结果。
那么如何避免呢？
常用简单的办法就是将浮点数转变为整数来计算。
简单了解 null 和 undefined
一句简单来说是：undefined 代表了不存在的值，null 代表了没有值。
也就是，比如对一个值声明后，没有赋值，输出他就是 undefined ，是不存在的，而当赋值为 null， 那么输出就是 null。
这两者还有一些区别点要注意：
//1
undefined == null //true，这里相等是因为 “==” 对他们做了转换
undefined === null //false
//undefined的值 是 null 派生来的，所以他们表面上是相等的

//2
let a;
typeof a; //undefined

let b = null;
typeof b; //object
这里为什么typeof b 输出为 Object 呢？
null 不是一个对象，尽管 typeof age输出的是 Object，逻辑上讲，null 值表示一个空对象指针，这是一个历史遗留问题，JS 的最初版本中使用的是 32 位系统，为了性能考虑使用低位存储变量的类型信息，000 开头代表是对象，null表示为全零，所以将它错误的判断为 Object。
undefined 和 undeclared 的区别
Undeclared（未声明） : 当尝试访问尚未使用 var、let 或 const 声明的变量时会发生这种情况。
Undefined（未定义） : 它发生在使用 var、let 或 const 声明变量但未赋值时。
在 JavaScript 中，两者很容易被混为一谈
typeof 对 undefined 和 undeclared 的 都返回 “undefined”
let a;
typeof a; // undefined
typeof b // undefined （实际上这里应该输出 undeclared 才是合适的）
我们访问 undeclared 变量的时候,是这样报错的：ReferenceError ： a is not defined。
var a;
console.log(a); //undefined
console.log(b); //ReferenceError: b is not defined
=== 和 == 以及 = 的区别
它们最主要的区别在于 == 对比时，若类型不相等，会先转换为相同类型，然后再来比较值。而 === 则不会，只能在相同类型下比较值，不会做类型转换。还有一个是 =，这个是赋值，不是运算符。
1、 === 这个比较简单。下面的规则用来判断两个值是否===相等：
如果类型不同，就不相等
如果两个都是数值，并且是同一个值，那么相等；(！例外)的是，如果其中至少一个是NaN，那么不相等。（判断一个值是否是NaN，只能用 isNaN() 来判断）
如果两个都是字符串，每个位置的字符都一样，那么相等；否则不相等。
如果两个值都是true，或者都是false，那么相等。
如果两个值都引用同一个对象或函数，那么相等；否则不相等。
如果两个值都是null，或者都是undefined，那么相等。
2、==
如果两个值类型相同，进行 === 比较。
如果两个值类型不同，他们可能相等。根据下面规则进行类型转换再比较：
如果一个是null、一个是undefined，那么相等。
如果一个是字符串，一个是数值，把字符串转换成数值再进行比较。
如果任一值是 true ，把它转换成 1 再比较；如果任一值是 false，把它转换成 0 再比较。
如果一个是对象，另一 个是数值或字符串，把对象转换成基础类型的值再比较。对象转换成基础类型，利用它的 toString 或者 valueOf 方法。js 核心内置类，会尝试 valueOf 先于 toString；例外的是 Date，Date利用的是toString转换。非 js 核心的对象，令说（比较麻烦，我也不大懂）
任何其他组合，都不相等。
有时会在结构读取属性值时会在前面加上 “？” 这个是可选链，表示判断空值的情况。
JavaScript NaN 属性
NaN 属性是代表非数字值的特殊值。该属性用于指示某个值不是数字。可以把 Number 对象设置为该值，来指示其不是数字值。
NaN 属性是一个不可配置（non-configurable），不可写（non-writable）的属性。但在ES3中，这个属性的值是可以被更改的，但是也应该避免覆盖。
编码中很少直接使用到 NaN。通常都是在计算失败时，作为 Math 的某个方法的返回值出现的（例如：Math.sqrt(-1)）或者尝试将一个字符串解析成数字但失败了的时候（例如：parseInt(“blabla”)）。
typeof NaN; // “number”
NaN 的特性
NaN是一个特殊值，它和自身不相等，是唯一一个非自反（自反，reflexive，即x === x不成立）的值。而NaN !== NaN 为 true。
使用 isNaN() 函数来判断一个值是否是 NaN 值。
isNaN&number.isNaN()
函数 isNaN 尝试将参数转换为数值，任何不能被转换为数值的的值都会返回 true，因此非数字值传入也会返回 true ，会影响 NaN 的判断
函数 Number.isNaN 首先判断传入参数是否为数字，如果是数字继续判断是否为 NaN ，这种方法对于 NaN 的判断更为准确
function typeOfNaN(x) {

    if (Number.isNaN(x)) {
        return 'Number NaN';
    }

    if (isNaN(x)) {
        return 'NaN';
    }
}

console.log(typeOfNaN('100F'));
// expected output: "NaN"

console.log(typeOfNaN(NaN));
// expected output: "Number NaN"
isFinite()&isNaN()
Infinity和-Infinity是特殊的数值
NaN代表一个error
它俩都是number类型，但不是"普通"数字
isNaN(val)，将val转换为数字，再测试是否为NaN
isNaN(NaN);//true

isNaN('merry');//true
值NaN独一无二，不等于任何东西，包括自身
NaN===NaN;//false
isFinite(val)将val转换为数字，若是常规数字而不是NaN/Infinity/-Infinity，则返回true
isFinite(11);//true

isFinite("merry");//false 因为是NaN

isFinite(Infinity);//false 因为是Infinity
在所有数字函数中，包括isFinite，空字符串或只有空格的字符串都被视为0
逻辑与 && 和 逻辑或 ||
一、逻辑与 && 和 逻辑或 ||
当我们操作数是布尔值的时候，逻辑与需要操作都为 true 才会返回 true，而逻辑或只需要操作数中有一个为 true 就会返回 true， 但是要是操作数不是布尔值呢？
二、下面语句的输出是？
console.log(0&&1)  //0
console.log(1&&2)  //2
console.log(0||1)  // 1
console.log(1||2)  //1
首先我们先看结论，再来分析为什么。
逻辑与操作符是一种短路操作符，也就是如果第一个操作数结果为 false，就不会对第二个操作数求值
逻辑或操作符也是一种短路操作符，但不同的是当第一个操作结果为 true，就不会对第二个操作符求值
只要“&&”前面是false，无论“&&”后面是true还是false，结果都将返“&&”前面的值;
只要“&&”前面是true，无论“&&”后面是true还是false，结果都将返“&&”后面的值;
只要“||”前面为false,不管“||”后面是true还是false，都返回“||”后面的值。
只要“||”前面为true,不管“||”后面是true还是false，都返回“||”前面的值。
需要补充的是在 在 JavaScript 逻辑运算中，0、”“、null、false、undefined、NaN都会判为false，其他都为true
三、短路的特性的作用
在使用中可以避免变量赋值为 null 或者 undefined ，1
let myObject = perferredObject || backupObject
还可以做空值判断，因为在我们的一些对象中是没发判断是否存在的，获取不到的，所以需要做空值判断
{{ data.owner && data.owner.avatar }}
数组
数组方法
创建数组
Array.from() 浅拷贝
const dp = Array(5).fill();
const dp = Array.from(Array(m + 1), () => Array(n + 1).fill(0));
从类数组对象或者可迭代对象中创建一个新的数组实例。 Array.from还可以接受第二个参数，作用类似于数组的map方法，用来对每个元素进行处理，将处理后的值放入返回的数组。
Array.of()
根据一组参数来创建新的数组实例，支持任意的参数数量和类型，没有参数时返回 []，当参数只有一个的时候，实际上是指定数组的长度。
sort原理
对数组进行排序，默认排序顺序规则是将元素转换为字符串，然后比较它们的 UTF-16 代码单元值序列时构建的 。
copyWithin()
将指定位置的成员复制到其他位置（会覆盖原有成员），然后返回当前数组。
target（必需）：从该位置开始替换数据。如果为负值，表示倒数。
start（可选）：从该位置开始读取数据，默认为 0。如果为负值，表示从末尾开始计算。
end（可选）：到该位置前停止读取数据，默认等于数组长度。如果为负值，表示从末尾开始计算。
[1, 2, 3, 4, 5].copyWithin(0, 3);
// 将从 3 号位直到数组结束的成员（4 和 5），复制到从 0 号位开始的位置，结果覆盖了原来的 1 和 2
// [4, 5, 3, 4, 5] 
find()
find()用于找出第一个符合条件的数组成员
参数是一个回调函数，接受三个参数依次为当前的值、当前的位置和原数组
findIndex()
findIndex返回第一个符合条件的数组成员的位置，如果所有成员都不符合条件，则返回-1
find和findIndex这两个方法都可以接受第二个参数，用来绑定回调函数的this对象。
fill()
还可以接受第二个和第三个参数，用于指定填充的起始位置和结束位置.
注意，如果填充的类型为对象，则是浅拷贝.
对原数组有影响
push
返回数组最新长度
unshift()
返回新数组长度
splice
返回空数组，返回包含删除元素的数组
[2, 3, 4].splice(0, 1); // 0位置删除一个，返回[2]

[2, 3, 4].splice(0, 1, 5); // 0位置删除1个，插入5，原数组是[5, 3, 4]，返回[2]

arrayObject.splice(index,howmany,item1,.....,itemX)
index : 必需。添加/删除项目位置，使用负数可从数组结尾处规定位置。
howmany :必需。要删除项目数量。如果设置为 0，则不会删除项目。
item1, ..., itemX: 可选。向数组添加新项目。
pop()
shift()
对原数组无影响
concat()
创建一个副本，返回新构建的数组
slice()
创建一个包含原有数组中一个或多个元素的新数组
reduce
reduce() 方法不会改变原始数组。
filter
将所有元素进行判断，将满足条件的元素作为一个新的数组返回
some
将所有元素进行判断返回一个布尔值，如果存在元素都满足判断条件，则返回 true，若所有元素都不满足判断条件，则返回 false：
every
将所有元素进行判断返回一个布尔值，如果所有元素都满足判断条件，则返回 true，否则为 false：
求最大值
var a=[1,2,3,4];

Math.max.apply(null, a);
join
纯函数
flat()，flatMap()
将数组扁平化处理，返回一个新数组，对原数据没有影响。
flat()默认只会“拉平”一层，如果想要“拉平”多层的嵌套数组，可以将flat()方法的参数写成一个整数，表示想要拉平的层数，默认为1。
flatMap()方法对原数组的每个成员执行一个函数相当于执行Array.prototype.map()，然后对返回值组成的数组执行flat()方法。该方法返回一个新数组，不改变原数组。
flatMap()方法还可以有第二个参数，用来绑定遍历函数里面的this
数组去重
indexof、includes、filter
function unique(arr) {
    let res = arr.filter(function (item, index, array) {
    
            return array.indexOf(item) === index
        })
        
        return res;
}
Set
let unique=arr=>[...new Set(arr)];

let res=Array.from(new Set(arr));
Map
const unique = (arr) => {

    const map = new Map();
    const res = [];

    for (let item of arr) {

        if (!map.has(item)) {

            map.set(item, true);
            res.push(item);
        }
    }
}
数组和链表
数据的物理存储结构：连续存储（数组）离散存储（链表）
区别：
对数组，查找方便，连续存储，增删改效率低；事先申请好连续的内存空间小，太大浪费内存，太小越界
对链表，动态申请内存空间，不需要像数组需要提前申请好内存的大小，链表只需在用的时候申请就可以，根据需要来动态申请或者删除内存空间，对于数据增加和删除以及插入比数组灵活
应用场景：
数组：适合数据量固定，频繁查询，较少增删的场景
链表：适合数据量不固定，频繁增删，较少查询的场景
数组拍平
ary = ary.flat(Infinity); //Infinity无穷大
toString+replace+split
replace+JSON.parse
递归
function flatten(arr, n) {

    if (n < 2) {
        return arr;
    }

    let res = [];
    const dfs = (arr, n) => {
        if (n < 2) {
            res.push(arr);
            return res;
        }
        for (let item of arr) {
            if (Array.isArray(item) && n) {
                dfs(item, n - 1);
            } else {
                res.push(item);
            }
        }
    }

    dfs(arr, n);

    return res;
}
利用reduce函数迭代
const arr3 = [
    [1, 2],
    [3, 4],
    [5, [7, [9, 10], 8], 6],
];
console.log(flatten(arr3, 2));
function flatten(_arr, depth = 1) {
    if (depth === 0) {
        return _arr;
    }
    return _arr.reduce((pre, cur) =>
        pre.concat(Array.isArray(cur) && depth > 1 ?
            flatten(cur, depth - 1) :
            cur), [])
}
function flatten(_arr, depth = 1) {
    if (depth === 0) {
        return _arr;
    }
    return _arr.reduce((pre, cur) => {
        return Array.isArray(cur) && depth > 1 ?
        [...pre, ...flatten(cur, depth - 1)] :
        [...pre, cur];
    }, [])
}
扩展运算符
while (arr.some(Array.isArray)) {
    arr = [].concat(...arr);
}
toString+split+map
const str = [1, 2, 3, [5, 6, [7, 8]]].toString();
const _arr = str.split(",");
const newArr = _arr.map(item => +item);
console.log(newArr)
ES6新增的数组方法
find找到符合条件的成员
findIndex找到符合条件元素的下标
flat拍平数组
默认拍平一层
带参n表示拍平n层
Infinity作为参数，不管几层，全部拍成一层
数组有空位会跳过
flatMap()
只能拍平一层
对每个元素执行一个函数，再执行flat()
返回新数组，不改变原数组
**Array.at()**返回对应下标的值
**Array.from()**将类似数组的对象转为真的数组
类数组对象需要有length属性，否则返回[]
let arrayLike = {

 '0': 'a',
 '1': 'b',
 '2': 'c',

 length: 3
};

// ES5的写法
var arr1 = [].slice.call(arrayLike); // ['a', 'b', 'c']

// ES6的写法
let arr2 = Array.from(arrayLike); // ['a', 'b', 'c']
**Array.of()**将 一组数值 转为 数组
const a = Array.of(10, 20, 26, 38);

console.log(a); // [10, 20, 26, 38]
Array.includes() 判断数组是否包含某个值，返回boolean类型
... 扩展运算符
rest参数的逆运算
copyWithin()
将指定位置的成员复制到其他位置（会覆盖原有成员），然后返回当前数组。
Array.prototype.copyWithin(target, start = 0, end = this.length)
**fill()**填充数组
**entries()**遍历键值对
**keys()**遍历键名
**values()**遍历键值
**Array.proptype.sort()**的排序稳定性
判断是否存在某个值
array.indexOf() //return 下标或-1
array.find() //返回满足条件的第一个元素的值，若没有，则返回undefined
array.findIndex() //返回满足条件的第一个元素下标，若没有找到，返回-1
String.prototype.includes()
includes() 方法用于判断一个字符串/数组是否包含在另一个字符串中，根据情况返回 true 或 false，方法的第二个参数表示搜索的起始位置，默认为0，参数为负数则表示倒数的位置。
arguments为啥不是数组
另一种对象类型，也叫类对象数组（类数组）
有callee和length属性
如何转换为数组
Array.prototype.slice.call()
function sum(a, b) {
    let args = Array.prototype.slice.call(arguments);
    console.log(args.reduce((sum, cur) => sum + cur)); //args可以调用数组原生的方法啦
}
sum(1, 2); //3
Array.form
对一个类似数组或可迭代对象创建一个新的，浅拷贝的数组实例。
从类数组对象或者可迭代对象中创建一个新的数组实例
function sum(a, b) {

    //Array.from() 方法对一个类似数组或可迭代对象创建一个新的，浅拷贝的数组实例。
    let args = Array.from(arguments);
    console.log(args.reduce((sum, cur) => sum + cur));
}

sum(1, 2);

ES6扩展运算符
function sum(a, b) {

    let args = [...arguments];
    console.log(args.reduce((sum, cur) => sum + cur));
}

sum(1, 2);
concat+apply or apply
function sum(a, b) {

    let args = Array.prototype.concat.apply([], arguments); //apply会把第二个参数展开
    console.log(args.reduce((sum, cur) => sum + cur));
}

function exam(a, b, c, d, e) {

    // 先看看函数的自带属性 arguments 什么是样子的
    console.log(arguments);

    // 使用call/apply将arguments转换为数组, 返回结果为数组，arguments自身不会改变
    var arg = [].slice.call(arguments);

    console.log(arg);
}

exam(2, 8, 9, 10, 3);
// result:
// { '0': 2, '1': 8, '2': 9, '3': 10, '4': 3 }
// [ 2, 8, 9, 10, 3 ]
//
// 也常常使用该方法将DOM中的nodelist转换为数组
// [].slice.call( document.getElementsByTagName('li') );
对象
遍历对象属性
使用 hasOwnProperty 判断对象自身属性中是否具有指定的属性
访问属性点表示和[]
[]语法的主要优点是可以通过变量访问属性。
如果属性包含空格，就不能通过 . 访问它。属性名可以包含非字母非数字，使用[]访问它。
除非必须使用变量访问属性，否则我们使用点表示法。
注意，属性名表达式如果是一个对象，默认情况下会自动将对象转为字符串[object Object]
const keyA = {
    a: 1
};
const keyB = {
    b: 2
};

const myObject = {
    [keyA]: 'valueA',
    [keyB]: 'valueB'
};

myObject // Object {[object Object]: "valueB"}
for...in
循环遍历对象自身的和继承的可枚举属性（不含 Symbol 属性）
Object.keys(obj)
返回一个数组，包括对象**自身的（不含继承的）**所有可枚举属性（不含 Symbol 属性）的键名
Object.getOwnPropertyNames(obj)
返回一个数组，包含对象**自身的所有属性（不含 Symbol 属性，但是包括不可枚举属性）**的键名
Object.getOwnPropertySymbols(obj)
返回一个数组，包含对象自身的所有 Symbol 属性的键名
Reflect.ownKeys(obj)
返回一个数组，包含对象自身的（不含继承的）所有键名，不管键名是 Symbol 或字符串，也不管是否可枚举
遍历对象的方法
for in 以任意顺序 迭代 一个对象的除Symbol以外的可枚举属性，包括继承的可枚举属性。
// Object 原型链上扩展的方法也会被遍历出来
Object.prototype.fun = () => {};
var obj = {
    a: 1,
    b: 2,
    c: 3
};

for (const item in obj) {
    console.log("属性名：" + item + " / 属性值：" + obj[item]);
}

// 属性名：a / 属性值：1
// 属性名：b / 属性值：2
// 属性名：c / 属性值：3
// 属性名：fun / 属性值：() => {}

//而如果我们不希望搜索到原型上的，我们就可以使用 hasOwnProperty
for (const item in obj) {
    if (obj.hasOwnProperty(item)) {
        console.log("属性名：" + item + " / 属性值：" + obj[item]);
    }
}
// 属性名：a / 属性值：1
// 属性名：b / 属性值：2
// 属性名：c / 属性值：3
object.key 返回一个给定对象的自身可枚举 属性名组成的数组，数组中属性名的排列顺序和正常循环遍历该对象时返回的顺序一致 。
// 注意：当属性名为数字的时候会排序，key / values / entries都有这个特性~
const anObj = { 100: 'a', 2: 'b', 7: 'c' };
console.log(Object.keys(anObj)); // console: ['2', '7', '100']

const str = 'hello';
console.log(Object.keys(str));// ["0", "1", "2", "3", "4"]

const arr = ['a', 'b', 'c'];
console.log(Object.key(arr));// ["0", "1", "2"]

var obj = {a:1, b:2, c:3};
console.log(Object.keys(obj));// ["a","b","c"]
Object.values 返回一个给定对象自身的所有可枚举 属性值的数组，值的顺序与使用for…in循环的顺序一致
// 注意：当属性名为数字的时候会排序，key / values / entries都有这个特性~
const obj = {100:1, d:2, a: 9, 1:3, 5: 99 , b: 8};
console.log(Object.values(obj)); //  [3,99,1,2,9,8]

const str = 'hello';
console.log(Object.values(str));// ["h", "e", "l", "l", "o"]

const arr = ['a', 'b', 'c'];
console.log(Object.values(arr));// ["a", "b", "c"]

var obj = {a:1, b:2, c:3};
console.log(Object.values(obj));// ["1","2","3"]
Object.entries 返回一个给定对象自身可枚举属性的 键值对数组，其排列与使用 for…in 循环遍历该对象时返回的顺序一致
// 注意：当属性名为数字的时候会排序，key / values / entries都有这个特性~
const obj = {100:1, d:2, a: 9, 1:3, 5: 99 , b: 8};
console.log(Object.entries(obj)); //   [["1",3],["5",99],["100",1],["d",2],["a",9],["b",8]]

const str = 'hello';
console.log(Object.entries(str));// [["0","h"],["1","e"],["2","l"],["3","l"],["4","o"]]

const obj = {a:1, b:2, c:3};
console.log(Object.entries(obj));// [["a",1],["b",2],["c",3]]

const obj1 = {a:1, b:2, c:3};
for (const [key, value] of Object.entries(obj1)) {    
  console.log(`${key}: ${value}`);
}
//a: 1
// b: 2
// c: 3
Object.getOwnPropertyNames 返回一个由指定对象的所有自身属性的 属性名组成的数组。（包括不可枚举属性但不包括Symbol值作为名称的属性）
// 注意：当属性名为数字的时候会排序，key / values / entries都有这个特性~
const arobj = {100:1, d:2, a: 9, 1:3, 5: 99 , b: 8};
console.log(Object.getOwnPropertyNames(arobj)); //  ["1","5","100","d","a","b"]

const str = 'hello';
console.log(Object.getOwnPropertyNames(str));//  ["0","1","2","3","4","length"]

const arr = ['a', 'b', 'c'];
console.log(Object.getOwnPropertyNames(arr));// ["0","1","2","length"]

const obj = {a:1, b:2, c:3};
console.log(Object.getOwnPropertyNames(obj));// ["a","b","c"]

const syobj = { a:1, b:2 };
const symbol1 = Symbol('symbol1')
const symbol2 = Symbol('symbol2')
syobj[symbol1] = 'hello'
syobj[symbol2] = 'world'
console.log(Object.getOwnPropertyNames(syobj)); //["a","b"]
Object.getOwnPropertySymbols() 方法返回一个给定对象自身的 所有 Symbol 属性的数组
const obj = {a:1, b:2, c:3};
const symbol1 = Symbol('symbol1')
const symbol2 = Symbol('symbol2')
obj[symbol1] = 'hello'
obj[symbol2] = 'world'
console.log(Object.getOwnPropertySymbols(obj));// [Symbol(symbol1), Symbol(symbol2)]
Reflect.ownKeys() 静态方法 Reflect.ownKeys() 返回一个由目标对象自身的 属性名组成的数组
const obj = {a:1, b:2, c:3};
const symbol1 = Symbol('symbol1')
const symbol2 = Symbol('symbol2')
obj[symbol1] = 'hello'
obj[symbol2] = 'world'
console.log(Reflect.ownKeys(obj));// ["a","b","c",Symbol(symbol1), Symbol(symbol2)]
注意
在 ES6 之前 Object 的键值对是无序的；
在 ES6 之后 Object 的键值对按照自然数、非自然数和 Symbol 进行排序，自然数是按照大小升序进行排序，其他两种都是按照插入的时间顺序进行排序。
判断对象是否具有属性
1、in
如果属性来自对象的原型，仍然返回true
let obj = {
    name: 'aa'
};

'name' in obj; //true

'toString' in obj; //true
2、Reflect.has()
检查属性是否在对象中，和in一样作为函数工作
const obj = {
    name: 111
};

Reflect.has(obj, 'name'); //true

Reflect.has(obj, 'toString'); //true
3、hasOwnProperty()
返回布尔值，指对象是否具有指定属性作为它自己的属性(不是继承)
可正确区分对象本身属性和其原型的属性
const obj = {
    a: 1
};

obj.hasOwnProperty('a'); //true

obj.hasOwnProperty('toString'); //false
缺点：如果对象是用Object.create(null)创建的，不能使用这个方法
const obj = Object.create(null);

obj.name = 'merry';

obj.hasOwnProperty('name');

//Uncaught TypeError: obj.hasOwnProperty is not a function
4、Object.prototype.hasOwnProperty()
可解决3的问题，本方法直接调用内置有效函数，跳过原型链
const obj = Object.create(null);

obj.name = 'merry';

Object.prototype.hasOwnProperty.call(obj, 'name'); //true

Object.prototype.hasOwnProperty.call(obj, 'toString'); //false
5、Object.hasOwn()
若对象具有指定属性作为自己的属性，则Object.hasOwn()静态方法返回true，若属性被继承或不存在，返回false
const obj = Object.create(null);

obj.name = 'merry';

Object.hasOwn(obj, 'name'); //true

Object.hasOwn(obj, 'toString'); //false
for in 和 for of 的区别
一句话总结：for ... in是为遍历对象属性而构建的，遍历的是 index，而 for ... of是为了遍历数组的，遍历的是 value
const arobj = {
    100: 1,
    d: 2,
    a: 9,
    1: 3,
    5: 99,
    b: 8
};
Object.prototype.fun = () => {};
arobj.name = "lallala"
    const arr = [1, 2, 4, 8, 9, 10]
    Array.prototype.method = () => {};
arr.name = "bababa";

for (const item in arobj) {
    console.log(arobj[item]) // 3 99 1 2 9 8 lallala () => {}
}
for (const item in arr) {
    console.log(item) //0 1 2 3 4 5 name method fun
}
for (const item of arobj) {
    console.log(item) // Uncaught TypeError: arobj is not iterable
}
for (const item of arr) {
    console.log(item) // 1 2 4 8 9 10
}
一、for … in
for … in 适合遍历对象，遍历数组的时候会出现奇奇怪怪的问题
for … in 遍历会遍历所有的可枚举属性，包括原型链上的，可以使用 hasOwnProperty 来过滤
for … in 中 index 索引为字符串型数字，不能直接进行几何运算
二、for … of
适合比遍历所有拥有迭代器的对象的集合
原型和原型链
实例是类的具象化产品
对象是一个具有多种属性的内容结构
实例都是对象，对象不一定是实例（如Object.prototype是对象但不是实例），构造函数也是对象
prototype是构造函数的属性
__proto__是对象的属性
Object也是Function的实例，那Function是谁的实例呢？
Function.__proto__=== Function.prototype;

//true
Function构造函数的prototype和__proto__属性都指向同一个原型，是否可以说Function对象是由Function构造函数创建的一个实例？
Yes and No.
Yes 的部分： 按照JS中“实例”的定义，a 是 b 的实例即 a instanceof b 为 true，默认判断条件就是 b.prototype 在 a 的原型链上。而 Function instanceof Function 为 true，本质上即 Object.getPrototypeOf(Function) === Function.prototype，正符合此定义。
No 的部分：
Function 是 built-in 的对象，也就是并不存在“Function对象由Function构造函数创建”这样显然会造成鸡生蛋蛋生鸡的问题。实际上，当直接写一个函数时（如 function f() {} 或 x => x），也不存在调用 Function 构造器，只有在你显式调用 Function 构造器时（如 new Function('x', 'return x') ）才有。
注意，本质上，a instanceof b 只是一个运算，即满足某种条件就返回 true/false，当我们说 a 是 b 的实例时，也只是表示他们符合某种关系。JS 是一门强大的动态语言，你甚至可以在运行时改变这种关系，比如修改对象的原型从而改变 instanceof 运算的结果。此外，ES6+ 已允许通过 Symbol.hasInstance 来自定义 instanceof 运算。
Function.prototype//"function"
后来意见：
先有的Object.prototype， Object.prototype构造出Function.prototype，然后Function.prototype构造出Object和Function。
Object.prototype是鸡，Object和Function都是蛋。
prototype
有一个默认的constructor属性,用于记录实例由哪个构造函数创建.
proto
每一个对象都具有的一个属性,叫__proto__,这个属性指向该对象的原型.，原型有两个属性,constructor和proto
既然实例对象和构造函数都可以指向原型,那么原型是否有属性可以指向构造函数或实例吗?
proto与其说是一个属性,不如说是个getter/setter,当使用obj._proto_时,可以理解为返回了Object.getPrototypeOf(obj).
constructor
每一个原型都有一个constructor属性指向关联的构造函数.
function Person()  {}

var person = new Person();

console.log(person.__proto__ == Person.prototype) // true

console.log(Person.prototype.constructor == Person) // true 原型对象的constructor指向构造函数本身

// 顺便学习一个ES5的方法,可以获得对象的原型

console.log(Object.getPrototypeOf(person) === Person.prototype) // true

console.log(Object.getPrototypeOf(person))

person.__proto__

Person.prototype //constructor
实例&原型
当读取实例属性时,若找不到,就会查找与对象关联原型中的属性,若还查不到,就去找原型的原型,一直找到最顶层为止.
原型的原型
实例的proto指向构造函数的prototype
原型链
console.log(Object.prototype.__proto__ === null) // true
意思就是Object.prototype没得原型.
图中由相互关联的原型组成的练状结构就是原型链(蓝色这条线)
创建一个原型链只有name属性的对象
let obj = Object.create(null) //为obj的prototype属性赋值为null

    obj.name = 'merry'

    console.log(obj)
参考文档https://zh.javascript.info/prototype-methods
proto和prototype
prototype是原型对象
__ proto __ 将对象和该对象的原型相连
特殊的 Function 对象，Function 的 proto 指向的是自身的 prototype 。
构造函数 prototype 的 proto 也是指向构造函数的构造函数的 prototype
构造函数是一个函数对象，通过Function构造器产生的。
原型对象本身是一个普通对象，而普通对象的构造函数是Object。
除了Object的原型对象（Object.prototype）的proto指向null，其他内置函数对象的原型对象（例如：Array.prototype）和自定义构造函数的 proto都指向Object.prototype, 因为原型对象本身是普通对象
Object.prototype.__proto__ = null;

Array.prototype.__proto__ = Object.prototype;

Foo.prototype.proto = Object.prototype;
一切对象都是继承自Object对象，Object 对象直接继承根源对象null
一切的函数对象（包括 Object 对象），都是继承自 Function 对象
Object 对象直接继承自 Function 对象
Function对象的__proto__会指向自己的原型对象，最终还是继承自Object对象
原型&原型链
需要new关键字，成为“构造器constructor或构造函数”。
通过prototype定义的属性，再被多个实例化后，引用地址是同一个。
继承链 从祖父——到爷爷——到爸爸——到自己
constructor指向构造函数，每个对象的__proto__指向创建它的构造函数的prototype，而构造函数的prototype也有__proto__指向他的父辈或者是Object，当查找一个对象中不存在的属性时，会去它的__proto__、__proto__中的__proto__中进行寻找，直到找到或者是null为止
instanceof判断对象的__proto__和构造函数的prototype是不是同一个地址
Object.setPrototypeOf改变对象的__proto__
原型(prototype)：一个对象，实现对象的属性继承，简单理解为对象的爹。
prototype可以通过Object.getPrototypeOf() 和 Object.setPrototypeOf() 访问器访问。
当继承的函数被调用时，this 指向的是当前继承的对象，而不是继承的函数所在的原型对象。
不是所有对象都有原型。
继承方式
构造函数会在每一个实例上都创建一遍！
使用原型模式定义的属性和方法由所有实例共享！
原型链
function Parent() {
    this.name = 'kevin';
}

Parent.prototype.getName = function () {
    console.log(this.name);
}

function Child() {}

Child.prototype = new Parent();

var child1 = new Child();

console.log(child1.getName()) // kevin
缺点
引用类型的属性被所有实例共享
创建Child实例时，不能向Parent传参
借用构造函数(经典继承)
function Parent() {
    this.names = ['kevin', 'daisy'];
}

function Child() {
    Parent.call(this);
}

var child1 = new Child();

child1.names.push('yayu');

console.log(child1.names); // ["kevin", "daisy", "yayu"]

var child2 = new Child();

console.log(child2.names); // ["kevin", "daisy"]
避免了 引用类型的属性被所有实例共享
可以在 Child 中向 Parent 传参
缺点
方法都在构造函数中 定义，每次创建实例都会创建一遍方法
组合继承
原型链继承+经典继承 双剑合璧
function Parent(name) {
    this.name = name;

    this.colors = ['red', 'blue', 'green'];
}

Parent.prototype.getName = function () {
    console.log(this.name)
}

function Child(name, age) {
    Parent.call(this, name);

    this.age = age;
}

Child.prototype = new Parent();

Child.prototype.constructor = Child;

var child1 = new Child('kevin', '18');

child1.colors.push('black');

console.log(child1.name); // kevin

console.log(child1.age); // 18

console.log(child1.colors); // ["red", "blue", "green", "black"]

var child2 = new Child('daisy', '20');

console.log(child2.name); // daisy

console.log(child2.age); // 20

console.log(child2.colors); // ["red", "blue", "green"]
融合 原型链 继承和构造函数的优点，JS最常用继承模式
原型式继承
function createObj(o) {
    function F()  {}

    F.prototype = o;

    return new F();
}
ES5 Object.create的模拟实现，将传入对象 作为 创建的对象的原型
包含引用类型的属性值都会共享相应的值——和原型链 继承一样
var person = {
    name: 'kevin',

    friends: ['daisy', 'kelly']
}

var person1 = createObj(person);

var person2 = createObj(person);

person1.name = 'person1';

console.log(person2.name); // kevin

person1.friends.push('taylor');

console.log(person2.friends); // ["daisy", "kelly", "taylor"]
寄生式继承
创建一个仅用于封装继承过程的函数，该函数在内部以某种形式 做增强对象，再返回对象
function createObj(o) {
    var clone = Object.create(o);

    clone.sayName = function () {
        console.log('hi');
    }

    return clone;
}
缺点
和借用构造函数一样，每次创建对象都会创建一遍方法
寄生组合式继承
组合继承 最大缺点——调用2次 父构造方法
设置子实例的原型时
创建子类型的实例时
如何避免重复调用？
如果我们不使用Child.prototype=new Parent()，而是间接让 Child.prototype访问Parent.prototype呢？
function Parent(name) {
    this.name = name;

    this.colors = ['red', 'blue', 'green'];
}

Parent.prototype.getName = function () {
    console.log(this.name)
}

function Child(name, age) {
    Parent.call(this, name);

    this.age = age;
}

// 关键的三步

var F = function ()  {};

F.prototype = Parent.prototype;

Child.prototype = new F();

var child1 = new Child('kevin', '18');

console.log(child1);
封装一下这个继承方法
function object(o) {
    function F()  {}

    F.prototype = o;

    return new F();
}

function prototype(child, parent) {
    var prototype = object(parent.prototype); //创建父类原型对象的副本

    prototype.constructor = child; //增强对象，补充因重写原型而失去的默认的constructor属性

    child.prototype = prototype; //将创建的新副本指定给子类的原型对象
}

// 当我们使用的时候：
prototype(Child, Parent);
优点——引用类型最理想的继承方式
只调用一次Parent 构造函数，避免了在Parent.prototype上面创建不必要的、多余的属性
同时，原型链能保持不变，能正常使用instanceof和isPrototypeOf
instanceof
原理：判断构造函数的prototype属性是否出现在对象的原型链上
优点：instanceof 可以弥补 Object. prototype. toString. call()不能判断自定义实例化对象的缺点
缺点： instanceof 只能用来判断对象类型
console.log(2 instanceof Number); // false
console.log(true instanceof Boolean); // false
console.log('str' instanceof String);// false
console.log([] instanceof Array); // true
console.log(function(){} instanceof Function); // true
console.log({} instanceof Object); //true
实现
// 利用原型链向上查找 能找到这个类的prototype的话，就为true
function myInstanceof(left, right) {

    if (left === null || typeof right !== 'function') {

        return false;
    }
    let proto = Object.getPrototypeOf(left); // 获取对象的原型

    // let proto=left.proto;
    let prototype = right.prototype; // 获取构造函数的 prototype 对象

    // 判断构造函数的 prototype 对象是否在对象的原型链上
    while (true) {

        if (proto === null) {
            return false;
        }

        if (proto === prototype) {
            return true;
        }

        proto = Object.getPrototypeOf(proto);
    }
}

const Person = function () {}

const p1 = new Person()

    console.log(myInstanceof(p1, Person));
typeof&instanceof
typeof 操作符返回一个字符串，表示未经计算的操作数的类型。
instanceof 运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上
区别如下：
typeof会返回一个变量的基本类型，instanceof返回的是一个布尔值
instanceof 可以准确地判断复杂引用数据类型，但是不能正确判断基础数据类型
typeof 虽然可以判断基础数据类型（null 除外），但是引用数据类型中，除了function 类型以外，其他的也无法判断
可以看到，上述两种方法都有弊端，并不能满足所有场景的需求
如果需要通用检测数据类型，可以采用Object.prototype.toString，统一返回格式“[object Xxx]”的字符串
深浅拷贝
浅拷贝只能拷贝一层对象。
深拷贝能解决无限层级对象嵌套问题。
浅拷贝
Object.assign()
拷贝的是对象属性的引用，而不是对象本身。
console.log(Object.assign([1, 2, 3], [4, 5])); //4,5,3
assign方法可以用于处理数组，不过会把数组视为对象，比如这里会把目标数组视为是属性为0、1、2的对象，所以源数组的0、1属性的值覆盖了目标对象的值。
var obj = {

    age: 18,
    nature: ['smart', 'good'],

    names: {
        name1: 'fx',
        name2: 'xka'
    },

    love: function () {
        console.log('fx is a great girl')
    }
}

var newObj = Object.assign({}, obj);
concat浅拷贝数组
slice浅拷贝
...扩展运算符
for...in
深拷贝
1.JSON.parse(JSON.stringify());
无法解决循环利用问题
无法拷贝一条特殊对象 RegExp Date Set Map 等
忽略undefined、symbol和函数
递归实现
lodash第三方库实现
拷贝特殊对象，使用 Object.prototype.toString.call(obj)鉴别。
freeze属性
我们常常用到 freeze 来冻结对象，那么 freeze 属性是如何实现冻结对象，使之不能修改的呢？
一、这里是关于属性的四个基本类型
1、[[Configurable]]: 表示属性是否可以通过 delete 删除并重新定义，是否可以修改它的特性，以及是否可以把它改为访问器属性。默认为 true 。
2、[[Enumerable]]： 表示属性是否可以通过for-in循环返回。默认为 true 。
3、 [[Writable]]： 表示属性的值是否可以被修改。默认为 true 。
4、[[Value]]： 表示属性实际的值。默认为 undefined 。
当我们显式的添加一个属性之后，它的值就会被设置到 [[Value]] 中，而 [[Writable]]表示我们能否读这个值进行修改，如果设置为 false ，那么当我们修改这个值的时候回就会报错，同理其他的属性也是一样的。而如果我们要修改属性的类型的值的时候 ，是使用 Object.defineProperty()方法 来进行修改的。
二、那么 freeze 做了什么？
那么回到我们的前面开篇的问题，当我们使用了 feeeze 的时候，它就会做下面的事情：
设置 Object.preventExtension()，禁止添加新属性 ( 绝对存在 )
设置 Writable 为 false，禁止修改 ( 绝对存在 )
设置 Configurable 为 false，禁止配置 ( 绝对存在 )
禁止更改访问器属性 ( getter 和 setter )
我们有时候会看到有一些属性是用两个中括号包含起来的，这是怎么回事呢？这是因为：当为了将某个特征标识为内部特性，规范会用两个中括号把特性的名称括起来
函数
函数基本知识
函数声明
使用function的函数声明比函数表达式优先提升
变量对象的创建过程中，函数声明比变量声明 有更为优先的执行顺序
无论在什么位置声明了函数，都可以在同一个执行上下文中直接使用
函数表达式
也叫匿名函数
函数表达式使用 var/let/const声明，我们在确认他是否可以正确使用时，必须依照var/let/const的规则 判断，即变量声明
使用var进行变量声明， 进行了两步操作
// 变量声明
var a = 20;

// 实际执行顺序
var a = undefined; // 变量声明，初始值undefined，变量提升，提升顺序次于function声明

a = 20; // 变量赋值，该操作不会提升
同样道理，当我们使用变量声明的方式声明函数时——函数表达式。函数表达的提升方式与变量声明一致
fn(); // 报错

var fn = function () {
    console.log('function');
}

//上述例子执行顺序为

var fn = undefined; // 变量声明提升

fn(); // 执行报错

fn = function () {
    // 赋值操作，此时将后边函数的引用赋值给fn
    console.log('function');
}
因此，由于声明方式的不同，导致 函数声明与函数表达式在使用上的一些差异需要 注意，除此之外，这两种形式的函数在使用上并无不同
匿名函数
没有被显示进行赋值操作的函数。 使用场景——多作为一个参数传入另一个函数中
函数自执行，其实是匿名函数的一种应用
回调函数
匿名函数传入另一个函数之后，最终 在另一个函数中执行，因此我们也常常称这个匿名函数为回调函数
高阶函数
一个函数 接收另一个函数作为参数或返回另一个函数
map
reduce
参数: 两个参数，一个为回调函数，另一个 初始值。回调函数中四个默认参数，依次为积累值、当前值、当前索引和整个数组
filter 返回新数组
sort
普通函数
若是'use strict'，不能将全局对象window作为默认绑定。this=undefined
普通函数：定义时this 指向函数作用域，但定时器之后执行函数时， this指向 window
普通函数的this——调用时所在的对象
函数声明、函数表达式
函数声明式 ： function functionName （）{}
函数表达式：let name = function(){}
console.log(a) //undefined

var a = 1

    console.log(getNum) //getNum(){a=3}

    var getNum = function () {
    a = 2
}
function getNum() {
    a = 3
}
console.log(a) //1

getNum()

console.log(a) //2
函数声明有提升，代码执行前 把函数提升到顶部，执行上下文中生成函数定义，所以第二个 getNum会被最先提升到顶部
然后 var 声明 getNum 的本该提升，但是因为 getNum 的函数已经被声明了，所以就不需要再声明一个同名变量，只是将已经声明的getNum替换掉了，于是修改a=2
console.log(foo) //undefined

console.log(bar) //f(){}

var foo = function () {
    // Some code
};

function bar() {
    // Some code
};
var foo提升至顶部为foo=undefined
// foo bar的定义位置被提升
function bar() {
    // Some code
};

var foo;

console.log(foo) //undefined

console.log(bar)

foo = function () {
    // Some code
};
自执行函数
[IIFE]Immediately Invoked Function Expression：声明即执行的函数表达式
函数传参：按值传递
按值传递，当我们期望传递一个引用类型时**，真正传递的，**只是这个引用类型保存在变量对象中的引用而已
var person = {
    name: 'Nicholas',

    age: 20
}

function setName(obj) { 
    // 传入一个引用
    obj = {}; // 将传入的引用指向另外的值

    obj.name = 'Greg'; // 修改引用的name属性
}

setName(person);

console.log(person.name); // Nicholas 未被改变
函数式编程
将这 多次出现的功能封装
使用时，只需要关心这个方法能做什么，而不用关心具体是怎么实现的。这也是函数式编程思维与命令式不同的地方之一
特征
函数是第一等公民
所谓"第一等公民"（first class），是函数与其他数据类型一样，处于平等地位，可以赋值给其他变量，也可以作为参数，传入另一个函数，或者作为别的函数的返回值
只用"表达式"，不用"语句"
"表达式"（expression）是一个单纯的运算过程，总是有返回值；"语句"（statement）是执行某种操作，没有返回值。函数式编程要求，只使用表达式，不使用语句。每一步都是单纯的运算，都有返回值
函数式编程期望一个函数有输入，也有输出
纯函数
即：只要是同样的参数传入，返回的结果一定是相等的
函数柯里化
是高阶函数的一种特殊用法
柯里化：一个函数(假设叫做createCurry)，接收函数A作为参数，运行后返回一个新的函数。并且这个新的函数能够处理函数A的剩余参数
柯里化函数的运行过程是一个参数的收集过程，我们将每一次传入的参数收集起来，并在最里层里面处理
fn.length 表示fn函数的参数个数
实现函数柯里化
let addCurry = curry1((a, b) => a + b);

console.log(addCurry()(11)(1));

function curry1(fn) {

    let judge = (...args) => {

        if (args.length === fn.length) {

            return fn.call(this, ...args);
        }

        //获取偏函数，返回包装器，重新组装参数并传入
        return (...arg) => judge(...arg, ...args)
    }

    return judge;
}
函数的 length
请问下面这个结果是多少呢
123['toString'].length + 123 = ?
1、形参个数 来看看下面这个例子
function fn1 () {}
function fn2 (name) {}
function fn3 (name, age) {}

console.log(fn1.length) // 0 
console.log(fn2.length) // 1 
console.log(fn3.length) // 2
可以看出，function有多少个形参，length就是多少。但是事实真是这样吗？继续往下看
2、 默认参数 如果有默认参数的话，函数的length会是多少呢？
function fn1 (name) {} 
function fn2 (name = '林三心') {} 
function fn3 (name, age = 22) {} 
function fn4 (name, aaa, age = 22, gender) {} 
function fn5(name = '林三心', age, gender, aaa) {} 

console.log(fn1.length) // 1 
console.log(fn2.length) // 0 
console.log(fn3.length) // 1 
console.log(fn4.length) // 2
console.log(fn5.length) // 0
上面可以看出，function的length，就是第一个具有默认值之前的参数个数
3、 剩余参数 在函数的形参中，还有剩余参数这个东西，那如果具有剩余参数，会是怎么算呢？
function fn1(name, ...args) {} 
console.log(fn1.length) // 1
可以看出，剩余参数是不算进length的计算之中的
4、总结 先公布123[‘toString’].length + 123 = ?的答案是124 length 是函数对象的一个属性值，指该函数有多少个必须要传入的参数，即形参的个数。形参的数量不包括剩余参数个数，仅包括第一个具有默认值之前的参数个数。
箭头函数和普通函数区别
箭头函数的 this 为定义时所在的 this，不绑定this (因为箭头函数没有Constructor)，会捕获其所在上下文的 this 作为自己的 this
若包裹在函数中，就是函数调用时所在的对象，放在全局就是window，箭头函数的this就是外层代码块的this，固定不变。
没有自己的this
继承来的this不会变
没有arguments，实际获得的arguments是外层函数的arguments
call apply 和bind无法改变this指向
不可用于构造函数，没有new关键字
无prototype
不能用于generator函数，没有yield关键字
定义对象的大括号{}不是一个单独的执行环境，它依旧处于全局环境中
构造函数
一、构造函数
在 JavaScript 中，通过 new 来实例化对象的函数叫构造函数，也就是初始化一个实例对象，对象的 prototype 属性是继承一个实例对象。构造函数的命名一般会首字母大写
二、 为什么需要使用构造函数
是为了创建对象
JavaScript 中创建对象有两种，一种是 构建函数 + prototype，另一种是用 class。这里我们不去讲解 class ，先放到构造函数上。
//当我们需要创建比较多信息时
var person1 = { name: 'aa', age: 6, gender: '男', classRoom：'高一'};
var person2 = { name: 'bb', age: 6, gender: '女', classRoom：'高一'};
var person3 = { name: 'cc', age: 6, gender: '女', classRoom：'高一'};
var person4 = { name: 'dd', age: 6, gender: '男', classRoom：'高一'};
那么如果需要创建很多呢？需要这样一个一个的写下去吗？但是实际上可以通过下面的形式来实现。
function Person(name, age, gender, classRoom) {
    this.name = name;
    this.age = age;
    this.gender = gender;
    this.classRoom = '高一'
}

Person.prototype.sayHi = function () {
    console.log("你好，我叫" + this.name + "是一个" + this.sex + "来自" + classRoom);
};

let person1 = new Person("a", 18, '男'); //我们还可以不传 classRoom，让他使用默认的
let person2 = new Person("b", 19, '女');
三、构造函数的执行过程
构造函数的执行过程其实也就是 new 操作符的基本过程
创建一个新的对象，并且在内存中创建一个新的地址。 // let person1 = {}；
继承原型 // person1 .proto = Person.prototype
改变构造函数的 this指向，并且新对象添加构造函数的属性和方法 //执行Person函数，将name,age,sex 参数传入Person中执行，此时函数内部 this 为 new 创建的 person1 对象，所以 person1.name = ‘a’; person1 .age = 18; person1.gender= ‘男’；
根据构建函数返回类型作判断，如果是原始值则被忽略，如果是返回对象，需要正常处理
new 操作符通过构造函数创建的实例，可以访问构造函数的属性和方法，同时实例与构造函数通过原型链连接起来了。
四、构造函数的返回值
构造函数中，不要显式返回任何值：
//返回原始值
function Person(name) {
    this.name = name;
    return '啦啦啦啦'
}
let person1 = new Person("a");
console.log(person1.name) //a

//返回对象

function Person(name) {
    this.name = name;
    return {
        aaa: "asdas"
    }
}
let person1 = new Person("a");
console.log(person1) //{aaa : "asdas"}
console.log(person1.name) //'undefined'
可以看到当返回原始值的时候，并不会正常返回这个原始值 “啦啦啦啦”，而当返回直是对象的时候，这个返回值能被正常返回，但是这时候 new 就不生效了。所以，构造函数尽量不要返回值。因为返回原始值不会生效，返回对象会导致 new 操作符没有作用。
那么为什么会这样呢？
构造函数没有返回值的原因是因为它不是由你的代码直接调用的，它是由运行时的内存分配和对象初始化代码调用的。 它的返回值（如果它在编译为机器代码时实际上有一个）对用户来说是不透明的——因此，你不能指定它。
其实在 JavaScript 中，
let a = [] 也就是 let a = new Array []；
function a () {} 也就是 let a = new Function () {}
执行上下文
当执行 JS 代码时，会产生三种执行上下文
全局执行上下文
函数执行上下文
eval 执行上下文
在该执行上下文的创建阶段，变量对象、作用域链、闭包、this指向会分别被确定。
对于每个执行上下文，都有三个重要属性：
变量对象(Variable object，VO) 包含变量、函数声明和函数的形参，该属性只能在全局上下文中访问
作用域链(Scope chain) JS 采用词法作用域，也就是说变量的作用域是在定义时就决定了
this
全局上下文的变量对象就是全局对象.
JavaScript属于解释型语言，JavaScript的执行分为：解释和执行两个阶段,这两个阶段所做的事并不一样：
解释阶段
词法分析
语法分析
作用域规则确定
执行阶段
创建执行上下文
执行函数代码
垃圾回收
作用域在定义时就确定,而不是在函数调用时确定，不会改变,但是执行上下文是在函数执行前创建的。随时可以改变，执行上下文最明显的就是this的指向在执行时确定. 而作用域访问的变量是编写代码的结构确定的。
同一个作用域下，不同的调用会产生不同的执行上下文环境，继而产生不同的变量的值。
JS引擎创建了执行上下文栈管理执行上下文。
当 JavaScript 开始要解释执行代码的时候，最先遇到的就是全局代码，所以初始化的时候首先就会向执行上下文栈压入一个全局执行上下文，我们用 globalContext 表示它，并且只有当整个应用程序结束的时候，ECStack 才会被清空，所以程序结束之前， ECStack 最底部永远有个 globalContext：
let a = 'Hello World!';

function first() {

	console.log('Inside first function');

    second();

    console.log('Again inside first function');
}

function second() {

	console.log('Inside second function');
}

first();

console.log('Inside Global Execution Context');
简单分析一下流程：
创建全局上下文压入执行栈
first函数被调用，创建函数执行上下文并压入栈
执行first函数过程遇到second函数，再创建一个函数执行上下文并压入栈
second函数执行完毕，对应的函数执行上下文被推出执行栈，执行下一个执行上下文first函数
first函数执行完毕，对应的函数执行上下文被推出栈，然后执行全局上下文
所有代码执行完毕，全局上下文被推出栈，程序结束
作用域
Scope，变量（变量作用域又称为上下文）和函数存在的范围。
作用域:规定了如何查找变量,即确定当前执行代码对变量的访问权限.(决定了代码区块中变量和其他资源的可见性),内层作用域可以访问外层作用域的变量,反之不行.
词法环境其实就是作用域，是一套规则
全局作用域
在代码任何地方都能访问到的对象拥有全局作用域.
一般以下几种情形有全局作用域链:
最外层函数和在最外层函数外面定义的变量拥有全局作用域
所有末定义直接赋值的变量自动声明为拥有全局作用域
所有window对象的属性拥有全局作用域
函数作用域
函数作用域,是指声明在函数内部的变量，和全局作用域相反，局部作用域一般只在固定的代码片段内可访问到，最常见的例如函数内部。
块级作用域(ES6新增)
块级作用域可通过新增命令let和const声明，所声明的变量在指定块的作用域外无法被访问。块级作用域在如下情况被创建：
在一个函数内部
在一个代码块（由一对花括号包裹）内部
特点:
声明变量不会提升到代码块顶部
禁止重复声明
循环中的绑定块作用域的妙用
for循环还有一个特别之处，就是设置循环变量的那部分是一个父作用域，而循环体内部是一个单独的子作用域。
var i = 1

function b() {

	console.log(i)
}

function a() {

	var i = 2

	b()
}

a() // 1
每个函数在执行时都会创建一个执行上下文，其中会关联一个变量对象，也就是它的作用域，上面保存着该函数能访问的所有变量，另外上下文中的代码在执行时还会创建一个作用域链，
如果某个标识符在当前作用域中没有找到，会沿着外层作用域继续查找，直到最顶端的全局作用域，**因为js是词法作用域，在写代码阶段就作用域就已经确定了，换句话说，是在函数定义的时候确定的，而不是执行的时候，**所以b函数是在全局作用域中定义的，虽然在a函数内调用，但是它只能访问到全局的作用域而不能访问到a函数的作用域。
词法作用域
又叫做静态作用域，变量被创建时就确定好了，而不是执行阶段。
作用域链
当查找变量时,会先从当前上下文的变量对象中查找,从当前作用域开始一层层往上找某个变量,如果没有找到，就会从父级(词法层面上的父级执行上下文的变量对象中查找，一直找到全局上下文的变量对象，(多个执行上下文的变量对象构成的链表叫做作用域链)
保证了当前执行环境对符合访问权限的变量和函数的有序访问。
JS采用静态作用域(词法作用域)，因此函数的作用域在函数定义时就确定了.
与其相对的是动态作用域,函数的作用域在函数调用时才决定.
作用域链规定如何查找变量，确定当前执行代码对变量的访问权限。
块语句（大括号“｛｝”中间的语句），如 if 和 switch 条件语句或 for 和 while 循环语句，不像函数，它们不会创建一个新的作用域。
作用域和作用域链
说到作用域链，我们不得不先从作用域开始。首先我们得知道在js中有全局作用域和函数作用域。顾名思义：
作用域就是变量与函数的可访问范围，即作用域控制着变量和函数的可见性和生命周期
全局作用域的变量，函数在整个全局中都能被访问到，它的生命周期和页面的等同
函数作用域的，只能在当前函数内被访问到，生命周期随函数结束而结束销毁。
所以每一个变量或函数都会有自己的作用域范围，而作用域链简单看来说就是:
当前作用域范围（自身内部）中找不到时，就会往他的上一级寻找有没有，直到全局都没有的，返回 undefined。
要小心的是，有些时候，不要相信我们第一眼看到的就以为是他的上一级。如何判断他的上一级需要根据词法作用域来判断。
闭包和内存泄漏
有权访问另外一个函数作用域中变量的函数。
闭包是指那些能够访问自由变量的函数. 自由变量是指在函数中使用的，但既不是函数参数也不是函数的局部变量的变量。 闭包 = 函数 + 函数能够访问的自由变量。
每一个函数都会拷贝上级作用域，形成一个作用域链条。
闭包：自由变量的查找，是在函数定义的地方，向上级作用域查找。不是在执行的地方。
闭包的变量存在堆中，即解释了函数调用之后为什么闭包还能引用到函数内的变量。
闭包的形成需要两个条件：
闭包是在函数被调用执行的时候才被确认创建的。
闭包的形成，与作用域链的访问顺序有直接关系。
只有内部函数访问了上层作用域链中的变量对象时，才会形成闭包，因此，我们可以利用闭包来访问函数内部的变量。
闭包，本质上是上级作用域内变量的生命周期，因为被下级作用域引用，没有得到释放，需要等到下级作用域执行完后才得到释放。
作用
独立作用域，避免变量污染
实现缓存计算结果
库的封装 jQuery
运用
防抖节流
防抖：事件触发高频到最后一次操作，如果规定时间内再次触发，则重新计时。
function debounce(fn, delay = 300) {

    let timer; //闭包引用外界变量

    return function () {

        consr args = arguments;

        if (timer) {
            clearTimeout(timer);
        }

        timer = setTimeout(() => {
                fn.apply(this, args);
            }, delay);
    };
}
模拟块级作用域
function OutPutNum(cnt) {
    
    (function () {

        for (let i = 0; i < cnt; i++) {

            alert(i);
        }
        
    })();
    
    alert(i);
}

对象中创建私有变量
this
new绑定>显示绑定>隐式绑定>默认绑定
this指向在函数被调用时确定，即执行上下文被创建时确定。函数执行过程中，一旦this指向被确定就不可更改。
在一个函数上下文中，this由调用者提供，由调用函数的方式来决定。如果调用者函数，被某一个对象所拥有，那么该函数在调用时，内部的this指向该对象。如果函数独立调用，那么该函数内部的this，则指向undefined。但是在非严格模式中，当this指向undefined时，它会被自动指向全局对象。
// demo03
var a = 20;

var obj = {

    a: 10,

    c: this.a + 20,

    fn: function () {
        return this.a;
    }
}

console.log(obj.c); //40

console.log(obj.fn()); //10
**单独的{}不会形成新的作用域，**因此这里的this.a，由于并没有作用域的限制，它仍然处于全局作用域之中。所以这里的this其实是指向的window对象。
全局上下文
非严格模式和严格模式中this都是指向顶层对象（浏览器中是window，nodejs中是global）。
// 在浏览器中，全局对象为 window 对象：

console.log(this === window); // true

this.a = 37;

console.log(window.a); // 37
函数调用
严格模式下 this 为undefined，非严格模式下为 window
箭头函数
作为方法的箭头函数 this 指向当前被定义变量的上下文环境。
箭头函数的this 为定义时所在的 this，不绑定this (因为箭头函数没有Constructor这个内部槽)，会捕获其所在上下文的 this 作为自己的 this。(箭头函数的this就是它在外面的第一个不是箭头函数的函数的this)**
没有arguments变量
若包裹在函数中，就是函数调用时所在的对象，放在全局就是window，箭头函数的this就是外层代码块的this，固定不变。
ES5 中，永远是 this 指向最后调用它的那个对象
不可用于构造函数，无prototype
无法改变this指向
bind 函数
在 Function的原型链上，Function.prototype.bind.通过 bind 函数绑定后，函数将绑定在其第一个参数对象上，除非使用new时被改变，其他情况不会改变，无论在啥情况下被调用。
setTimeout & setInterval
延时函数内部回调函数this 指向全局对象window。
使用箭头函数使其 this 指向我们所期望的那个对象。
如果this 是 在一个函数中，并且被用作方法来叫，那么这个时候的 this 就指向了父级对象;
如果this 是在匿名函数，或者全局环境的函数中，那么这个时候的 this 就是undefined;
如果this 是在构造函数中，那么这个时候的 this 就指向了即将生成的那个对象
introduction() === introduction.call() ，前者是后者的简写！并且call()中的第一个传参可以指定这个函数中的 this 指向谁！
function introduction(name) {
    console.log('你好,' + name + ' 我是' + this.name);
}

var zhangsan = {
    name: '张三'
}

introduction.call(zhangsan, "李四") // 你好 李四, 我是 张三 call

introduction.apply(zhangsan, ["李四"]) // 你好 李四, 我是 张三 apply

intro = introduction.bind(zhangsan)

    intro("李四") // 你好 李四, 我是 张三 bind
bind()是返回一个绑定新环境的function，等着被调用。
关于 this 的指向问题
每个函数的 this 是在调用时被绑定的，完全取决于函数的调用位置
如何判断 this 的指向呢？有两个关键的点 调用位置 和 绑定规则。
一、调用位置
我们知道执行是在执行栈中的，执行栈是一个栈的结构，遵从先进后出，我们会把执行的任务压入栈中。所以我们这里寻找的调用位置就是当前正在执行的函数的上一个调用的位置。下面看个例子理解：
function a() {
    //当前调用栈是：a，所以当前调用位置是全局
    console.log(“a”)
    b(); // b 的调用位置
}
function b() {
    //当前调用栈是：a->b，所以当前调用位置是a
    console.log(“b”)
    c(); // c 的调用位置
}
function c() {
    //当前调用栈是：a->b->c，所以当前调用位置是b
    console.log(“c”)
}

a()
二、绑定规则
默认绑定：这条规则可以看作是无法应用其他规则时的默认规则，也是我们最常用的。
var a = 2
function foo() {
    var a = 3;
    console.log(this.a)
}
foo() // 2，为什么不是3，那就是因为使用了 this，根据我们上面的调用规则，他是绑定到全局中的
隐式绑定 需要考虑的规则是调用位置是否有上下文对象，当函数拥有上下文对象时，隐式绑定会把this绑定到这个上下文来，并且如果函数调用前存在多个对象，this指向距离调用自己最近的对象。下面我们看例子来理解这段话：
var a = 1;

function foo() {
    var a = 4;
    console.log(this.a)
}

var obj2 = {
    a:2,
    foo:foo
};

var obj1 = {
    a:3,
    obj2: obj2
};

obj2.foo()  // 2 当函数拥有上下文对象时，隐式绑定会把this绑定到这个上下文来
obj1.obj2.foo() //2 如果函数调用前存在多个对象，this指向距离调用自己最近的对象
在隐式绑定中，还会出现一个问题，那就是 隐式丢失，作为 参数传递 以及 变量赋值， 会使参数或者变量直接指向函数，从而丢失 this 指向。
1. 变量赋值
var a = 1;
function foo() {
    var a = 3;
    console.log(this.a)
}
var obj = {
    a:2,
    foo:foo
};
var bar = obj.foo;
bar() // 1 
为什么这里输出的是 1 ，而不是按照上面的规则输出 2 呢？这是因为这里的引用实际只是给函数起了个名字 bar 而已，并没有被调用，在声明 var bar 后才调用 bar () == foo ()， 而此时的 this 指向也就是全局的了。
2. 参数传递
var a = 1;
function foo() {
    var a = 3;
    console.log(this.a)
}
function doFun(fn) {
 fn()
}
var obj = {
    a:2,
    foo:foo
};
doFun(obj.foo;) // 1 
这里其实也是和上面的情况相似的，在 doFun 里面，fu 其实引用的是 foo，所以指向的是全局的
那么如何解决 隐式丢失 呢？
使用 隐式绑定 ：将函数绑定至对象属性，调用时通过对象属性直接调用，弱赋值到其他对象，需将正对象赋值过去，不然会发生丢失（丢失初次绑定的环境）
显式绑定
显示绑定就是指通过 call，apply 以及 bind方法 改变 this 的行为，具体这三个方法看下面就好了~
new 绑定
我们在上面的构造函数中讲到 new 操作符构造函数的过程，可以上去看看~
使用 new 来调用的时候，实际构建一个新的对象并把他绑定到 foo（）调用的 this 上。
function foo(a) {
    this.a = a;
}
var bar = new foo(2);
console.log(bar.a) // 2
箭头函数
箭头函数不会创建自己的 this，所以它没有自己的this，它只会从自己的作用域链的上一层继承 this。
改变this指向的方法（bind / call / apply）
三者都是用来重新定义 this 这个对象的
一、三者的区别：
1、调用上
let name = "www", age = "17";
let obj = {
    name = "aaa";
    objAge = this.age;
    myFun: function () {
        console.log(this.name + "年龄" + this.age)
    }
}

let db = {
    name: "bbb";
    age: 12
}

obj.myFun.call(db)；　　　　	 // bbb年龄 99
obj.myFun.apply(db);		// bbb年龄 99
obj.myFun.bind(db)();		// bbb年龄 99
首先我们可以看出，除了 bind 需要在方法后面添加 “()” 以外，其他的都是直接调用。这是因为 bind()方法创建了一个新的函数，你必须调用显函数才会执行目标函数， 而对于 call 和 apply 是使用后马上执行。
2、参数上
let name = "www", age = "17";
let obj = {
	name = "aaa";
	objAge = this.age;
	myFun: function(fm, t) {
		console.log( this.name + " 年龄" + this.age，"来自" + fm + "去往" + t)
	}
}

let db={
	name: "bbb";
	age: 12
}

obj.myFun.call(db,'成都','上海')；　　　　 // bbb 年龄 99  来自 成都去往上海
obj.myFun.apply(db,['成都','上海']);      // bbb年龄 99  来自 成都去往上海  
obj.myFun.bind(db,'成都','上海')();       // bbb 年龄 99  来自 成都去往上海
obj.myFun.bind(db,['成都','上海'])();　　 // bbb 年龄 99  来自 成都, 上海去往 undefined
可以看出，三个函数的第一个参数都是 this 的指向对象，区别在于第二个参数。
对于 Function.prototype.call 来说，第一个参数就是 this 的指向对象，其余参数是直接放进去，用逗号隔开就好了。
对于 Function.prototype.apply 来说，Function.apply( obj,args ) 方法能接收两个参数，obj：是 this 的指向对象。而 args：这个是数组，它将作为参数传递，也就是说 apply 的所有参数都必须放在一个数组里面传进去
对于 Function.prototype.bind 来说，第一个参数就是 this 的指向对象，其余参数是直接放进去，用逗号隔开就好了。也就是说他和 call 是基本相同的，除了是返回是一个函数。
注意 对于 bind 来说，多次的 bind 调用，this的指向仍然是第一次的 function aa() { console.log(this) } aa.bind(1).bind(2)() // 1
二、bind / call / apply 的异同
相同：都能改变 this 的指向，都是挂载在 Function. prototype 上 不同：call 和 apply 是使用后马上执行，而 bind 是返回一个新的函数，调用显函数才会执行目标函数。并且 call 和 bind 的参数格式是一样的，第一个参数是 this 的指向对象，其余参数用逗号，apply 是参数需要放到数组中。
总结
关于修改 this 的指向的方法有三个， bind 和 call 以及 apply，他们的相同点都是 能修改 this 的指向的问题的，并且都是挂载在 Function.prototype 上的。
不同点在于参数 和执行上，call 和 bind 的参数格式是一样的，第一个参数是 this 的指向对象，其余参数用逗号，而 apply 的参数需要放到数组中。在执行中，call 和 apply 是使用后马上执行，而 bind 是返回一个新的函数，调用显函数才会执行目标函数。
其中需要注意的是，箭头函数的 this 是指向他所在的上下文中，并且是不能使用这三个方法修改的。
字符串
String方法
charAt(index): 返回指定索引处的字符串，若没找着，返回空
charCodeAt(index): 返回指定索引处的字符的 Unicode 值
// toLowerCase()转换成小写 toUpperCase()转换成大写

var x = "a".toLowerCase().charCodeAt(0)

//x = 97
concat(str1, str2, ... ): 连接多个字符串，返回连接后字符串副本，纯函数（和数组一样的用法）
fromCharCode(): 将 Unicode 值转换成实际字符串
String.fromCharCode(97)

// 返回"a"
indexOf(str): 返回 str 在父串中第一次出现的位置，若没有返回-1
lastIndexOf(str): 返回 str 在父串中最后一次出现的位置，若没有返回-1
match(regex): 搜索字符串，返回正则表达式的所有匹配
search(regex): 基于正则表达式搜索字符串，返回第一个匹配的位置
slice(start, end)：返回字符索引在 start 和 end（不含）之间的子串
split(sep，limit)：将字符串分割为字符数组，limit 为从头开始执行分割的最大数量
substr(start，length)：从字符索引 start 的位置开始，返回长度为 length 的子串
substring(from, to)：返回字符索引在 from 和 to（不含）之间的子串，和slice几乎相同，但它允许from>to，不支持负参数
toLowerCase()：将字符串转换为小写
toUpperCase()：将字符串转换为大写
valueOf()：返回原始字符串值
toString() 把Number 对象转换为字符串，返回结果
{} 的 valueOf 结果为 {} ，toString 的结果为 "[object Object]"
[] 的 valueOf 结果为 [] ，toString 的结果为 ""
str.codePointAt(pos)返回pos位置的字符编码
// 不同的字母有不同的代码

alert( "z".codePointAt(0) ); // 122

alert( "Z".codePointAt(0) ); // 90
**String.fromCodePoint(code)**通过code创建字符
alert( String.fromCodePoint(90) ); // Z

//\u后跟十六进制代码，通过代码添加Unicode字符

// 在十六进制系统中 90 为 5a

alert( '\u005a' ); // Z

'a'>'Z'

因为字符通过数字代码比较，a(97)>Z(90)

// 英文是否大写

function upperCase(num) {

var reg = /^[A-Z]+$/;

return reg.test(num);

}
replace
不会修改原字符串！
第二个参数传入要替换的目标字符串，replace只会匹配一次
第二个参数也可传入一个函数，若原始字符串中有n个我们查找的字符串，函数就会执行n次，且函数返回一个字符串，来替换每次匹配到的字符串
参数
$&
$& 适用于没有子表达式的情况
var sStr='讨论一下正则表达式中的replace的用法';

sStr.replace(/正则表达式/,'《$&》');

// 得到："讨论一下《正则表达式》中的replace的用法"
$`
匹配字符串左边的所有字符
var sStr='讨论一下正则表达式中的replace的用法';

sStr.replace(/正则表达式/,'《$`》');

// 得到："讨论一下《讨论一下》中的replace的用法"
$'
匹配字符串右边的所有字符
var sStr='讨论一下正则表达式中的replace的用法';

sStr.replace(/正则表达式/,"《$'》");

// 得到："讨论一下《中的replace的用法》中的replace的用法"
1,2,3,4……n
依次匹配子表达式
var sStr='讨论一下正则表达式中的replace的用法';

sStr.replace(/(正则)(.+?)(式)/,"《$1》$2<$3>");

// 得到："讨论一下《正则》表达<式>中的replace的用法"
函数
var sStr='讨论一下正则表达式中的replace的用法';

sStr.replace(/(正则).+?(式)/,function() {

console.log(arguments);

});

// ["正则表达式", "正则", "式", 4, "讨论一下正则表达式中的replace的用法"]
参数分别为
匹配到的字符串
若正则使用了分组匹配就是多个，否则无此参数
匹配字符串的索引位置
原始字符串
arguments是当前函数的内置属性，指代当前匹配的参数伪数组。
或者使用命名形参的方式：
var sStr='讨论一下正则表达式中的replace的正则表达式用法';

sStr.replace(/(正则).+?(式)/g,function($1) {

console.log($1);

return $1 + 'a';

});
用法
str = str.replace(/\s*/g); //去除字符串内所有的空格 \s匹配任何空白字符。（空格，制表符，换行符）

str = str.replace(/^\s*|\s*$/g, "");//去除字符串内首尾空格

str = str.replace(/^\s*/, "");//去除字符串左侧空格

str = str.replace(/\s*&/, "");//去除字符串右侧空格

name = "Doe, John";

let a=name.replace(/(\w+)\s*, \s*(\w+)/, "$2 $1");

console.log(a)

//John Doe

//首字母大写

let name = 'aaa bbb ccc';

let uw=name.replace(/\b\w+\b/g, function(word){

return word.substring(0,1).toUpperCase()+word.substring(1);}

);
str.trim()
trim()删除字符串两端的空白字符并返回**，不影响原来字符串本身，**返回一个新的字符串
缺陷：只能去除字符串两端的空格，不能去除中间的空格
截取字符串
substring()
substring()用于提取字符串中介于两个指定下标之间的字符
substring(start,stop)
start：一个非负整数，指要提取的子串的第一个字符在字符串中的位置，必需填写
stop：一个非负整数，比要提取的子串的最后一个字符在字符串上的位置多 1，可写可不写，如果不写则返回的子串会一直到字符串的结尾
该字符串的长度为stop-start
如果参数 start 与 stop 相等，则该方法返回的就是一个空串，如果 start 比 stop 大，那么该方法在提取子串之前会先交换这两个参数
substr()
substr()在字符串中抽取从 start 下标开始的指定数目的字符
substr(start,length)
start：要截取的子串的起始下标，必须是数值。如果是负数，那么该参数从字符串的尾部开始算起的位置。也就是说，-1 指字符串中最后一个字符，-2 指倒数第二个字符，以此类推，必需要写
length：子串中的字符数，必须是数值。如果不填该参数，返回字符串的开始位置到结尾的字符。如果length 为0 或者负数，将返回一个空字符串
split()
split() 把一个字符串分割成字符串数组
stringObject.split(separator,howmany)
separator：字符串或正则表达式，从该参数指定的地方分割字符串。必须要填写
howmany：指返回的数组的最大长度。如果设置了该参数，返回的子串不会多于这个参数指定的数组。如果没有设置该参数，整个字符串都会被分割，不考虑它的长度。可选
DOM和事件
事件流
一、什么是事件流：
我们点击一个按键，那么他是如何传递的呢，是从文档顶部一层层传入到这个按键，还是从这个按键传出去呢？
曾经在 IE 就是从里面往外（确定的逐步到不确定的），叫做事件冒泡
而到了 Netscapte 就是从外面往里（不确定的逐步到确定的），叫做事件捕捉
最终在 W3C 的定义规范中，就把两者都包含了~~~（哈哈哈，谁都赢了，但谁也没赢）
所以现在在 DOM事件模型中会分为捕获和冒泡。一个事件发生后，会在子元素和父元素之间传播（propagation）。这种传播分成三个阶段。
捕获阶段：事件从window对象自上而下向目标节点传播的阶段；
目标阶段：真正的目标节点正在处理事件的阶段；
冒泡阶段：事件从目标节点自下而上向window对象传播的阶段。
那么为什么会有事件捕获和事件冒泡呢 这就涉及到事件委托
那么什么是事件委托呢，事件委托就是利用事件冒泡，只指定一个事件处理程序，就可以管理某一类型的所有事件。
事件流描述 从页面接收事件的顺序
事件发生时会在元素节点和根节点之间按照特定的顺序传播，路径所经过的节点都会收到该事件——DOM事件流。
两种事件流模型：
﻿1.捕获：触发元素的事件时，该事件从该元素的祖先元素传递下去 (不太具体的节点应该更早接收到事件，而最具体的节点最后收到事件)
2.冒泡：到达此元素之后，又会向其祖先元素传播上去 DOM标准规定事件流包括3个阶段：事件捕获、处于目标阶段和事件冒泡
事件捕获：实现目标在捕获阶段不会接收事件
处于目标阶：事件在
上发生并处理。但是事件处理会被看成是冒泡阶段的一部分
冒泡阶段：事件又传播回文档
所有事件都要经过捕获阶段和处于目标阶段，但有些事件没有冒泡阶段。
**如focus(获得输入焦点)和失去输入焦点的blur事件。**无法进行委托
事件模型
原始事件模型

var btn = document.getElementById('.btn');
btn.onclick = fun;
绑定速度快
可能页面还未完全加载出来，事件可能无法正常运行
只支持冒泡，不支持捕获
同一个类型的事件只能绑定一次

var btn = document.getElementById('.btn');
btn.onclick = fun2;
//出错 后绑定的事件会覆盖掉之前的事件
删除 DOM0 级事件处理程序只要将对应事件属性置为null即可
btn.onclick = null;
标准事件模型
事件捕获：从document一直向下传播到目标元素, 依次检查经过的节点是否绑定了事件监听函数，如果有则执行
事件处理：到达目标元素, 触发目标元素的监听函数
事件冒泡：从目标元素冒泡到document, 依次检查经过的节点是否绑定了事件监听函数，如果有则执行
事件绑定监听函数的方式如下:
addEventListener(eventType, handler, useCapture)
事件移除监听函数的方式如下:
removeEventListener(eventType, handler, useCapture)
eventType指定事件类型(不要加on)
handler是事件处理函数
useCapture是boolean类型用于指定是否在捕获阶段进行处理，一般设置为false与IE浏览器保持一致
举个例子：
var btn = document.getElementById('.btn');
btn.addEventListener(‘click’, showMessage, false);
btn.removeEventListener(‘click’, showMessage, false);
特性
可以在一个DOM元素上绑定多个事件处理器，不会冲突
btn.addEventListener(‘click’, showMessage1, false);
btn.addEventListener(‘click’, showMessage2, false);
btn.addEventListener(‘click’, showMessage3, false);
第三个参数(useCapture)设置为true就在捕获过程中执行，反之在冒泡过程中执行
IE事件模型
事件处理：事件到达目标元素, 触发目标元素的监听函数。
事件冒泡：事件从目标元素冒泡到document
事件绑定监听函数的方式
attachEvent(eventType, handler)
事件移除监听函数的方式
detachEvent(eventType, handler)
举个例子：
var btn = document.getElementById('.btn');
btn.attachEvent(‘onclick’, showMessage);
btn.detachEvent(‘onclick’, showMessage);
哪些事件支持冒泡
可以通过 event.bubbles 属性可以判断该事件是否可以冒泡
事件	是否冒泡
click	可以
dbclick	可以
keydown	可以
keyup	可以
mousedown	可以
mousemove	可以
mouseout	可以
mouseover	可以
mouseup	可以
scroll	可以
概括来说，鼠标事件，和键盘事件，以及点击事件是支持冒泡的
事件	是否冒泡
blur	不可以
focus	不可以
resize	不可以
about	不可以
mouseenter	不可以
mouseleave	不可以
load	不可以
unload	不可以
而聚焦和失焦事件，加载事件，ui事件、鼠标移入移出事件是不支持的。
阻止冒泡
阻止冒泡行为：非 IE 浏览器 stopPropagation()，IE 浏览器 window. event. cancelBubble = true
阻止默认行为：非 IE 浏览器 preventDefault()，IE 浏览器 window. event. returnValue = false
事件代理
把一个元素响应事件（click、keydown......）的函数委托到另一个元素，在冒泡阶段完成
相对于直接给目标注册事件，有以下优点
节省内存，减少dom操作
不需要给子节点注销事件
动态绑定事件
事件委托，会把一个或者一组元素的事件委托到它的父层或者更外层元素上，真正绑定事件的是外层元素，而不是目标元素。
适合事件委托的事件有：click，mousedown，mouseup，keydown，keyup，keypress
事件委托
添加到页面上事件处理程序数量将直接关联到页面的整体性能
对“事件处理程序过多”问题的解决方案就是事件委托
利用事件冒泡，只指定一个事件处理程序，就可以管理某一类型所有事件
使用事件委托，只需在DOM树中尽量高的一层添加一个事件处理程序
因为事件在冒泡过程中会上传到父节点，并且父节点可以通过事件对象获取到目标节点，因此可以把子节点的监听函数定义在父节点上，由父节点的监听函数统一处理多个子元素的事件
适合用事件委托的事件：click，mousedown，mouseup，keydown，keyup，keypress。
mouseover 和 mouseout 虽然也有事件冒泡，但是因为需要经常计算它们的位置，处理起来不太容易
不适合的就有很多了，举个例子，mousemove，每次都要计算它的位置，不好把控， focus，blur 之类的，本身就没用冒泡的特性，自然就不用事件委托了
为什么要用事件委托
提高性能
新添加的元素还会有之前的事件
HTMLCollection、NodeList
NodeList
NodeList 对象是节点的集合，通常由属性，如Node.childNodes和方法，如 document.querySelectorAll返回
不是数组，是类数组对象
可以使用forEach迭代，使用Array.from()转换为数组
一些情况下，NodeList动态变化，如果文档节点树变化，NodeList会随之而变，Node.childNodes是实时的
其他情况，NodeLIst是静态集合，document.querySelectorAll返回静态NodeList
可使用for循环 或 for-of 遍历，不要使用 for-in 遍历NodeList，因为NodeList对象的length和item属性会被遍历出来，可能导致错误，且for-in无法保证属性顺序
NodeList可包含任何节点类型
HTMLCollection
一个类数组对象，包含元素的通用集合（元素顺序为文档流中顺序）
live——即时更新
因此，最好创建副本后再迭代 以 add 、delete 或是 move节点
getElementByTagName()返回HTMLCollection对象
HTMLCollection有namedITem方法，其他和NodeList保持一致
HTMLCollection只包含元素节点（ElementNode）
Element、Node
Node是基类，Element、Text都继承于它
Element、Text分别叫做ELEMENT_NODE，TEXT_NODE
html上的元素，即element，是类型为ELEMENT_NODE的Node
Node表示DOM树的结构，html中节间可以插入文本，这个插入的空隙就是TEXT_NODE
可使用childNodes得到NodeList，如何获取ElementList？
getElementByXXX返回ElementList，它的真名是 ElementCollection
就像NodeList是Node的集合一样，ElementCollection也是Element的集合
他们都不是真正的数组
dom.onclick 和 dom.addEventListener的区别
一、两者基本信息：
dom.onclick：onclick 事件会在元素被点击时发生，可以在 HTML 和 JavaScript 中使用，所有的浏览器都支持 onclick 事件。
onclick 属性可以使用与所有 HTML 元素，除了：< base > , < bdo >, < br >, < head >, < html >, < iframe >, < meta >, < param >, < script >, < style >, 和 < title >。
dom.addEventListener：document.addEventListener() 方法用于向文档添加事件句柄。具有三个参数，分别是事件，触发执行的函数，以及是否在在捕获或冒泡阶段执行
Internet Explorer 8 及更早IE版本不支持 addEventListener() 方法，Opera 7.0 及 Opera 更早版本也不支持。 但是可以使用 attachEvent() 方法来添加事件句柄
二、三者的区别：
事件监听器（addEventListener / attachEvent）
 < a href = "//google.com" > Try clicking this link. <  / a >

    const element = document.querySelector('a');

element.addEventListener('click', event => event.preventDefault(
        console.log("Hello World"); ));

element.addEventListener('click', event => event.preventDefault(
        console.log("How are you?"); ));

element.click(）
    // "Hello World"
    // "How are you?"
如果不考虑性能等因素，可以添加无限数量的事件到该元素上，并且可以通过 removeEventListener() 移除事件
不能在 HTML 上使用，只能在< script >元素中添加。
有useCapture 参数，你可以选择是在捕获还是在冒泡阶段执行
几乎适合所有浏览器，要是需要适应早期的，可以使用 attachEvent
分离文档结构 (HTML) 和逻辑 (JavaScript)，在大型的项目中开发便于维护
更加好理解，获取元素，添加监听事件，如果发生就触发执行函数。
内联事件监听器
< a href = "//google.com" onclick = "event.preventDefault();" > Try clicking this link. </a>
只能添加一个事件在之上
onclick 可以作为HTML属性添加，也能在< script >元素中添加。
不能在这里使用匿名函数或者闭包
是一个潜在的安全问题，因为它使 XSS 更加有害。如今，网站应该发送适当的Content-Security-PolicyHTTP 标头来阻止内联脚本，并只允许来自受信任域的外部脚本。
不分离文档结构和逻辑。
如果您使用服务器端脚本生成页面，例如您生成一百个链接，每个链接都具有相同的内联事件处理程序，那么您的代码将比事件处理程序仅定义一次时长得多。这意味着客户端必须下载更多内容，结果您的网站会变慢。
不能选择是在捕获还是在冒泡阶段执行
相当于内联 JavaScript
 < a href = "//google.com" > Try clicking this link. <  / a >
    const element = document.querySelector('a');
element.onclick = event => event.preventDefault1();
element.onclick = event => event.preventDefault2(); //会覆盖上面的执行函数
相比上面的方式，基本类似，但因为相当于内联JavaScript，也就是我们是在编写脚本，而不是HTML，就使得我们可以定义实现的更多，也就是可以使用匿名函数、函数引用和/或闭包。但这种方式存在被覆盖的可能性，也就是我们定义的可能被覆盖
三、总结
总的来说没有说那种是最好的，最好的往往是根据实际的情况选择的，但是一般建议使用 addEventListener，因为它可以做任何事情 onclick 能做的，甚至更多。但是可以说 onclick 基本是始终都会有效的，而 当我们addEventListener 需要考虑是否支持。
并且不要使用内联 onclick 来用作 HTML 属性，因为这会混淆 javascript 和 HTML，这是一种不好的做法，它使得代码的可维护性降低。应该说如果没有很好的理由，所有的内联形式都是不建议的。
e.target和e.currentTarget
e.target：触发事件的元素，是点击的元素
e.currentTarget：绑定事件的元素，是途径的元素，执行捕获的顺序
addEventListener和onClick()
addEventListener是为元素绑定事件的方法，接收三个参数：
第一个参数：绑定的事件名
第二个参数：执行的函数
第三个参数：
false：默认，代表冒泡时绑定
true：代表捕获时绑定
onclick和addEventListener事件区别是：onclick事件会被覆盖，而addEventListener可以先后运行不会被覆盖，addEventListener可以监听多个事件
页面生命周期
HTML 页面的生命周期包含三个重要事件：
DOMContentLoaded —— 浏览器已完全加载 HTML，并构建了 DOM 树，但像  和样式表之类的外部资源可能尚未加载完成。
load —— 浏览器不仅加载完成了 HTML，还加载完成了所有外部资源：图片，样式等。
beforeunload/unload —— 当用户正在离开页面时。
每个事件都是有用的：
DOMContentLoaded 事件 —— DOM 已经就绪，因此处理程序可以查找 DOM 节点，并初始化接口。
load 事件 —— 外部资源已加载完成，样式已被应用，图片大小也已知了。
beforeunload 事件 —— 用户正在离开：我们可以检查用户是否保存了更改，并询问他是否真的要离开。
unload 事件 —— 用户几乎已经离开，但是我们仍然可以启动一些操作，例如发送统计数据。
DOMContenLoaded
当浏览器遇到script标签，会在DOM构建之前运行它，因为脚本可能想要修改DOM，对其执行write操作，所以DOMContentLoaded必须等待脚本执行结束。
外部样式表不会影响DOM，因为DOMContenLoaded不会等待他们。
但是，如果在样式后面有一个脚本，那么该脚本必须等待样式表加载完成：
<link type="text/css" rel="stylesheet" href="style.css">

<script>

 // 在样式表加载完成之前，脚本都不会执行

 alert(getComputedStyle(document.body).marginTop);

</script>
原因是，脚本可能想要获取元素的坐标或其他与样式相关的属性，如上例所示。因此，它必须等待样式加载完成。
当 DOMContentLoaded 等待脚本时，它也在等待脚本前面的样式。
不会阻塞 DOMContentLoaded 的脚本
具有 async 特性的脚本不会阻塞 DOMContentLoaded
使用 document.createElement('script') 动态生成并添加到网页的脚本也不会阻塞 DOMContentLoaded。
onload
当整个页面，包括样式、图片和其他资源被加载完成时，会触发 window 对象上的 load 事件。可以通过 onload 属性获取此事件。
onunload
当访问者离开页面时，window 对象上的 unload 事件就会被触发。我们可以在那里做一些不涉及延迟的操作，例如关闭相关的弹出窗口。
onbeforeunload
如果访问者触发了离开页面的导航（navigation）或试图关闭窗口，beforeunload 处理程序将要求进行更多确认。
如果我们要取消事件，浏览器会询问用户是否确定。
readyState
如果我们在文档加载完成之后设置 DOMContentLoaded 事件处理程序，会发生什么？
很自然地，它永远不会运行。
在某些情况下，我们不确定文档是否已经准备就绪。我们希望我们的函数在 DOM 加载完成时执行，无论现在还是以后。
document.readyState 属性可以为我们提供当前加载状态的信息。
有 3 个可能值：
loading —— 文档正在被加载。
interactive —— 文档被全部读取。
complete —— 文档被全部读取，并且所有资源（例如图片等）都已加载完成。
所以，我们可以检查 document.readyState 并设置一个处理程序，或在代码准备就绪时立即执行它。
异步
异步解决方案
同步操作：顺序执行，同一时间只能做一件事情。缺点是会阻塞后面代码的执行。
异步：指的是当前代码的执行作为任务放进任务队列。当程序执行到异步的代码时，会将该异步的代码作为任务放进任务队列，而不是推入主线程的调用栈。等主线程执行完之后，再去任务队列里执行对应的任务。优点是：不会阻塞后续代码的运行。
异步场景
定时任务：setTimeout、setInterval
网络请求：ajax请求、动态创建img标签的加载
事件监听器：addEventListener
回调
回调函数就是我们请求成功后需要执行的函数。
实现了异步，但是带来一个非常严重的问题——回调地狱。
事件发布/订阅
Promise
const promise = new Promise((resolve, reject) => {

        resolve('a');
    });

promise

.then((arg) => {
    console.log(`执行resolve,参数是${arg}`)
})

.catch((arg) => {
    console.log(`执行reject,参数是${arg}`)
})

.finally(() => {
    console.log('结束promise')
});

Promise.reject(2)

//.catch(err=>console.log("err1,",err))
.then(null, err => console.log("err1,", err)) //因为是rejected状态，执行then的第二个callback，改变状态为fulfilled

.then(res => {
    console.log("then1", res)
}, null) //因为是fulfilled，于是执行第一个回调,不会去到下一步catch

//.catch(err=>console.log("err2,",err))

.then(null, err => console.log("err2,", err))
then实现链式操作减低代码复杂度，增强代码可读性。
Promise对象的错误具有“冒泡”性质，会一直向后传递，直到被捕获为止。
每个Promise都会经历的生命周期是：
进行中（pending） - 此时代码执行尚未结束，所以也叫未处理的（unsettled）
已处理（settled） - 异步代码已执行结束 已处理的代码会进入两种状态中的一种：
已完成（fulfilled） - 表明异步代码执行成功，由resolve()触发
已拒绝（rejected）- 遇到错误，异步代码执行失败 ，由reject()触发
方法
Promise.all 传入多个异步请求数组，若all成功，进入fulfilled状态，若一个失败，则立即进入rejected状态。
Promise.allSettled 传入多个异步请求数组，无论失败还是失败，都会进入fulfilled状态。
Promise.race 以一个Promise对象组成的数组作为参数，只要当数组中一个Promsie状态变成resolved或者rejected时，就调用.then方法。
事件循环
Generator
iterator
ES6推出,更方便创建iterator.Generator是一个返回值为iterator对象的函数.
iterator中文名叫迭代器。它为js中各种不同的数据结构(Array、Set、Map)提供统一的访问机制。部署了Iterator接口，就可以完成遍历操作。 因此iterator也是一种对象，不过相比于普通对象来说，它有着专为迭代而设计的接口。
iterator 的作用：
为各种数据结构，提供一个统一的、简便的访问接口；
使得数据结构的成员能够按某种次序排列；
ES6 创造了一种新的遍历命令for…of循环
iterator的结构： 它有next方法，该方法返回一个包含value和done两个属性的对象（我们假设叫result）。value是迭代的值，后者是表明迭代是否完成的标志。true表示迭代完成，false表示没有。iterator内部有指向迭代位置的指针，每次调用next，自动移动指针并返回相应的result。
原生具备iterator接口的数据结构如下：
Array
Map
Set
String
TypedArray
函数里的arguments对象
NodeList对象
这些数据结构都有一个Symbol.iterator属性，可以直接通过这个属性来直接创建一个迭代器。也就是说，Symbol.iterator属性只是一个用来创建迭代器的接口，而不是一个迭代器，因为它不含遍历的部分。 使用Symbol.iterator接口生成iterator迭代器来遍历数组的过程为：
let arr = ['a','b','c'];

let iter = arr[Symbol.iterator]();

iter.next() // { value: 'a', done: false }

iter.next() // { value: 'b', done: false }

iter.next() // { value: 'c', done: false }

iter.next() // { value: undefined, done: true }
for ... of的循环内部实现机制其实就是iterator，它首先调用被遍历集合对象的 Symbol.iterator 方法，该方法返回一个迭代器对象，迭代器对象是可以拥有.next()方法的任何对象，然后，在 for ... of 的每次循环中，都将调用该迭代器对象上的 .next 方法。然后使用for i of打印出来的i也就是调用.next方法后得到的对象上的value属性。
对于原生不具备iterator接口的数据结构，比如Object，我们可以采用自定义的方式来创建一个遍历器。
Generator
function  * createIterator() {

    yield 1;
    yield 2;
    yield 3;
}

// generators可以像正常函数一样被调用，不同的是会返回一个 iterator
let iterator = createIterator();

console.log(iterator.next().value); // 1

console.log(iterator.next().value); // 2

console.log(iterator.next().value); // 3
Generator 函数是一个普通函数，但是有两个特征:
function关键字与函数名之间有一个星号
使用yield语句，定义不同的内部状态
Generator函数的调用方法与普通函数一样，也是在函数名后面加上一对圆括号。不同的是，调用Generator函数后，该函数并不执行，返回的也不是函数运行结果，而是一个指向内部状态的指针对象，也就是遍历器对象（Iterator Object）
function  * generator() {

    yield 1;
}

console.dir(generator);
generator函数的返回值的原型链上确实有iterator对象该有的next，这充分说明了generator的返回值是一个iterator。除此之外还有函数该有的return方法和throw方法。
generator和普通的函数完全不同。当以function*的方式声明了一个Generator生成器时，内部是可以有许多状态的，以yield进行断点间隔。期间我们执行调用这个生成的Generator,他会返回一个遍历器对象，用这个对象上的方法，实现获得一个yield后面输出的结果。
yield和return的区别：
都能返回紧跟在语句后面的那个表达式的值
yield相比于return来说，更像是一个断点。遇到yield，函数暂停执行，下一次再从该位置继续向后执行，而return语句不具备位置记忆的功能。
一个函数里面，只能执行一个return语句，但是可以执行多次yield表达式。
正常函数只能返回一个值，因为只能执行一次return；Generator 函数可以返回一系列的值，因为可以有任意多个yield
语法注意点：
yield表达式只能用在 Generator 函数里面
yield表达式如果用在另一个表达式之中，必须放在圆括号里面
yield表达式用作函数参数或放在赋值表达式的右边，可以不加括号。
使用Generator的其余注意事项：
需要注意的是，yield 不能跨函数。并且yield需要和*配套使用，别处使用无效
function  * createIterator(items) {

    items.forEach(function (item) {

        // 语法错误
        yield item + 1;
    });
}
箭头函数不能用做 generator
那么Generator到底有什么用呢？
因为Generator可以在执行过程中多次返回，所以它看上去就像一个可以记住执行状态的函数，利用这一点，写一个generator就可以实现需要用面向对象才能实现的功能。
Generator还有另一个巨大的好处，就是把异步回调代码变成“同步”代码
async/await
ES7提出的关于异步的终极解决方案
第一个版本说async/await是Generator的语法糖
第二个版本说async/await是Promise的语法糖
关于async/await是Generator的语法糖： 表明的就是aysnc/await实现的就是generator实现的功能。但是async/await比generator要好用。
因为generator执行yield设下的断点采用的方式就是不断的调用iterator方法，这是个手动调用的过程。
针对generator的这个缺点，后面提出来自动执行next，但是仍然麻烦。而async配合await得到的就是断点执行后的结果。
因此async/await比generator使用更普遍。
async函数对 Generator函数的改进：
内置执行器：Generator函数的执行必须靠执行器，因为不能一次性执行完成。但是，async函数和正常的函数一样执行，也不用使用 next方法，会自动执行。
适用性更好：yield命令后面是 Promise对象，但是 async函数的 await关键词后面，可以不受约束。
可读性更好：async和 await，比起使用 *号和 yield，语义更清晰明了。
关于async/await是Promise的语法糖： 如果不使用async/await的话，Promise就需要通过链式调用来依次执行then之后的代码：
而async/await的出现，就使得我们可以通过同步代码来达到异步的效果：
由此可见，Promise搭配async/await的使用才是正解！
async/await其实是基于Promise的.async把promise包装了一下,使用async函数可以让代码简介很多,不需要像promise一样需要写then,不需要写匿名函数处理promise的resolve值,也不需要定义多余的data变量,还避免了嵌套代码。
async函数时Generator函数的语法糖,async函数的返回值是promise对象,generator函数的返回值是 iterator对象方便多了,同时,还可以使用 await 代替then 方法指定下一步操作。
function f() {

    return Promise.resolve('TEST');
}

// asyncF is equivalent to f!
async function asyncF() {

    return 'TEST';
}
await 会阻塞下面的代码（即加入微任务队列），先执行 async外面的同步代码，同步代码执行完，再回到 async 函数中，再执行之前阻塞的代码
定时器原理
var id=setTimeout(fn,delay); 初始化一个只执行一次的定时器，这个定时器会在指定的时间延迟 delay 之后调用函数 fn ,该 setTimeout 函数返回定时器的唯一 id ，我们可以通过这个 id 来取消定时器的执行。
var id=setInvertal(fn,delay); 与 setTimeout 类似，只是它会以 delay 为周期，反复调用函数 fn ，直到我们通过id取消该定时器。
clearInterval(id),clearTimeout(id); 这两个函数接受定时器的 id，并停止对定时器中指定函数的调用。
定时器指定的延迟时间不能得到保证
在浏览器中，因为所有的JS代码都运行在单一线程中，异步事件只有在被触发时，其回调才会得到执行。
因为单线程的缘故，在同一时间只能执行一条 JavaScript 代码，每一个代码块都会阻塞其他异步事件的执行。
这就意味着，当一个异步事件发生的时候（例如鼠标点击，定时器触发，一个 XMLHttpRequest 请求完成），它进入了代码的执行队列，执行线程空闲时会依照该执行队列中顺序依次执行代码。
总结：
JavaScript 引擎是单线程的，会迫使异步事件进入执行队列，等待执行。
setTimeout 和 setInterval 在执行异步代码时从根本上是有所不同的。
如果一个定时器事件被阻塞，使得它不能立即执行，那么它会被延迟，直到下一个可能的时间点，才被执行（这可能比你指定的 delay 时间要长）
Interval 的回调有可能‘背靠背’无间隔的执行，这种情况是说 interval 的回调函数的执行时间比我们指定的 delay 时间还要长
内存管理GC
栈中JS引擎自动清除.
栈内存中变量一般在它的当前执行环境结束就会被销毁被垃圾回收制回收， 而堆内存中的变量则不会，因为不确定其他的地方是不是还有一些对它的引用。 堆内存中的变量只有在所有对它的引用都结束的时候才会被回收。
JS 引擎可以通过逃逸分析辨别出哪些变量需要存储在堆上，哪些需要存储在栈上。
自动垃圾回收机制：找出不使用的值，释放内存。
函数运行结束，没有闭包或引用，局部变量被 标记 清除
全局变量：浏览器卸载页面 被清除
垃圾回收算法
不论哪个垃圾回收算法，都有一套共同的流程：
标记内存空间中的活动对象（在使用中的对象）和非活动对象（可以回收的对象）。
删除非活动对象，释放内存空间。
整理内存空间，避免频繁回收后产生的大量内存碎片（不连续内存空间）。
引用计数
一个对象是否有被引用（循环引用导致内存泄露）
策略:跟踪每个变量被使用的次数
当声明了一个变量且将一个引用类型赋值给该变量时,这个值的引用次数为1
若同一个值又被赋给另一个值,引用数 +1
如果该变量的值被其他的值覆盖了，则引用次数减 1
当这个值的引用次数变为 0 的时候，说明没有变量在使用，这个值没法被访问了，回收空间，垃圾回收器会在运行的时候清理掉引用次数为 0 的值占用的内存
缺点:
需要一个计数器，所占内存空间大，因为我们也不知道被引用数量的上限。
解决不了循环引用导致的无法回收问题。
标记清除
将“不再使用的对象”定义为“无法到达的对象”
工作流程：
垃圾收集器在运行时给内存变量加上 标记,假设内存汇总所有对象都是垃圾,全标记为0
从根部出发，寻找可到达的变量，并将其标记清除,改为1
留有标记的变量就是待删除的,即标记为0,销毁并回收它们占用的内存
把所有内存中对象标记修改为0,等待下一轮垃圾回收
优点:实现简单,一位二进制位就可以为其标记
缺点:
内存碎片化,空闲内存块不连续
分配速度慢,因为即使使用first-fit策略,其操作仍是一个O(n)的操作,最坏情况是每次都要遍历到最后,因为碎片化,大对象的分配速率会更慢﻿
复制算法
为了解决上述问题，复制算法出现了。
将整个空间平均分成 from 和 to 两部分。
先在 from 空间进行内存分配，当空间被占满时，标记活动对象，并将其复制到 to 空间。
复制完成后，将 from 和 to 空间互换。
由于直接将活动对象复制到另一半空间，没有了清除阶段的开销，所以能在较短时间内完成回收操作，并且每次复制的时候，对象都会集中到一起，相当于同时做了整理操作，避免了内存碎片的产生。
优点：吞吐量高、没有碎片
缺点：首先，复制操作需要时间成本的，若堆空间很大且活动对象很多，则每次清理时间会很久；其次，将空间二等分的操作，让可用的内存空间直接减少了一半。
标记整理
也叫做 标记-压缩算法。结合了标记-清除和复制算法的优点。
从一个 GC root 集合出发，标记所有活动对象。
将所有活动对象移到内存的一端，集中到一起。
直接清理掉边界以外的内存，释放连续空间。
该算法既避免了标记-清除法产生内存碎片的问题，又避免了复制算法导致可用内存空间减少的问题。当然，该算法也不是没有缺点的，由于其清除和整理的操作很麻烦，甚至需要对整个堆做多次搜索，故而堆越大，耗时越多。
识别内存泄露
经验法则是，如果连续五次垃圾回收之后，内存占用一次比一次大，就有内存泄漏。
这就要求实时查看内存的占用情况。
在 Chrome 浏览器中，我们可以这样查看内存占用情况
1.打开开发者工具，选择 Performance 面板
2.在顶部勾选 Memory
3.点击左上角的 record 按钮
4.在页面上进行各种操作，模拟用户的使用情况
5.一段时间后，点击对话框的 stop 按钮，面板上就会显示这段时间的内存占用情况
造成内存泄露
意外的全局变量
被遗忘的定时器和回调函数
事件监听没有移除
没有清理的DOM 引用
子元素存在的内存泄漏
闭包
V8对GC优化
栈中数据回收：执行状态指针 ESP 在执行栈中移动，移过某执行上下文，就会被销毁；
堆中数据回收：V8 引擎采用标记-清除算法；
V8 把堆分为两个区域——新生代和老生代，分别使用副、主垃圾回收器；
副垃圾回收器负责新生代垃圾回收，小对象（1 ～ 8M）会被分配到该区域处理；
新生代采用 scavenge 算法处理：将新生代空间分为两半，一半空闲，一半存对象，对对象区域做标记，存活对象复制排列到空闲区域，没有内存碎片，完成后，清理对象区域，角色反转；
新生代区域两次垃圾回收还存活的对象晋升至老生代区域；
主垃圾回收器负责老生区垃圾回收，大对象，存活时间长；
新生代区域采用标记-清除算法回收垃圾：从根元素开始，递归，可到达的元素活动元素，否则是垃圾数据；
为了不造成卡顿，标记过程被切分为一个个子标记，交替进行。
分代式垃圾回收
以上所说的垃圾清理算法每次垃圾回收时都要检查内存中所有的对象,酱紫对一些大,老,存活时间长的对象来说，同新,小,存活时间短的对象一个频率的检查很不好，因为前者需要时间长且不需要频繁进行清理，后者恰恰相反,如何优化?
分代式
分代式机制把一些新、小、存活时间短的对象作为新生代，采用一小块内存频率较高的快速清理，而一些大、老、存活时间长的对象作为老生代，使其很少接受检查，新老生代的回收机制及频率是不同的，可以说此机制的出现很大程度提高了垃圾回收机制的效率
新老生代
V8的GC策略基于分代式垃圾回收机制,将堆内存分为新生代和老生代两区域,采用不同的垃圾回收策略进行垃圾回收.
新生代的对象是存活时间较短的对象,简单来说就是新产生的对象,通常只支持1-8M的容量,而老生代的对象为存活时间较长或常驻内存的对象.
新生代垃圾回收
新生代中对象一般存活时间较短，采用 scavenge 算法处理,在Scavenge算法具体实现中,主要采用一种复制式的方法及Cheney算法：
其将新生代空间对半分为 from-space 和 to-space 两个区域。新创建的对象都被存放到 from-space，当空间快被写满时触发垃圾回收。先对 from-space 中的对象进行标记，完成后将标记对象复制到 to-space 的一端，然后将两个区域角色反转，就完成了回收操作。
由于每次执行清理操作都需要复制对象，而复制对象需要时间成本，所以新生代空间会设置得比较小（1~8M）。
当一个对象经过多次复制后依然存活，它将会被认为是生命周期较长的对象，随后会被移动到老生代中，采用老生代的垃圾回收策略进行管理
另外还有一种情况，如果复制一个对象到空闲区时，空闲区空间占用超过了 25%，那么这个对象会被直接晋升到老生代空间中，设置为 25% 的比例的原因是，当完成 Scavenge 回收后，空闲区将翻转成使用区，继续进行对象内存的分配，若占比过大，将会影响后续内存分配
老生代垃圾回收
老生代中的对象一般存活时间较长且数量也多，使用了两个算法，分别是标记清除算法和标记压缩算法。
什么情况下对象会出现在老生代空间中：
新生代中的对象是否已经经历过一次 Scavenge 算法，如果经历过的话，会将对象从新生代空间移到老生代空间中。
To 空间的对象占比大小超过 25 %。在这种情况下，为了不影响到内存分配，会将对象从新生代空间移到老生代空间中。
首先是标记阶段，从一组根元素开始，递归遍历这组根元素，遍历过程中能到达的元素称为活动对象，没有到达的元素就可以判断为非活动对象
清除阶段老生代垃圾回收器会直接将非活动对象清理掉
前面我们也提过，标记清除算法在清除后会产生大量不连续的内存碎片，过多的碎片会导致大对象无法分配到足够的连续内存，而 V8 中就采用了我们上文中说的标记整理算法来解决这一问题来优化空间
在老生代中，以下情况会先启动标记清除算法：
某一个空间没有分块的时候
空间中被对象超过一定限制
空间不能保证新生代中的对象移动到老生代中
由于JS是单线程运行的，意味着垃圾回收算法和脚本任务在同一线程内运行，在执行垃圾回收时，后续脚本任务需要等垃圾回收完成后才能继续执行。若堆中的数据量非常大，一次完整垃圾回收的时间会非常长，导致应用的性能和响应能力直线下降。为了避免垃圾回收影响应用的性能，V8 将标记的过程拆分成多个子标记，让垃圾回收标记和应用逻辑交替执行，避免脚本任务等待较长时间。
其它
UTF-8、UTF-16 和 Unicode
Unicode是一个字符集，它为每种语言中的每个字符设定了统一并且唯一的二进制编码，以满足跨语言、跨平台进行文本转换、处理的要求。
UTF-8,和UTF-16,是Unicode的实现方式，一个文字的Unicode码长度可以为1，2，4个字节，一个汉字2个字节不够时使用4个字节。
utf16：一个存储单位16bit，也就是2个字节，无符号整数，一个汉字可能占用不同个存储单元 。弊端：A一个字节就可以存储，utf16的话需要字节对齐，也就是2个字节，因此utf-8出现
utf-8：可变长的编码方式，可以用1~4个字节表示一个字符。
优点：节省方案，方便解析为各种类型，根据文字编码范围
base64怎么编码的
Base64就是一种基于64个可打印字符来表示二进制数据的编码方法。
为什么不直接用ASCII码呢？因为我们输入的字符可能有ASCII码中不可见的字符，为了完全可见，就用了base64编码。
中文是多少长度？
conlog.log("你好呀大笨蛋".length)  

// 6
中文在数据库中存放是占两个字符的，但是在浏览器中，由于 javascript 是 unicode 编码的，所有的字符对于它来说一个就是一个，获取的是中文的长度而不是字符的长度，所以上面的输出是 6 。
这就会导致前后端的对于中文的验证长度不一样了，如何解决？
function getRealLength( str ) {
    return str.replace(/[^\x00-\xff]/g, '__').length; //这个把所有双字节的都给匹配进去了
}
JavaScript 中日期时间格式转换
获取当天时间：
//获取当前时间
var date = new Date();
var year = date.getFullYear();
var month = date.getMonth() + 1;
var day = date.getDate();
//这两个是针对小于十的时候，会为个位数
if (month < 10) {
    month = "0" + month;
}
if (day < 10) {
    day = "0" + day;
}
var nowDate = year + "-" + month + "-" + day;

//往往格式成这种样式是后台处理好的，或者我们会使用一些插件，又或者我们在vue中会使用过滤器来处理。
//输出结果格式：2021-11-08
一、基本的函数：
getDate() 返回一个月中的某一天(1-31)
getMonth() 返回月份 (0 ~ 11)
getFullYear() 以四位数字返回年份(2011)
getHours() 返回小时 (0 ~ 23)
getMinutes() 返回分钟 (0 ~ 59)
getSeconds() 返回秒数 (0 ~ 59)
getTime() 返回 1970 年 1 月 1 日至今的毫秒数(1566715528024)
二、获取时间戳的方法
let timestamp =(new Date()).valueOf();
//或者            
let timestamp=new Date().getTime();              
三、练习题
问题：返回 “现在距离 今年元旦 还有 X 天 X 小时 X 分钟 X秒”
function timemove() {
    // 获取当前时间
    let d1 = new Date();
    //获取下一年
    let nextYear = d1.getFullYear() + 1;
    // 定义目标时间
    let d2 = new Date(nextYear + "/1/1 00:00:00");
    // 定义剩余时间
    let d = d2 - d1; // 是一个时间戳
    // 计算剩余天数
    let Day = parseInt(d / 1000 / 60 / 60 / 24);
    // 计算剩余小时
    let Hours = parseInt(d / 1000 / 60 / 60 % 24);
    // 计算剩余分钟
    let Minutes = parseInt(d / 1000 / 60 % 60);
    // 计算剩余秒
    let Seconds = parseInt(d / 1000 % 60);
    //拼接变量
    let time = Day + "天" + Hours + "小时" + Minutes + "分钟" + Seconds + "秒";
    // 将拼接好的变量显示在页面
    console.log("距离元旦还有" + time)
}
input和object实现双向绑定
Object.defineProperty()直接在一个对象上定义一个新的属性,或者修改一个已经存在的属性
Object.defineProperty(obj, props, desc), 其中:
obj: 需要定义属性的当前对象
props: 当前准备定义的属性名
desc: 对定义属性的描述
var Person = {}

var name = null

    Object.defineProperty(Person, 'name', {

        get: function () {
            return name
        },

        set: function (newV) {
            name = newV
        }
    })

    let p = document.getElementById('ppp')
    let ipt = document.getElementById('ipt')

    ipt.addEventListener('input', function (e) {

        Person.name = e.target.value
            p.innerText = Person.name
    })
JSON.stringify()
转换过程中会忽略值为undefined的字段
需要检测一下，若某个字段为undefined，则将其值修改为空字符串
1、若目标对象存在toJSON()方法，它负责定义哪些数据被序列化
let obj = {

    x: 1,
    y: 2,

    toJSON: function () {
        return 'a string create by toJSON'
    }
}

console.log(JSON.stringify(obj));
//'a string create by toJSON'
2、Boolean、Number、String对象被装换为对应原始值
const obj = {

    a: new Number(11),
    b: new String('aaa'),
    c: new Boolean(true)
}

console.log(JSON.stringify(obj));
//{"a":11,"b":"aaa","c":true}
3、undefined、Function和Symbol不是有效的JSON值，要么被忽略(在对象中找着)，要么被更改为null(在数组中找着)
const obj = {

    name: Symbol('aaa'),
    age: undefined,
    isHigh: function () {}
}

console.log(JSON.stringify(obj));
//{}

const arr = [Symbol('aaa'), undefined, function () {}, 'fighting'];

console.log(JSON.stringify(arr));
//[null,null,null,"fighting"]
4、所有Symbol-keyed属性被忽略
const obj = {}

obj[Symbol('a')] = 'aa';

obj[Symbol('b')] = 'bb';

console.log(obj);

console.log(JSON.stringify(obj));

//{Symbol(a): 'aa', Symbol(b): 'bb'}
//{}
5、Date的实例返回一个字符串实现toJSON()方法(和date.toISOString()——使用 ISO 标准返回 Date 对象的字符串格式相同)
JSON.stringify(new Date());

//'"2022-06-16T23:36:38.943Z"'
6、Infinity、NaN和null都被认为是null
const obj = {

    a: Infinity,
    b: NaN,
    c: null,
    val: 20
};

console.log(JSON.stringify(obj));
//{"a":null,"b":null,"c":null,"val":20}
7、所有其他Object实例(包括Map、Weakmap、Set和WeakSet)序列化为其可枚举的属性
let enumObj = {};

//直接在一个对象上定义新的属性或修改现有属性，并返回该对象
Object.defineProperties(enumObj, {

    'name': {
        value: 'a',
        enumerable: true
    },

    'age': {
        value: 99,
        enumerable: false
    },
});

console.log(JSON.stringify(enumObj));
//{"name":"a"}
8、遇到循环抛出TypeError(循环对象值)异常
const obj = {

    a: 'aa'
};

obj.subObj = obj;

console.log(JSON.stringify(obj));
//VM357:5 Uncaught TypeError: Converting circular structure to JSON
9、对BigInt值字符串化时抛出TypeError(BigInt值无法在JSON中序列化)
const obj = {
    a: BigInt(999999999999999999999)
};

console.log(JSON.stringify(obj));
//VM362:4 Uncaught TypeError: Do not know how to serialize a BigInt
escape、encodeURI&encodeURIComponent
escapeURI(已废弃)生成新的由16进制转义序列替换的字符串。字符的 16 进制格式值，当该值小于等于 0xFF 时，用一个 2 位转义序列: %xx 表示。大于的话则使用 4 位序列：%uxxxx 表示。
encodeURIComponent 用一个，两个，三个或四个表示字符的 UTF-8 编码的转义序列来编码 URI
encodeURI 对URI进行编码，将特定字符的每个实例替换为一个、两个、三或四个转义序列
encodeURIComponent和encodeURI异同点
var set1 = ";,/?:@&=+$"; // 保留字符

var set2 = "-_.!~*'()"; // 不转义字符

var set3 = "#";   // 数字标志

var set4 = "ABC abc 123"; // 字母数字字符和空格

console.log(encodeURI(set1)); // ;,/?:@&=+$

console.log(encodeURI(set2)); // -_.!~*'()

console.log(encodeURI(set3)); // #

console.log(encodeURI(set4)); // ABC%20abc%20123 (空格被编码为 %20)

console.log(encodeURIComponent(set1)); // %3B%2C%2F%3F%3A%40%26%3D%2B%24

console.log(encodeURIComponent(set2)); // -_.!~*'()

console.log(encodeURIComponent(set3)); // %23

console.log(encodeURIComponent(set4)); // ABC%20abc%20123
为避免服务器收到不可预知的请求，对用户输入的任何作为URI的部分都应该使用encodeURIComponent转义
移动端点击事件延迟
移动端点击有 300ms 的延迟，因为移动端有双击缩放操作，浏览器在 click 之后要等待 300ms（JS捕获click事件的回调处理），看用户有没有下一次点击，判断这次操作是不是双击
有三种办法解决这个问题：
meta 标签禁用网页的缩放
<meta name="viewport" content="width=device-width user-scalable= 'no'">
更改默认视口宽度
<meta name="viewport" content="width=device-width">
如果能识别网站是响应式的网站，那么移动端浏览器就可以自动禁掉默认的双击缩放行为并去掉300ms的点击延迟
调用 js 库，比如 FastClick
click 延时问题可能引起点击穿透，如在一个元素上注册了 touchStart 的监听事件，这个事件会将这个元素隐藏掉，发现当这个元素隐藏后，触发了这个元素下的一个元素的点击事件
移动端滚动穿透和溢出
滚动穿透
若页面超过一屏高度出现滚动条时，fixed定位的弹窗遮罩层上下滑动，下面的内容也会一起滑动——滚动穿透
1、默认情况，平移（滚动）和缩放手势由浏览器专门处理，但可通过 CSS 特性 touch-action 改变触摸手势的行为
2、
Step 1、监听弹窗最外层元素（popup）的 touchmove 事件并阻止默认行为来禁用所有滚动（包括弹窗内部的滚动元素）
Step 2、释放弹窗内的滚动元素，允许其滚动：同样监听 touchmove 事件，但是阻止该滚动元素的冒泡行为（stopPropagation），使得在滚动的时候最外层元素（popup）无法接收到 touchmove 事件
滚动溢出
弹窗内也含有滚动元素，在滚动元素滚到底部或顶部时，再往下或往上滚动，也会触发页面的滚动，这种现象称之为滚动链（scroll chaining）， 也称为滚动溢出（overscroll）
借用 event.preventDefault 的能力，当组件滚动到底部或顶部时，通过调用 event.preventDefault 阻止所有滚动，从而页面滚动也不会触发了，而在滚动之间则不做处理
JS如何影响DOM树构建
渲染引擎判断是一段脚本时，HTML解析器会暂停DOM的解析，JS引擎介入，因为JS脚本可能修改当前已生成的DOM
如果JS脚本通过文件加载，需要先下载JS代码，而JS文件的下载会阻塞DOM解析，下载非常耗时，受网络、文件大小 等因素的影响
如果脚本是内嵌，则 直接执行
如果JS脚本修改了 DOM中div内容，执行这段脚本后，div内容被修改，HTML解析器恢复解析过程
如果JS代码出现了修改CSS的语句，操纵 CSSOM，执行JS前，先解析JS语句之上所有CSS样式，如果引用了外部CSS文件，执行JS之前，需要等待外部CSS文件下载完成，解析生成CSSOM后，才能执行 JS 脚本
JS引擎解析JS代码前，不知道JS是否操纵了CSSOM，所以渲染引擎遇到JS脚本时，不管该脚本是否操纵了CSSOM，都会执行CSS文件下载，解析，再执行JS脚本，构建DOM，生成布局树
所以JS脚本依赖样式表
JS文件下载会阻塞DOM解析
样式文件会阻塞JS执行
ES6
ES6面试问题
Set集合
Set 对象允许我们存储任何类型的唯一值，无论是原始值或者是对象引用。
let mySet = new Set();

mySet.add(1); // Set [ 1 ]

mySet.add(5); // Set [ 1, 5 ]

mySet.add(5); // Set [ 1, 5 ]

mySet.add("some text"); // Set [ 1, 5, "some text" ]

let o = {a: 1, b: 2};

mySet.add(o);

mySet.add({a: 1, b: 2}); // o 指向的是不同的对象，所以没问题

mySet.has(1); // true

mySet.has(3); // false

mySet.has(5);       // true

mySet.has(Math.sqrt(25)); // true

mySet.has("Some Text".toLowerCase()); // true

mySet.has(o); // true

mySet.size; // 5

mySet.delete(5); // true, 从set中移除5

mySet.has(5);  // false, 5已经被移除

mySet.size; // 4, 刚刚移除一个值

console.log(mySet);

// logs Set(4) [ 1, "some text", {…}, {…} ] in Firefox

// logs Set(4) { 1, "some text", {…}, {…} } in Chrome

mySet.clear()//清楚所有成员，没有返回值
遍历
Set实例遍历的方法有如下：
关于遍历的方法，有如下：
keys()：返回键名的遍历器
values()：返回键值的遍历器
entries()：返回键值对的遍历器
forEach()：使用回调函数遍历每个成员
Set的遍历顺序就是插入顺序
keys方法、values方法、entries方法返回的都是遍历器对象。
实现并集、交集、和差集:
let a = new Set([1, 2, 3]);

let b = new Set([4, 3, 2]);

// 并集

let union = new Set([...a, ...b]);

// Set {1, 2, 3, 4}

// 交集

let intersect = new Set([...a].filter(x => b.has(x)));

// set {2, 3}

// （a 相对于 b 的）差集

let difference = new Set([...a].filter(x => !b.has(x)));

// Set {1}
Map字典
Map 对象存有键值对，其中的键可以是任何数据类型。
Map 对象记得键的原始插入顺序。
Map 对象具有表示映射大小的属性。
map.size // 属性返回 Map 结构的成员总数。

const m = new Map().set('key1', 'val1')

Map.prototype.set(key, value) // 方法设置键名key对应的键值为value，然后返回整个 Map 结构。如果key已经有值，则键值会被更新，否则就新生成该键。

// set方法返回的是当前的Map对象，因此可以采用链式写法。

Map.prototype.get(key) // 读取key对应的键值，如果找不到key，返回undefined。

Map.prototype.has(key) // 返回一个布尔值，表示某个键是否在当前 Map 对象之中

Map.prototype.delete(key) // 删除某个键，返回true。如果删除失败，返回false。

Map.prototype.clear() // 清除所有成员，没有返回值

Map.prototype.keys()：// 返回键名的遍历器。

Map.prototype.values()：// 返回键值的遍历器。

Map.prototype.entries()：// 返回所有成员的遍历器。

Map.prototype.forEach()：// 遍历 Map 的所有成员

forEach // 可以接受第二个参数，用来绑定this。
... 与rest
Rest为解决传入的参数数量不一定；不会为每个变量给一个单独的名称，参数对象包含所有参数传递给函数；arguments不是真正的数组，rest参数是真实的数组
剩余参数只包含那些没有对应形参的实参，arguments包含传给函数的所有实参
... 应用
ES6通过扩展元素符...，好比 rest 参数的逆运算，将一个数组转为用逗号分隔的参数序列
函数调用的时候，将一个数组变为参数序列
将某些数据结构转为数组
合并数组
注意：通过扩展运算符实现的是浅拷贝，修改了引用指向的值，会同步反映到新数组
rest特点
减少代码
//以前函数
function f(a, b) {
    var args = Array.prototype.slice.call(arguments, f.length);
}

// 等效于
function f(a, b, ...args)  {}
rest参数可以被解构
proxy
ES6新增功能，可以用来自定义对象中的操作
代理是一种很有用的抽象机制，能够通过API只公开部分信息，同时还能对数据源进行全面控制
在需要公开API，同时又要避免使用者直接操作底层数据时，可使用代理
比如，实现一个传统的栈数据类型，数组可以作为栈使用，但要保证人们只使用push pop 和length，我们可以基于数组创建一个代理对象，只对外公开这个三个对象成员
Vue3.0中使用Proxy替换原本的Object.defineProperty实现数据响应式
let p = new Proxy(target, handler)
target 表示需要添加代理的对象，handler表示自定义对象中的操作，可以用来自定义set或get函数
使用Proxy实现数据响应式：
let onWatch = (obj, setBind, getLogger) => {
    let handler = {
        get(target, property, receiver) {
            getLogger(target, property)
            return Reflect.get(target, property, receiver)
        },
        set(target, property, value, receiver) {
            setBind(value, property)
            return Reflect.set(target, property, value)
        }
    }
    return new Proxy(obj, handler)
}
let obj = {
    a: 1
}
let p = onWatch(
        obj,
        (v, property) => {
        console.log(`监听到属性${property}改变为${v}`)
    },
        (target, property) => {
        console.log(`'${property}' = ${target[property]}`)
    })
    p.a = 2 // 监听到属性a改变
    p.a // 'a' = 2
自定义set和get函数，在原本逻辑中插入函数逻辑，实现 在对 对象任何属性进行读写时 发出通知
如果 是实现Vue中的响应式，需要在get中收集依赖，在set派发更新，Vue3.0使用Proxy代替原来API的原因在于 Proxy无需一层层递归为每个属性添加代理，一次即可完成以上操作，性能更好，Proxy可以完美监听到任何方式的数据改变，缺陷是 浏览器兼容性 不太好
模块化
特点
解决命名污染，全局污染，变量冲突等
内聚私有，变量不能被外部访问
更好的分离，按需加载
引入其他模块可能存在循环引用问题
代码抽象，封装，复用和管理
避免通过script标签从上至下加载资源
大型项目资源难以维护，特别是多人合作的情况
CommonJS
服务端解决方案。加载速度快(因为模块文件一般存在本地硬盘)
**每个文件是一个模块，**有自己的作用域。在一个文件里面定义的变量、函数、类，都是私有的，对其他文件不可见。
运行时加载，只能在运行时才能确定一些东西
同步加载，只有加载完成后，才能执行后续操作。 因为用于服务端，文件都在本地，同步导入即使卡住主线程影响也不大。
导出时都是值拷贝，就算导出的值变了，导入的值也不会改变，所以如果想更新值，必须重新导入一次。
模块在首次执行后会缓存，再次加载只返回缓存结果，若想再次执行，可清除缓存。
模块加载的顺序就是代码出现的顺序
基本语法
暴露模块：module.exports = value或exports.xxx = value
引入模块：require(xxx),如果是第三方模块，xxx为模块名；如果是自定义模块，xxx为模块文件路径
CommonJS规范规定，每个模块内部，module变量代表当前模块。这个变量是一个对象，它的exports属性（即module.exports）是对外的接口。加载某个模块，其实是加载该模块的module.exports属性。
// 加载模块
var example = require('./example.js');

var config = require('config.js');

var http = require('http');

// 对外暴露模块
module.exports.example = function () {

 ...

}

module.exports = function(x){ 

  console.log(x)
}

exports.xxx=value;
require命令用于加载模块文件。require命令的基本功能是，读入并执行一个JavaScript文件，然后返回该模块的exports对象。如果没有发现指定模块，会报错。
因为nodejs主要用于服务器编程，模块文件一般已经存在本地硬盘，所以加载起来比较快，不用考虑异步加载的方式，所以使用CommonJS规范。
如果是浏览器环境，要从服务器端加载模块，用CommonJS需要等模块下载完并运行后才能使用，将阻塞后面代码的执行，这时就必须采用非同步模式，因此浏览器端一般采用AMD规范，解决异步加载的问题。
AMD
会编译成 require/exports 来执行
浏览器一般使用AMD规范，解决异步加载问题。
RequireJS是一个工具库。主要用于客户端的模块管理。它可以让客户端的代码分成一个个模块，实现异步或动态加载，从而提高代码的性能和可维护性。它的模块管理遵守AMD规范。
Require.js的基本思想是，通过define方法，将代码定义为模块；通过require方法，实现代码的模块加载。
基本语法
定义暴露模块:
//定义没有依赖的模块
define(function(){

	return 模块

})

//定义有依赖的模块
define(['module1', 'module2'], function(m1, m2){

	return 模块

})
引入使用模块:
require(['module1', 'module2'], function(m1, m2){

	使用m1/m2

})
采用异步加载的方式来加载模块，模块的加载不影响后面语句的执行，所有依赖这个模块的语句都定义在一个回调函数里，等到加载完成后再执行回调函数；也可以根据需要动态加载模块
AMD模块定义的方法非常清晰，不会污染全局环境，可清楚地显示依赖关系
CMD
CMD规范专门用于浏览器端，异步加载模块，实用模块时才会加载执行。
整个了CommonJS和AMD规范的特点。
Sea.js中，所有JS模块都遵循CMD模块定义规范。
基本语法
定义暴露模块：
//定义没有依赖的模块
define(function(require, exports, module){
	exports.xxx = value
	module.exports = value
})

//定义有依赖的模块
define(function(require, exports, module){

 	//引入依赖模块(同步)
	var module2 = require('./module2')

    //引入依赖模块(异步)
	require.async('./module3', function (m3) {
 })

 	//暴露模块
 	exports.xxx = value
})
引入使用模块：
define(function (require) {

 	var m1 = require('./module1')
 	var m4 = require('./module4')

 	m1.show()
 	m4.show()
})
ES6
使用 import 和 export 的形式来导入导出模块。这种方案和上面三种方案都不同。
思想是尽量静态化，为了保证在编译时就能确定模块的依赖关系和输入输出的变量。
异步导入，因为用于浏览器，需要下载文件，如果采用同步导入会对渲染有很大影响
采用实时绑定的方式，导入导出的值都指向同一个内存地址，所以导入值会跟随导出值变化
会编译成 require/exports 来执行
使用export命令定义了模块的对外接口以后，其他 JS 文件就可以通过import命令加载这个模块。
一个模块就是一个独立的文件，该文件内部的所有变量，外部无法获取。如果你希望外部能够读取模块内部的某个变量，就必须使用export关键字输出该变量。
在编译阶段，import会提升到整个模块的头部，首先执行。
如果不需要知道变量名或函数就完成加载，就要用到export default命令，为模块指定默认输出。
export default命令用于指定模块的默认输出。显然，一个模块只能有一个默认输出，因此export default命令只能使用一次。所以，import命令后面才不用加大括号，因为只可能唯一对应export default命令。
基本语法
export
1.如果不想对外暴露内部变量的真实名称，可以使用as关键字设置别名，同一个属性可以设置多个别名。
在外部进行引入时，可以通过name2这个变量访问到king值。
const name='king';

export {name as name2};
2.在同一个文件中，同一个变量名只能够export一次，否则会抛出异常。
const name='king';

const _name='king';

export {name as _name};

export {name};//抛出异常，name作为对外输出的变量，只能export一次
import
1.import和export的变量名相同
2.相同变量名的值只能import一次
3.import命令具有提升的效果
//export.js
export const name='king';

//import.js
console.log(name);//king

import {name} from './export.js'
本质：因为import是在编译期间运行的，在执行console语句之前就已经执行了import语句。因此能够打印出 name的值，即，King
4.多次import时，只会加载一次
以下代码汇总，我们import了两次export.js文件，但是最终只输出执行了一次“开始执行”，可以推断出import导入的模块是个单例模式。
//export.js
console.log('start');

export const name='king';

export const age=19;

//import.js
import {name} from './export.js

import {age} from './export.js''
5.允许我们在需要的时候才动态加载模块，而不是一开始就加载所有模块，这样可以帮我们提高性能。
这个新功能允许我们将import()作为函数调用，将其作为参数传递给模块的路径。 它返回一个 promise，它用一个模块对象来实现，可以访问该对象的导出。
import('/modules/myModule.mjs')

.then((module) => {
    // Do something with the module.
});
对比总结
ES6 输出值的引用（对外接口只是一种静态定义，代码解读阶段生成），CommonJS模块输出值的拷贝（加载一个对象，及module.exports属性，该对象只有在脚本运行时才会生成）
ES6模块时动态引用，且不会缓存值，模块中的变量绑定其所在的模块
ES6模块编译时输出接口，CommonJS模块运行时加载
CommonJS规范主要用于服务端编程，同步加载模块，不适合浏览器环境，因为同步意味阻塞，而浏览器资源时异步加载的，因此诞生了AMD 和 CMD
AMD规范在浏览器环境中异步加载模块，且可以并行加载多个模块。但是开发成本高，代码阅读困难，模块定义语义不顺畅
CMD和AMD相似，依赖就近，延迟执行，易在nodejs运行。但是，依赖SPM打包，模块加载逻辑偏重
ES6实现模块功能且实现简单，完全可以取代CommonJS和AMD规范，进而成为浏览器和服务器通用模块解决方案的宠儿。
Ajax、Fetch和Axios
Ajax
Ajax（Asynchronous JavaScript and XML，异步JavaScript与XML技术），使网页实现异步更新，不重新加载网页的情况下，对网页部分进行更新
不是一种新技术，而是2005年被提出的新术语
由XMLHttpRequest的API实现
请求步骤
//创建 XMLHttpRequest 对象
const ajax = new XMLHttpRequest();

//规定请求的类型、URL 以及是否异步处理请求,通过 XMLHttpRequest 对象的 open() 方法与服务端建立连接
ajax.open('GET', url, true);

//发送信息至服务器时内容编码类型
ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

//发送请求
ajax.send(null);

//监听服务端的通信状态，接受服务器响应数据
ajax.onreadystatechange = function () {
    if (ajax.readyState == 4 && (ajax.status == 200 || ajax.status == 304)) {}
};
特点：
局部刷新页面，无需重载整个页面
基于原生XHR开发，而XHR本身架构不清晰
对基于异步的事件不友好
Fetch
fetch 是底层API，代替XHR，是真实存在的，基于 promise 实现
不是Ajax的封装，而是原生JS，没有使用XMLHttpRequest对象
特点：
使用 promise，支持async/await
提供的API丰富
脱离XHR
不携带cookie，需要手动添加配置项
Axios
Axios 是一个基于 promise 封装的HTTP客户端，可以用在浏览器和 node.js 中
它本质也是对原生XMLHttpRequest的封装，只不过它是Promise的实现版本，符合最新的ES规范
特点：
从浏览器中创建 XMLHttpRequests
从 node.js 创建 http 请求
支持 Promise API
拦截请求和响应
转换请求数据和响应数据
取消请求
自动转换 JSON 数据
客户端支持防御 XSRF
axios({

    url: 'xxx', // 设置请求的地址

    method: "GET", // 设置请求方法

    params: { // get请求使用params进行参数凭借,如果是post请求用data
        type: '',
        page: 1
    }
}).then(res => {

    // res为后端返回的数据
    console.log(res);

})
设置接口请求前缀
利用node环境变量判断，区分开发、测试、生产环境
if (process.env.NODE_ENV === 'development') {

    axios.defaults.baseURL = 'http://dev.xxx.com'
} else if (process.env.NODE_ENV === 'production') {

    axios.defaults.baseURL = 'http://prod.xxx.com'
}
本地调试时，在config.js中配置proxy实现代理转发
设置请求头和超时时间
const service = axios.create({
        ...

        timeout: 30000, // 请求 30s 超时

        headers: {
        
            get: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
                // 在开发中，一般还需要单点登录或者其他功能的通用请求头，可以一并配置进来
            },

            post: {
                'Content-Type': 'application/json;charset=utf-8'
                // 在开发中，一般还需要单点登录或者其他功能的通用请求头，可以一并配置进来
            }
        },
    })
封装请求方法
// get 请求
export function httpGet({

    url,
    params = {}

}) {
    return new Promise((resolve, reject) => {

        axios.get(url, {

            params
        }).then((res) => {
        
            resolve(res.data)
        }).catch(err => {
        
            reject(err)
        })
    })
}
请求拦截器
在每个请求里加上token，统一处理维护方便
响应拦截器
在接收到响应后先做一层判断，比如状态码判断登录状态、授权
