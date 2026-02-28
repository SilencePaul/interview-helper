CSS
基础
为什么要初始化CSS样式
消除浏览器之间的差异，提高兼容性
提高代码质量
第一点：
未初始化时，当我们添加进去一个DIV，会发现他并不是紧贴着窗口的，而是有一定的距离的。这就是一个例子，在不同的浏览器中，对一些标签是具有的默认值的，而且不同的浏览器默认值也肯是不一样的。如果没有对其 CSS样式做初始化，就可能导致在不同的浏览器之间展示的效果是不一样的。
第二点：
初始化后，便于我们对代码的统一管理，减少重复样式等。同时修改的时候便于统一管理。
HTML页面中 id 和 class 有什么区别
在css样式表中书写时，id选择符前缀应加"#“，class选择符前缀应加”."
id属性在一个页面中书写时只能使用一次，而class可以反复使用
id作为元素标签用于区分不同结构和内容，而class作为一个样式，可以应用到任何结构和内容当中去
布局上的一般原则：id先确定结构和内容再为它定义样式。而class正好相反，是先定义样式，然后在页面中根据不同需求把样式应用到不同结构和内容上
目前浏览器都允许同一个页面出现多个相同属性值的id，一般情况能正常显示，不过当javascript通过id来控制元素时就会出错
在实际应用中，class常被用到文字版块和页面修饰上，而id多被用在宏伟布局和设计包含块，或包含框的样式。
伪元素和伪类
(:)用于伪类，(::)用于伪元素。
::before以一个子元素存在，定义的一个伪元素，只存在页面中。
伪元素：对选择元素的指定部分进行修改样式，常见的有 :before，:after，:first-line，first-letter 等等
伪类：对选择元素的特殊状态进行修改样式，常见的有 :hover，:active，:checked，:focus，:first-child 等等
单位
px % em 这几个单位，可以适用于大部分项目开发，且拥有较好兼容性
px ： 一个固定像素单位，一个像素表示终端屏幕能显示的最小的区域
% ：元素的宽高可随浏览器的变化而变化，实现响应式，一般子元素的百分比相对于直接父元素
em ： 作为 font-size 的单位时，代表父元素的字体大小按比例计算值，作为其他属性单位时，代表相对自身字体大小按比例计算值
.parent {
font-size:32px;
}
/** child字体为16px **/
.child {
font-size:.5em;
width:2em;
/* 32 * 0.5 * 2 */}}

rem ： CSS3新增。相对于根元素字体大小按比例计算值；作用于根元素字体大小时，相对于其出初始字体大小（16px）
html {
font-size:20px;
}
/* 作用于非根元素，相对于根元素字体大小，所以为40px */
p {
font-size:2rem;
}
vw 相对于视图窗口宽度，视窗宽度为100vw
vh 相对于视图窗口高度，视窗高度为100vh
vm
rpx
rpx是微信小程序独有的，解决屏幕自适应的尺寸单位
responsive pixel（动态像素）
可以根据屏幕宽度进行自适应，无论屏幕大小，规定屏幕宽度为750rpx
通过rpx设置元素和字体大小，可实现小程序在不同尺寸的屏幕上自动适配
rpx和px的换算
iPhone6的屏幕宽度为375px，有750个物理像素，则750rpx=375px=750个物理像素
1px=2rpx
block，inline，inline-block
块级元素：自动占据一行，可以设置宽高
常见的有 div，p，h1-h6，ul，li，form，table
行内元素：占据一行的一小部分，多个行内元素水平排版，无法设置宽高
常见的有 span ，img，a
行内块级元素：跟行内元素类似，不过可以设置宽高
常见的有 button ，img ， input, select, label，textarea
空元素:img,br,input,link,meta
link标签的伪类和用法
<div id="content">

  <h3>

   <a class="a1" href="#">

    a标签伪类link，hover，active，visited，focus区别

   </a>

 </h3>

</div> 

<style>

a.a1:link{  /*链接未被访问时的状态*/

 color: blue;

}

a.a1:visited{ /*链接访问后的状态*/

 color: green; 

}

a.a1:hover{  /*鼠标悬浮的状态*/

 color: red;

}

a.a1:focus{  /*鼠标点击后，刚松开的状态*/

 color: orange; 

}

a.a1:active{  /*点击中的状态，鼠标未松开时*/

 color: yellow;

}

</style>
a:link 未设置超链接则无效
a:visited 针对URL，若两个a标签指向一个链接，点击一个另一个也有visited属性
重排、重绘和合成
回流一定触发重绘，重绘不一定触发回流。重绘开销小，回流代价高。
回流reflow
也叫重排 layout
渲染树中部分或全部元素的尺寸、结构或属性变化，浏览器会重新渲染部分或全部文档
触发回流的操作:
初次渲染
窗口大小改变(resize事件)
元素属性、尺寸、位置、内容改变
元素字体大小变化
添加或者删除可见 dom 元素
激活 CSS 伪类(如 :hover)
查询某些属性或调用某些方法
clientWidth、clientHeight、clientTop、clientLeft
offsetWidth、offsetHeight、offsetTop、offsetLeft
scrollWidth、scrollHeight、scrollTop、scrollLeft
getComputedStyle()
getBoundingClientRect()
scrollTo()
修改样式的时候，**最好避免使用上面列出的属性，他们都会刷新渲染队列。**如果要使用它们，最好将值缓存起来。
重绘 repaint
某些元素的样式如颜色改变，但不影响其在文档流中的位置，浏览器会对元素重新绘制
不再执行布局阶段，直接进入绘制阶段
合成
利用transform、opacity和filter可实现合成效果，即GPU加速
避开布局 分块和绘制阶段
优化
最小化重绘和重排：样式集中改变，使用添加新样式类名
使用 absolute或 fixed使元素脱离文档流(制作复杂动画时对性能有影响)
开启GPU加速。利用css属性transform opacity will-change等，比如改变元素位置，使用translate会比使用绝对定位改变其left或top更高效，因为它不会触发重排或重绘，**transform使浏览器为元素创建一个GPU图层，这使得动画元素在一个独立的层中进行渲染，**当元素内容没有改变就没必要进行渲染。
使用 visibility替换 display: none ，因为前者只会引起重绘，后者会引发回流（改变了布局）
DOM 离线后修改，如：先把 DOM 设为display:none(有一次 Reflow)，然后修改再显示，只会触发一次回流
不要把 DOM 结点属性值放在一个循环当成循环里的变量
不要使用 table 布局，可能很小的一个小改动会造成整个 table 重新布局
动画实现速度的选择，动画速度越快，回流次数越多，也可以选择使用 requestAnimationFrame
CSS 选择符从右往左匹配查找，避免节点层级过多
频繁运行的动画变为图层，图层能够阻止该节点回流影响别的元素。比如对于 video 标签，浏览器会自动将该节点变为图层
通过documentFragment创建一个DOM文档片段，在它上面批量操作DOM，完成后再添加到文档中，只触发一次回流
documentFragment不是真实DOM的一部分，它的变化不会触发DOM树的重新渲染，不会导致性能问题
效果不甚明显，因为现代浏览器会使用队列存储储存多次修改进行优化
盒子模型
1、盒模型宽度的计算
（1）普通盒模型
默认盒子属性：box-sizing: content-box;
width只包含内容宽度，不包含border和padding
offsetWidth = (width + padding + border)，不算 margin
width 和 height 属性只会应用到这个元素的内容区

box-sizing: content-box;//定义引擎如何计算元素的总高度和总宽度
content-box 默认值，元素的 width/height 不包含padding，border，与标准盒子模型表现一致
border-box 元素的 width/height 包含 padding，border，与怪异盒子模型表现一致
inherit 指定 box-sizing 属性的值，应该从父元素继承
（2）怪异盒模型
设置语句：box-sizing: border-box;
offsetWidth = width（padding 和 border 都挤压到内容里面）
width 和 height 包括内容区、padding 和 border，不算 margin

2、margin 纵向重叠
margin 纵向重叠取重叠区最大值，不进行叠加

3、margin 负值问题
margin-top 和 margin-left 是负值，元素会向上或者向左移动
margin-right 负值，右侧元素左移，自身不受影响
margin-bottom 负值，下侧元素上移，自身不受影响
4、BFC
Block Format Context：块级格式化上下文
一块独立的渲染区域，内部元素的渲染不会影响边界以外的元素
形成 BFC 的条件：
float 不设置成 none
position 是 absolute 或者 fixed
overflow 不是 visible
display 是 flex 或者 inline-block 等
应用：清除浮动
5、float
（1）圣杯布局和双飞翼布局
作用：
实现 pc 端三栏布局，中间一栏最先渲染
实现两边宽度固定，中间自适应
效果图：

（2）圣杯布局
HTML：
<div class="container clearfix">
    <div class="main float"></div>
    <div class="left float"></div>
    <div class="right float"></div>
</div>
CSS：
.container {
    padding: 0 200px;
    background-color: #eee;
}

/* 清除浮动 */
.clearfix::after {
    content: '';
    display: table;
    clear: both;
}

/* 关键 */
.float {
    float: left;
}

.main {
    width: 100%;
    height: 200px;
    background-color: #ccc;
}

.left {
    width: 200px;
    height: 200px;
    /* ---关键--- */
    position: relative;
    right: 200px;
    margin-left: -100%;
    /* ---关键--- */
    background-color: orange;
}

.right {
    width: 200px;
    height: 200px;
    /* ---关键--- */
    margin-right: -200px;
    /* ---关键--- */
    background-color: skyblue;
}
（3）双飞翼布局
HTML：
<div class="float wrapper">
    <div class="main"></div>
</div>
<div class="left float"></div>
<div class="right float"></div>
CSS：
/* 关键 */
.float {
    float: left;
}

.wrapper {
    width: 100%;
    height: 200px;
    background-color: #ccc;
}

/* 关键 */
.wrapper .main {
    height: 200px;
    margin-left: 200px;
    margin-right: 200px;
}

.left {
    width: 200px;
    height: 200px;
    /* 关键 */
    margin-left: -100%;
    background-color: orange;
}

.right {
    width: 200px;
    height: 200px;
    /* 关键 */
    margin-left: -200px;
    background-color: skyblue;
}
（4）对比
属性	圣杯布局	双飞翼布局
HTML	包裹三栏	只包裹中间一栏
是否定位	相对定位	无需定位
左右栏的空间	使用 padding 预留	使用 margin 预留
左栏处理	positon + margin-left	margin-left
右栏处理	margin-right	margin-left
（5）手写clearfix
CSS：
/* 1、父级标签定义伪类 */
.clearfix::after {
    content: '';
    display: table;
    clear: both;
}
/* 兼容IE低版本 */
.clearfix {
    *zoom: 1;
}

/* 2、父级标签 overflow */
.clearfix {
    overflow: hidden;
}

/* 3、添加空 div 标签 */
.clearfix {
    clear: both;
}
6、元素居中
（1）行内元素水平垂直居中
设置父级标签。
水平居中： text-align: center
垂直居中： line-height：盒子高度
（2）块级元素水平垂直居中
水平居中:
margin : 0 auto;  
水平垂直都居中
position: absolute;    
top: 50%;  
left: 50%;  
transform: translate(-50%，-50%)   
不会触发重排，因此最常用
position: absolute;   
top: 0;   
left: 0;   
right: 0;   
bottom: 0;   
margin: auto;  
容器设置：
display：flex;   
justify-content: center;   
align-items: center;    
容器：
display: table-cell;   
text-align: center;   
vertical-align: middle;   
子元素：
display: inline-block;
7、样式单位
em：相对于自身字体大小的单位
rem：相对于 html 标签字体大小的单位
vh：相对于视口高度大小的单位，20vh == 视口高度/10020
vw：相对于视口宽度大小的单位, 20vw == 视口宽度/10020
margin 合并
margin 合并也叫外边框塌陷或者外边距重叠，注意不同于高度塌陷。
外边距重叠：块的上外边距(margin-top)和下外边距(margin-bottom)有时合并(折叠)为单个边距，其大小为单个边距的最大值(或如果它们相等，则仅为其中一个)，这种行为称为边距折叠。
1、同一层相邻元素之间
<p>1 </p>
<p>2 </p>
<style>
p:nth-child(1){
  margin-bottom: 13px;
}
p:nth-child(2){
  margin-top: 12px;
}
</style>
这里我们希望的是这两个之间的距离是 25px，但是实际上他们的距离是13px
2、没有内容将父元素和后代元素分开
<style type="text/css">
    section    {
        margin-top: 13px;
        margin-bottom: 87px;
    }

    header {
        margin-top: 87px;
    }

    footer {
        margin-bottom: 13px;
    }
</style>

<section>
    <header>上边界重叠 87</header>
    <main></main>
    <footer>下边界重叠 87 不能再高了</footer>
</section>
3、空的块级元素
<style>
p {
  margin: 0;
}
div {
  margin-top: 13px;
  margin-bottom: 87px;
}
</style>

<p>上边界范围是 87 ...</p>
<div></div>
<p>... 上边界范围是 87</p>
margin和padding 的值为百分比时
当 padding 属性值为百分比的时候，如果父元素有宽度，相对于父元素宽度，如果没有，找其父辈元素的宽度，均没设宽度时，相对于屏幕的宽度。
不管 margin-top/margin-bottom 还是 margin-left/margin-right（对于padding 同样）也是，参考的都是 width。
那么为什么是 width， 而不是 height 呢？
CSS权威指南中的解释：
我们认为，正常流中的大多数元素都会足够高以包含其后代元素（包括外边距），如果一个元素的上下外边距时父元素的 height 的百分数，就可能导致一个无限循环，父元素的 height 会增加，以适应后代元素上下外边距的增加，而相应的，上下外边距因为父元素 height 的增加也会增加，如此循环。
BFC
块格式化上下文（Block Formatting Context，BFC） 是Web页面的可视CSS渲染的一部分，是块盒子的布局过程发生的区域，也是浮动元素与其他元素交互的区域。
BFC是一个独立的布局环境，与外部互不影响，用于决定块级盒的布局及浮动相互影响范围的一个区域。
块盒和行盒(行盒由一行中所有的内联元素所组成)都会垂直沿着其父元素的边框排列。
除了 BFC，还有：
IFC（行级格式化上下文）- inline 内联
GFC（网格布局格式化上下文）- display: grid
FFC（自适应格式化上下文）- display: flex或display: inline-flex
注意：同一个元素不能同时存在于两个 BFC 中。
创建
根元素
float 值为 left 、right
display 值为 inline-block、table-cell、table-caption、table、inline-table、flex、inline-flex、grid、inline-grid
绝对定位元素：position 值为 absolute、fixed
overflow 值不为 visible，即为 auto、scroll、hidden
特点
是页面上的一个独立容器,容器里面的子元素不会影响外面的元素
垂直方向上，自上而下，与文档流排列方式一致
同一 BFC 下的相邻块级元素可能发生margin折叠，创建新的 BFC 可以避免外边距折叠
BFC区域不会与浮动容器发生重叠
两栏布局
float + overflow:hidden
计算BFC高度时，浮动元素参与计算
每个元素的左margin和容器的左border相接触,即,每个元素的外边距盒（margin box）的左边与包含块边框盒（border box）的左边相接触（从右向左的格式的话，则相反），即使存在浮动
应用
解决margin重叠问题
块级元素的上外边距和下外边距有时会合并（或折叠）为一个外边距，其大小取其中的较大者，这种行为称为外边距折叠（重叠），注意这个是发生在属于同一 BFC 下的块级元素之间
把两个元素变成两个BFC
自适应两栏布局
左列浮动。右列设置 overflow: hidden; 触发BFC , float + overflow:hidden
父子元素的外边距重叠
如果在父元素与其第一个/最后一个子元素之间不存在边框、内边距、行内内容，也没有创建块格式化上下文、或者清除浮动将两者的外边距 分开，此时子元素的外边距会“溢出”到父元素的外面。
解决
父元素触发BFC
父元素添加border
父元素添加padding
清除浮动，解决父元素高度塌陷
当容器内子元素设置浮动时，脱离了文档流，容器中总父元素高度只有边框部分高度。
浮动
浮动元素不在文档流中，所以文档流的块框表现得像浮动框不存在
块级元素认为浮动元素不存在，浮动元素会影响行内元素的布局，浮动元素通过行内元素间接影响包含块的布局
浮动元素摆放遵循规则：
尽量靠上
尽量靠左
尽量一个挨一个
可能超出包含块
不能超过所在行的最高点
行内元素绕着浮动元素摆放
带来的问题
父元素的高度无法被撑开
与浮动元素同级的非浮动元素会紧随其后
清除浮动
父级div定义height
最后一个浮动元素加空div标签，添加样式clear:both（不推荐）
父级div定义zoom
父级添加overflow：hidden/auto（不推荐）
浮动元素的容器添加浮动（不推荐，会使整体浮动，影响布局）
after伪元素清除浮动，尾部添加一个看不见的块元素清理浮动，设置clear:both（推荐）
before和after双伪元素清除浮动
总结 3 种
1、clear属性
2、BFC
3、::after伪元素
定位
relative：相对自身之前正常文档流中的位置发生偏移，与世隔绝，且原来的位置仍然被占据。发生偏移时，可能覆盖其他元素。body默认是relative,子绝父相。
absolute：元素框不再占有文档位置，并且相对于包含块进行偏移（所谓包含块就是最近一级外层元素position不为static的元素）。
fixed：元素框不再占有文档流位置，并且相对于视窗进行定位。
static：默认值，取消继承。
sticky：css3新增属性值，粘性定位，相当于relative和fixed的混合。最初会被当作是relative，相对原来位置进行偏移；一旦超过一定的阈值，会被当成fixed定位，相对于视口定位。
inherit
文档流
定位流
元素的属性 position 为 absolute 或 fixed，它就是一个绝对定位元素。
在绝对定位布局中，元素会整体脱离普通流，因此绝对定位元素不会对其兄弟元素造成影响，而元素具体的位置由绝对定位的坐标决定。
它的定位相对于它的包含块，相关CSS属性：top、bottom、left、right；
对于 position: absolute，元素定位将相对于上级元素中最近的一个relative、fixed、absolute，如果没有则相对于body；
对于 position:fixed，正常来说是相对于浏览器窗口定位的，但是当元素祖先的 transform 属性非 none 时，会相对于该祖先进行定位。
浮动流
在浮动布局中，元素首先按照普通流的位置出现，然后根据浮动的方向尽可能地向左边或右边偏移，其效果与印刷排版中的文本环绕相似。
普通流
普通流其实就是指BFC中的FC。FC(Formatting Context)，直译过来是格式化上下文，它是页面中的一块渲染区域，有一套渲染规则，决定了其子元素如何布局，以及和其他元素之间的关系和作用。
在普通流中，元素按照其在 HTML 中的先后位置至上而下布局，在这个过程中，行内元素水平排列，直到当行被占满然后换行。块级元素则会被渲染为完整的一个新行。
除非另外指定，否则所有元素默认都是普通流定位，也可以说，普通流中元素的位置由该元素在 HTML 文档中的位置决定。
CSS选择器
CSS选择器
选择器	例子	例子描述
.class	.intro	选择 class=“intro” 的所有元素。
.class1.class2	.name1.name2	选择 class 属性中同时有 name1 和 name2 的所有元素。
.class1 .class2	.name1 .name2	选择作为类名 name1 元素后代的所有类名 name2 元素。
#id	#firstname	选择 id=“firstname” 的元素。
*	*	选择所有元素。
element	p	选择所有 元素。
element.class	p.intro	选择 class=“intro” 的所有 元素。
element,element	div, p	选择所有 元素和所有 元素。
element element	div p	选择 元素内的所有 元素。
element>element	div > p	选择父元素是 的所有 元素。
element+element	div + p	选择紧跟 元素的首个 元素。
element1~element2	p ~ ul	选择前面有 元素的每个 元素。
[attribute]	[target]	选择带有 target 属性的所有元素。
[attribute=value]	[target=_blank]	选择带有 target=“_blank” 属性的所有元素。
[attribute~=value]	[title~=flower]	选择 title 属性包含单词 “flower” 的所有元素。
[attribute	=value]	[lang
[attribute^=value]	a[href^=“https”]	选择其 src 属性值以 “https” 开头的每个 元素。
[attribute$=value]	a[href$=“.pdf”]	选择其 src 属性以 “.pdf” 结尾的所有 元素。
[attribute*=value]	a[href*=“w3schools”]	选择其 href 属性值中包含 “abc” 子串的每个 元素。
:active	a:active	选择活动链接。
::after	p::after	在每个 的内容之后插入内容。
::before	p::before	在每个 的内容之前插入内容。
:checked	input:checked	选择每个被选中的 元素。
:default	input:default	选择默认的 元素。
:disabled	input:disabled	选择每个被禁用的 元素。
:empty	p:empty	选择没有子元素的每个 元素（包括文本节点）。
:enabled	input:enabled	选择每个启用的 元素。
:first-child	p:first-child	选择属于父元素的第一个子元素的每个 元素。
::first-letter	p::first-letter	选择每个 元素的首字母。
::first-line	p::first-line	选择每个 元素的首行。
:first-of-type	p:first-of-type	选择属于其父元素的首个 元素的每个 元素。
:focus	input:focus	选择获得焦点的 input 元素。
:fullscreen	:fullscreen	选择处于全屏模式的元素。
:hover	a:hover	选择鼠标指针位于其上的链接。
:in-range	input:in-range	选择其值在指定范围内的 input 元素。
:indeterminate	input:indeterminate	选择处于不确定状态的 input 元素。
:invalid	input:invalid	选择具有无效值的所有 input 元素。
:lang(language)	p:lang(it)	选择 lang 属性等于 “it”（意大利）的每个 元素。
:last-child	p:last-child	选择属于其父元素最后一个子元素每个 元素。
:last-of-type	p:last-of-type	选择属于其父元素的最后 元素的每个 元素。
:link	a:link	选择所有未访问过的链接。
:not(selector)	:not§	选择非 元素的每个元素。
:nth-child(n)	p:nth-child(2)	选择属于其父元素的第二个子元素的每个 元素。
:nth-last-child(n)	p:nth-last-child(2)	同上，从最后一个子元素开始计数。
:nth-of-type(n)	p:nth-of-type(2)	选择属于其父元素第二个 元素的每个 元素。
:nth-last-of-type(n)	p:nth-last-of-type(2)	同上，但是从最后一个子元素开始计数。
:only-of-type	p:only-of-type	选择属于其父元素唯一的 元素的每个 元素。
:only-child	p:only-child	选择属于其父元素的唯一子元素的每个 元素。
:optional	input:optional	选择不带 “required” 属性的 input 元素。
:out-of-range	input:out-of-range	选择值超出指定范围的 input 元素。
::placeholder	input::placeholder	选择已规定 “placeholder” 属性的 input 元素。
:read-only	input:read-only	选择已规定 “readonly” 属性的 input 元素。
:read-write	input:read-write	选择未规定 “readonly” 属性的 input 元素。
:required	input:required	选择已规定 “required” 属性的 input 元素。
:root	:root	选择文档的根元素。
::selection	::selection	选择用户已选取的元素部分。
:target	#news:target	选择当前活动的 #news 元素。
:valid	input:valid	选择带有有效值的所有 input 元素。
:visited	a:visited	选择所有已访问的链接。
CSS选择器优先级
一 、CSS 有多少种样式类型：
行内样式：< style/style >
内联样式：< div style="color:red> ;
外部样式：< link > 或 @import引入
二 、常见选择器及选择器权重
选择器	格式	优先级权重
id选择器	#id	100
类选择器	.classname	10
属性选择器	a[ref = “eee”]	10
伪类选择器	li:last-child	10
标签选择器	div	1
为元素选择器	li:after	1
相邻兄弟选择器	h1 + p	0
子选择器	ul > li	0
后代选择器	li a	0
通配符选择器	*	0
三 、注意事项
!important声明的样式的优先级最高；
如果优先级相同，则最后出现的样式生效；
继承得到的样式的优先级最低；
通用选择器（*）、子选择器（>）和相邻同胞选择器（+）并不在这四个等级中，所以它们的权值都为0；
样式表的来源不同时，优先级顺序为：内联样式 > 内部样式 > 外部样式 > 浏览器用户自定义样式 > 浏览器默认样式。
选择器权重Specificity
如何比较两个优先级的高低呢？ 比较规则是: 从左往右依次进行比较 ，较大者胜出，如果相等，则继续往右移动一位进行比较 。如果4位全部相等，则后面的会覆盖前面的。
内联>id>类=属性=伪类>标签(类型、元素选择器h1)=伪元素
内联样式表的权值最高为 1000；
ID 选择器的权值为 100
Class 类选择器、属性选择器、伪类的权值为 10
HTML 元素选择器、伪元素的权值为 1
加有!important的权值最大，优先级最高
需要注意权值计算要基于选择器的形式。特别是，“[id=p33]”形式的选择器被视为属性选择器(权值为10)，即使id属性在源文档的文档类型中被定义为“id选择器”。
通配符 * 和关系选择符(+ > ~ '' ||)和否定伪类(:not()) 对优先级没有影响，但是:not内部声明的选择器会影响优先级。
*{} /*通用选择器，权值为0 */

p{color:red;} /*标签，权值为1*/

p span{color:green;} /*两个标签，权值为1+1=2*/

p>span{color:purple;}/*权值与上面的相同，因此采取就近原则*/

a:hover{}/*标签和伪类，权值为1+10=11*/

.warning{color:white;} /*类选择符，权值为10*/

p span .warning{color:purple;} /*权值为1+1+10=12*/

h1+a[rel=up]{}/*标签和属性选择器，权值为1+10=11*/

#footer .note p{color:yellow;} /*权值为100+10+1=111*/

p{color:red!important; }  /*优先级最高*/
注意事项
!important优先级最高。避免使用，会破坏样式表中固有的级联规则！！
样式表来源不同时 优先级顺序为：内联>内部>外部>浏览器用户自定义>浏览器默认。
兄弟选择器 li ~ a
相邻兄弟选择器 li + a
属性选择器 a[rel="external"]
伪类选择器 a:hover, li:nth-child
通配选择器 *{}
类型选择器h1{}
:link ：选择未被访问的链接
:visited：选取已被访问的链接
:active：选择活动链接
:hover ：鼠标指针浮动在上面的元素
:focus ：选择具有焦点的
:first-child：父元素的首个子元素
伪元素选择器 ::before、::after
::first-letter ：用于选取指定选择器的首字母
::first-line ：选取指定选择器的首行
::before : 选择器在被选元素的内容前面插入内容
::after : 选择器在被选元素的内容后面插入内容
CSS属性继承
继承属性和非继承属性
继承属性：
当元素的一个继承属性 没有指定值时，则取父元素的同属性的计算值
非继承属性：
当元素的一个非继承属性没有指定值时，则取属性的初始值
那么这两类属性都有哪些呢？
一、无继承性的属性
1、display：
规定元素应该生成的框的类
2、文本属性：
vertical-align：垂直文本对齐
text-decoration：规定添加到文本的装饰
text-shadow：文本阴影效果
white-space：空白符的处理
unicode-bidi：设置文本的方向
3、盒子模型的属性：
width、height、margin 、margin-top、margin-right、margin-bottom、margin-left、border、border-style、border-top-style、border-right-style、border-bottom-style、border-left-style、border-width、border-top-width、border-right-right、border-bottom-width、border-left-width、border-color、border-top-color、border-right-color、border-bottom-color、border-left-color、border-top、border-right、border-bottom、border-left、padding、padding-top、padding-right、padding-bottom、padding-left
4、背景属性：
background、background-color、background-image、background-repeat、background-position、background-attachment
5、定位属性：
float、clear、position、top、right、bottom、left、min-width、min-height、max-width、max-height、overflow、clip、z-index
6、生成内容属性：
content、counter-reset、counter-increment
7、轮廓样式属性：
outline-style、outline-width、outline-color、outline
8、页面样式属性：
size、page-break-before、page-break-after
9、声音样式属性：
pause-before、pause-after、pause、cue-before、cue-after、cue、play-during
二、有继承性的属性
1、字体系列属性
font：组合字体
font-family：规定元素的字体系列
font-weight：设置字体的粗细
font-size：设置字体的尺寸
font-style：定义字体的风格
font-variant：设置小型大写字母的字体显示文本，这意味着所有的小写字母均会被转换为大写，但是所有使用小型大写字体的字母与其余文本相比，其字体尺寸更小。
font-stretch：对当前的 font-family 进行伸缩变形。所有主流浏览器都不支持。
font-size-adjust：为某个元素规定一个 aspect 值，这样就可以保持首选字体的 x-height。
2、文本系列属性
text-indent：文本缩进
text-align：文本水平对齐
line-height：行高
word-spacing：增加或减少单词间的空白（即字间隔）
letter-spacing：增加或减少字符间的空白（字符间距）
text-transform：控制文本大小写
direction：规定文本的书写方向
color：文本颜色
3、元素可见性：
visibility
4、表格布局属性：
caption-side、border-collapse、border-spacing、empty-cells、table-layout
5、列表布局属性：
list-style-type、list-style-image、list-style-position、list-style
6、生成内容属性：
quotes
7、光标属性：
cursor
8、页面样式属性：
page、page-break-inside、windows、orphans
9、声音样式属性：
speak、speak-punctuation、speak-numeral、speak-header、speech-rate、volume、voice-family、pitch、pitch-range、stress、richness、、azimuth、elevation
三、所有元素可以继承的属性
1、元素可见性：
visibility
2、光标属性：
cursor
四、内联元素可以继承的属性
1、字体系列属性
2、除text-indent、text-align之外的文本系列属性
五、块级元素可以继承的属性
1、text-indent、text-align
不可/可继承属性
可继承
字体属性
文本属性
元素可见性
列表布局属性
光标属性
不可继承
盒子模型属性
display
背景属性
定位属性
生成内容、轮廓样式、页面样式、声音样式
line-height 如何继承
父元素的 line-height 写了具体数值，比如 30px，则子元素 line-height 继承该值。
父元素的 line-height 写了比例，比如 1.5 或 2，则子元素 line-height 也是继承该比例。
父元素的 line-height 写了百分比，比如 200%，则子元素 line-height 继承的是父元素 fontSize * 200% 计算出来的值。
CSS常考属性
CSS隐藏元素的方法有哪些
常见的隐藏属性的方法有 display: none 与 visibility: hidden：
display: none：渲染树不会包含该渲染对象，因此该元素不会在页面中占据位置，也不会响应绑定的监听事件。
visibility: hidden：元素在页面中仍占据空间，但是不会响应绑定的监听事件。
opacity: 0：将元素的透明度设置为0，以此来实现元素的隐藏。元素在页面中仍然占据空间，并且能够响应元素绑定的监听事件。
position: absolute：通过使用绝对定位将元素移除可视区域内，以此来实现元素的隐藏。
z-index: 负值：来使其他元素遮盖住该元素，以此来实现隐藏。
clip/clip-path：使用元素裁剪的方法来实现元素的隐藏，这种方法下，元素仍在页面中占据位置，但是不会响应绑定的监听事件。
transform: scale(0,0)：将元素缩放为0，来实现元素的隐藏。这种方法下，元素仍在页面中占据位置，但是不会响应绑定的监听事件。
在VUE中还有 v-if 和 v-show 这两个指令，在目录你能看到关于这两个的使用区别
display: none与 visibility: hidden的区别
这两个属性都是让元素隐藏，不可见。两者的区别主要分两点
1 、是否在渲染树中
display: none 会让元素完全从渲染树中消失，渲染时不会占据任何空间；
visibility: hidden 不会让元素从渲染树中消失，渲染的元素还会占据相应的空间，只是内容不可见。
2 、是否是继承属性
display: none 是非继承属性，子孙节点会随着父节点从渲染树消失，通过修改子孙节点的属性也无法显示；
visibility: hidden 是继承属性，子孙节点消失是由于继承了 hidden，通过设置 visibility: Avisible可以让子孙节点显示；
修改常规文档流中元素的 display 通常会造成文档的重排，但是修改 visibility 属性只会造成本元素的重绘
如果使用读屏器，设置为 display: none 的内容不会被读取，设置为 visibility: hidden 的内容会被读取。
这两者的关系类似于 v-if 和 v-show 之间的关系
文本溢出
单行溢出
text-overflow：当文本溢出时，显示省略符号代表被修剪的文本
white-space：设置文字在一行显示，不能换行
overflow：文字长度超出限定宽度，隐藏超出的内容
overflow:hidden，普通情况用在块级元素的外层隐藏内部溢出元素，或配合以下两个属性实现文本溢出省略
white-space:nowrap，设置文本不换行，是overflow:hidden和text-overflow:ellipsis生效的基础
text-overflow属性值如下：
clip：对象内文本溢出部分裁掉
ellipsis：对象内文本溢出时显示...
多行溢出
基于高度截断
伪元素+定位
通过伪元素绝对定位到行尾并遮住文字，再通过overflow:hidden，隐藏多余文字
优点
兼容性好
响应式截断，根据不同宽度做出调整
基于行数截断
background-size
设置背景图片大小。图片可以保有其原有的尺寸、拉伸到新的尺寸，或者在保持原有比例的同时缩放到元素的可用空间的尺寸
div
{
    width: 300px;
    height: 200px;
    background: url("../assets/2.jpg")no - repeat;
    border: 1px solid red;
    /*background-size: 100%;*/
    background - size: cover;
}
/*若图片宽度250px，宽度为250px，让该图片完全铺满整个div区域，设置background-size*/
属性
100%：整个图片铺满div
cover：整个图片铺满div，缩放背景图片以完全覆盖背景区，可能背景图片部分看不见。和 contain 相反，cover 尽可能大地缩放背景图像并保持图像的宽高比例（图像不会被压扁）。背景图以它的全部宽或者高覆盖所在容器。当容器和背景图大小不同时，背景图的 左/右 或者 上/下 部分会被裁剪
contain：不能铺满整个div，缩放背景图片以完全装入背景区，可能背景区部分空白。contain 尽可能地缩放背景并保持图像的宽高比例（图像不会被压缩）。背景图会填充所在容器。当背景图和容器的大小的不同时，容器的空白区域（上/下或者左/右）显示由 background-color 设置的背景颜色
auto：不能铺满整个div，以背景图片比例缩放背景图片
z-index
取值
数字无单位
auto(默认)和其父元素一样的层叠等级
整数
inherit继承
层叠上下文和层叠等级
对每一个网页来说，默认创建一个层叠上下文(可类比一张桌子)，这个桌子就是html元素，html元素的所有子元素都位于这个默认层叠上下文中的某个层叠等级(类似于桌子上放了一个盆儿，盆上放了一个果盘，果盘上放了一个水杯……)
将元素的z-index属性设置为非auto时，会创建一个新的层叠上下文，它及其包含的层叠等级独立于其他层叠上下文和层叠等级(类似于搬了一张新桌子过来，和旧桌子完全独立)
层叠顺序
div默认在html之上，及div的层级高于html
一个层叠上下文可能出现7个层叠等级，从低到高排列为
背景和边框
z-index为负数
block盒模型(位于正常文档流，块级，非定位)
float盒模型(浮动，非定位)
inline盒模型(位于正常文档流，内联，非定位)
z-index=0
z-index为正数(数值越大越靠上方)
压盖顺序
自定义压盖顺序：使用属性z-index
只有定位元素(position属性明确设置为absolute、fixed或relative)可使用z-index
如果z-index值相同，html结果在后面的压盖住在前面的
父子都有z-index，父亲z-index数值小时，儿子数值再大没用
client、offset&scroll
client 主要与可视区有关
客户区大小指的是元素内容及其内边距所占据空间大小。
offset 主要与自身有关
偏移量，可动态得到元素的位置（偏移），大小。**元素在屏幕上占用的所有可见空间。**元素高度宽度包括内边距，滚动条和边框。
offsetParent是一个只读属性，返回一个指向最近的（closest，指包含层级上的最近）包含该元素的定位元素。如果没有定位的元素，则 offsetParent 为最近的 table, td, th或body元素。当元素的 style.display 设置为 “none” 时，offsetParent 返回 null。
element.clientWidth获取元素可视区的宽度，不包括垂直滚动条
element.offsetWidth获取元素的宽度= boder + padding + content
element.clientHeight获取元素可视区的高度，不包括水平滚动条
element.offsetHeight获取元素的高度= boder + padding + content
clientWidth 和 clientHeight 获取的值不包含边框
offsetWidth 和 offsetHeight 获取的值包含左右边框
element.clientTop获取元素的上边框宽度，不包括顶部外边距和内边距
element.clientLeft获取元素的左边框宽度
element.offsetTop获取元素到有定位的父盒子的顶部距离
element.offsetLeft获取元素到有定位的父盒子的左侧距离
e.clientX鼠标距离可视区的左侧距离
e.clientY鼠标距离可视区的顶部距离
scroll 滚动系列
动态获得元素大小，滚动距离等。具有兼容问题。
scrollWidth 和 scrollHeight 主要用于确定元素内容的实际大小
scrollLeft 和 scrollTop 属性既可以确定元素当前滚动的状态，也可以设置元素的滚动位置
垂直滚动 scrollTop > 0
水平滚动 scrollLeft > 0
将元素的 scrollLeft 和 scrollTop 设置为 0，可以重置元素的滚动位置
共同点
返回数字时，均不带单位。
只读。
CSS3新特性
CSS3新特性
新增选择器： p:nth-child（n）{color: rgba（255, 0, 0, 0.75）}
弹性盒模型： 弹性布局： display: flex; 栅格布局： display: grid;
渐变 线性渐变： linear-gradient（red, green, blue）； 径向渐变：radial-gradient（red, green, blue）
边框 border-radius：创建圆角边框 box-shadow：为元素添加阴影 border-image：使用图片来绘制边框
阴影 box-shadow:3px 3px 3px rgba（0, 64, 128, 0.3）；
背景 用于确定背景画区：background-clip 设置背景图片对齐：background-origin 调整背景图片的大小background-size 控制背景怎样在这些不同的盒子中显示：background-break 多列布局： column-count: 5;
text-overflow 文字溢出时修剪：text-overflow：clip 文字溢出时省略符号来代表：text-overflow：ellipsis
transform 转换 transform: translate(120px, 50%)：位移 transform: scale(2, 0.5)：缩放 transform: rotate(0.5turn)：旋转 transform: skew(30deg, 20deg)：倾斜
animation 动画 animation-name：动画名称 animation-duration：动画持续时间 animation-timing-function：动画时间函数 animation-delay：动画延迟时间 animation-iteration-count：动画执行次数，可以设置为一个整数，也可以设置为infinite，意思是无限循环 animation-direction：动画执行方向 animation-paly-state：动画播放状态 animation-fill-mode：动画填充模式
还有多列布局、媒体查询（@media）、混合模式等等，而CSS3如今有很多是我们日常使用到的，比如我们在处理文字溢出时会使用 text-overflow ，比如我们需要文字突破限制12像素就可以使用 transform: scale（0.5）来调整。
flex布局
弹性布局。可以 简便、完整、响应式地实现各种页面布局。为盒模型提供最大的灵活性。
父容器和子容器构成，通过主轴和交叉轴控制子容器排列布局，子元素float、clear和vertical-align属性失效
父容器
flex-direction
flex-wrap
flex-flow
justify-content
align-items
align-content
flex-direction
.container {
flex-direction: row | row-reverse | column | column-reverse;
}
决定主轴方向，子元素的排列方向
flex-wrap
.container {
flex-wrap: nowrap | wrap | wrap-reverse;
}
弹性元素永远沿主轴排列，那么如果主轴排不下，通过flex-wrap决定容器内项目是否可换行。
默认情况是不换行，但这里也不会任由元素直接溢出容器，会涉及到元素的弹性伸缩。
flex-flow
是flex-direction属性和flex-wrap属性的简写形式，默认值为row nowrap
当flex-grow之和小于1时，只能按比例分配部分剩余空间，而不是全部。
.box {
flex-flow: || ;
}
justify-content
定义了项目在主轴上的对齐方式
.box {
justify-content: flex-start | flex-end | center | space-between | space-around;
}
flex-start（默认值）：左对齐
flex-end：右对齐
center：居中
space-between：两端对齐，项目之间的间隔都相等
space-around：两个项目两侧间隔相等
align-items
.box {
align-items: flex-start | flex-end | center | baseline | stretch;
}
定义项目在交叉轴上如何对齐
flex-start：交叉轴的起点对齐
flex-end：交叉轴的终点对齐
center：交叉轴的中点对齐
baseline: 项目的第一行文字的基线对齐
stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度
align-content
.box {
align-content: flex-start | flex-end | center | space-between | space-around | stretch;
}
定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用
flex-start：与交叉轴的起点对齐
flex-end：与交叉轴的终点对齐
center：与交叉轴的中点对齐
space-between：与交叉轴两端对齐，轴线之间的间隔平均分布
space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍
stretch（默认值）：轴线占满整个交叉轴
子容器
order
flex-grow
flex-shrink
flex-basis
flex
align-self
order
定义item排列顺序，越小越靠前，默认0
flex-grow
定义项目的放大比例（容器宽度>元素总宽度时如何伸展）
默认为0，即如果存在剩余空间，也不放大。
flex-warp：nowrap；不换行的时候，container宽度不够分时，弹性元素会根据flex-grow来决定。
如果所有项目的flex-grow属性都为1，则它们将等分剩余空间（如果有的话）
如果一个项目的flex-grow属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍
弹性容器的宽度正好等于元素宽度总和，无多余宽度，此时无论flex-grow是什么值都不会生效。
flex-shrink
定义了项目的缩小比例（容器宽度<元素总宽度时如何收缩），默认为1，即如果空间不足，该项目将缩小。flex 元素仅在默认宽度之和大于容器的时候才会发生收缩，其收缩的大小是依据 flex-shrink 的值。
如果所有项目的flex-shrink属性都为1，当空间不足时，都将等比例缩小。
如果一个项目的flex-shrink属性为0，其他项目都为1，则空间不足时，前者不缩小。
flex-basis
定义分配多余空间前，占据主轴空间 默认auto。 元素在主轴上的初始尺寸，所谓的初始尺寸就是元素在flex-grow和flex-shrink生效前的尺寸
flex:1
等分剩余空间
flex: 1 相当于 flex-grow: 1、flex-shrink: 1 和 flex-basis: 0%。
flex 属性是 flex-grow, flex-shrink 和 flex-basis 的简写，默认值为 0 1 auto。后两个属性可选。
优先使用这个属性，而不是单独写三个分离的属性，因为浏览器会推算相关值。
flex: 1 = flex: 1 1 0%
flex: 2 = flex: 2 1 0%
flex: auto = flex: 1 1 auto
flex: none = flex: 0 0 auto，常用于固定尺寸不伸缩
aline-self
默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch。
允许单个项目有与其他项目不一样的对齐方式，可覆盖align-items属性
左边固定右边自适应
//垂直居中
flex-direction:row/column;
align-items:center
//水平局中
flex-direction:row/column;
justify-content:center;
flex: 1 = flex: 1 1 0%
flex: 2 = flex: 2 1 0%
flex: auto = flex: 1 1 auto
flex: none = flex: 0 0 auto，常用于固定尺寸不伸缩
隐藏元素
display:none
不会在页面占据位置
渲染树不会包含该渲染对象
不会绑定响应事件
会导致浏览器进行重排和重绘
visibility:hidden
占据位置,不更改布局
不会响应绑定事件
不会重排但会重绘
opacity:0
元素透明度设置为0
占据位置
能响应绑定事件
不能控制子元素展示
不会引发重排，一般会引发重绘
如果利用 animation 动画，对 opacity 做变化（animation会默认触发GPU加速），则只会触发 GPU 层面的 composite，不会触发重绘
设置height width为0
将影响元素盒模型的属性设置为0，若有元素内有子元素或内容，应该设置其overflow:hidden来隐藏其子元素。
元素不可见
不占据空间
不响应点击事件
position：absolute
将元素移除可视区域
元素不可见
不影响页面布局
transform: scale(0,0)
占据位置
不响应绑定事件
不会触发浏览器重排
页面中不存在存在存在重排会不会不会重绘会会不一定自身绑定事件不触发不触发可触发transition不支持支持支持子元素可复原不能能不能被遮挡的元素可触发事件能能不能opacity和rgba区别
opacity 取值在0到1之间，0表示完全透明，1表示完全不透明。
.aa{opacity: 0.5;}
rgba中的R表示红色，G表示绿色，B表示蓝色，三种颜色的值都可以是正整数或百分数。A表示Alpha透明度。取值0~1之间，类似opacity。
.aa{background: rgba(255,0,0,0.5);}
rgba()和opacity都能实现透明效果，但最大的不同是opacity作用于元素，以及元素内的所有内容的透明度，而rgba()只作用于元素的颜色或其背景色。
**总结：**opacity会继承父元素的 opacity 属性，而RGBA设置的元素的后代元素不会继承不透明属性。
常见布局
两栏布局
左边宽度固定，右边宽度自适应。
利用flex布局，将左边元素设置为固定宽度200px，将右边的元素设置为flex:1
利用浮动。左边元素宽度设置为200px，且设置向左浮动。右边元素的margin-left设置为200px，宽度设置为auto（默认为auto，撑满整个父元素）。margin-left/padding-left/calc
利用浮动。左边元素宽度固定 ，设置向左浮动。右侧元素设置 overflow: hidden; 这样右边就触发了 BFC ，BFC 的区域不会与浮动元素发生重叠，所以两侧就不会发生重叠。 float + overflow:hidden
左列左浮动,将自身高度塌陷,使得其它块级元素可以和它占据同一行位置
右列利用自身流特性占满整行
右列设置overflow,触发BFC特性,使自身和左列浮动元素隔开,不沾满整行
绝对定位 父级相对定位 左边absolute定位，宽度固定。设置右边margin-left为左边元素的宽度值。
绝对定位，父级元素相对定位。左边元素宽度固定，右边元素absolute定位，left为宽度大小，其余方向为0。(有歧义,谨慎使用!)
使用 calc 计算
.left {

   display: inline-block;
   width: 240px;
}

.right {

   display: inline-block;
   width: calc(100% - 240px);
}

//使用 calc() 函数计算 <div> 元素的宽度
grid
三栏布局
其中一列宽度自适应。
float布局
缺点：html结构不正确,当包含区域宽度小于左右框之和，右边框会被挤下来。float布局需要清除浮动，因为float会脱离文档流，会造成高度塌陷的问题。
两边float+中间margin
两变固定，中间自适应
中间元素margin值控制两边间距
宽度小于左右部分宽度之和时，右侧部分被挤下去
<!DOCTYPE html>

<html lang="en">

<head>

	<meta charset="UTF-8">

	<title>Title</title>

</head>

<body>

<style>

 .left {

    float: left;

    width: 300px;

    background-color: #a00;

 }


 .right {

    float: right;

    width: 300px;

    background-color: #0aa;

 }


 .center {

    margin: 0 300px;

    background-color: #aa0;

    overflow: auto;

 }

</style>

<section class="float">

  <article class="left">

    <h1>我是浮动布局左框</h1>

  </article>

  <article class="right">

    <h1>我是浮动布局右框</h1>

  </article>

  <article class="center">

    <h1>我是浮动布局中间框</h1>

  </article>

</section>


</body>

</html>
BFC布局
将main变成BFC，就不会和浮动元素发生重叠。
父元素设置overflow: hidden;
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

  *{

    margin: 0;

    padding: 0;

 }

 .left {

    float: left;

    background-color: red;

    width: 100px;

    height: 200px;

 }


 .right {

    float: right;

    background-color: blue;

    width: 100px;

    height: 200px;

 }

 .main{

    background-color: green;

    height: 200px;

    overflow: hidden;

 }

</style>

<div class="container">

  <div class="left"></div>

  <div class="right"></div>

  <div class="main">22111111jygjegrearewqrewqewgrhtyhyt</div>

</div>

</body>

</html>

table布局
优点:表格布局被称之为已经淘汰的布局，包括现在应该也很少有人使用，包括flex布局不兼容的情况下table还可以尝试，类似这种三栏布局，table的实现也很简单，这个东西自我觉得看个人喜爱了，能满足日常使用的话用用也未尝不可。
缺点:表格布局相当于其他布局，使用相对繁琐，代码量大，同时也存在缺陷，当单元格的一个格子超出高度之后，两侧就会一起触发跟着一起变高，这显然不是我们想要看到的情况。
display:table

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

 .table {

    display: table;

    width: 100%;

 }



 .table > article {

    display: table-cell;

 }



 .left {

    width: 300px;

    background-color: #a00;

 }



 .center {

    background-color: #aa0;

 }



 .right {

    width: 300px;

    background-color: #0aa;

 }



</style>

<section class="table">

  <article class="left">

    <h1>我是表格布局左框</h1>

  </article>

  <article class="center">

    <h1>我是表格布局中间框</h1>

  </article>

  <article class="right">

    <h1>我是表格布局右框</h1>

  </article>

</section>



</body>

</html>
flex弹性布局
利用flex布局，左右两栏设置固定大小，中间一栏设置为flex:1
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

 .flex {

    display: flex;

 }



 .left {

    width: 300px;

    /flex-shrink: 0; ! 不缩小 !/

    background-color: #a00;

 }



 .center {

    /flex-grow: 1; ! 增大 !/

    flex: 1;

    background-color: #aa0;

 }



 .right {

    /flex-shrink: 0; ! 不缩小 !/

    width: 300px;

    background-color: #0aa;

 }

</style>

<section class=" flex">

  <article class="left">

    <h1>我是flex弹性布局左框</h1>

  </article>

  <article class="center">

    <h1>我是flex弹性布局中间框</h1>

  </article>

  <article class="right">

    <h1>我是flex弹性布局右框</h1>

  </article>

</section>



</body>

</html>
grid栅格布局
优点:网格布局作为一个比较超前一点的布局自然有其独特的魅力，其布局方式布局思维都可以让你眼前一亮，有种新的思想。
缺点:兼容性
grid-template-columns 该属性是基于 网格列 的维度，去定义网格线的名称和网格轨道的尺寸大小。
用单位 fr 来定义网格轨道大小的弹性系数。 每个定义了 的网格轨道会按比例分配剩余的可用空间。当外层用一个 minmax() 表示时，它将是一个自动最小值(即 minmax(auto, ) ) 。
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

 .grid {

    display: grid;

    grid-template-columns: 300px 3fr 300px;

 }



 .grid .left {

    background-color: #a00;

 }



 .grid .center {

    background-color: #aa0;

 }



 .grid .right {

    background-color: #0aa;

 }

</style>

<section class="grid">

  <article class="left">

    <h1>我是grid栅格布局左框</h1>

  </article>

  <article class="center">

    <h1>我是grid栅格布局中间框</h1>

  </article>

  <article class="right">

    <h1>我是grid栅格布局右框</h1>

  </article>

</section>



</body>

</html>
圣杯布局
缺点：需要多加一层标签，html顺序不对，占用了布局框的margin属性。
圣杯布局的核心是左、中、右三栏都通过float进行浮动，然后通过负值margin进行调整。
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

 .container{

    padding-left: 100px;

    padding-right: 100px;

 }

 .left {

    float: left;

    width: 100px;

    height: 200px;

    background-color: red;

    margin-left: -100%;

    position: relative;

    left: -100px;

 }



 .right {

    float: left;

    width: 100px;

    height: 200px;

    background-color: yellow;

    margin-left: -100px;

    position: relative;

    right: -100px;

 }



 .main {

    float: left;

    width: 100%;

    height: 200px;

    background-color: green;

 }

</style>

<body>

<div class="container">

  <div class="main">发发发发发发返回和王企鹅王企鹅王企鹅而非</div>

  <div class="left"></div>

  <div class="right"></div>

</div>

</body>



</body>

</html>
双飞翼布局
双飞翼布局的前两步和圣杯布局一样，只是处理中间栏部分内容被遮挡问题的解决方案有所不同：
既然main部分的内容会被遮挡，那么就在main内部再加一个content，通过设置其margin来避开遮挡，问题也就可以解决了
双飞翼布局(两边 float+margin)，就是圣杯布局的改进方案。
<!DOCTYPE html>

<html lang="en">

<head>

  <style>

   .main {

      float: left;

      width: 100%;

   }

   .content {

      height: 200px;

      margin-left: 110px;

      margin-right: 220px;

      background-color: green;

   }

    /CSS伪元素::after用来创建一个伪元素，作为已选中元素的最后一个子元素。/

   .main::after {

      display: block;

      content: '';

      font-size: 0;

      height: 0;

      /唯一需要注意的是，需要在main后面加一个元素来清除浮动。/

      clear: both;

      zoom: 1;

   }

   .left {

      float: left;

      height: 200px;

      width: 100px;

      margin-left: -100%;

      background-color: red;

   }

   .right {

      width: 200px;

      height: 200px;

      float: left;

      margin-left: -200px;

      background-color: blue;

   }

  </style>

</head>

<body>

<div>

  <div class="main">

    <div class="content"></div>

  </div>

  <div class="left"></div>

  <div class="right"></div>

</div>

</body>

</html>
定位布局
优点：很快捷，设置很方便，而且也不容易出问题，你可以很快的就能想出这种布局方式。要求父级要有非static定位，如果没有，左右框容易偏移出去
缺点：绝对定位是脱离文档流的，意味着下面的所有子元素也会脱离文档流，这就导致了这种方法的有效性和可使用性是比较差的。
子绝父相，父元素设置为relative，左右两栏设置为absolute+中间一栏margin。
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<body>

<style>

 .tree-columns-layout {

    position: relative;

 }



 .left {

    position: absolute;

    left: 0;

    top: 0;

    width: 300px;

    background-color: #a00;

 }



 .right {

    position: absolute;

    right: 0;

    top: 0;

    width: 300px;

    background-color: #0aa;

 }



 .center {

    margin: 0 300px;

    background-color: #aa0;

    overflow: auto;

 }

</style>

<section class="tree-columns-layout">

  <article class="left">

    <h1>我是浮动定位左框</h1>

  </article>

  <article class="center">

    <h1>我是浮动定位中间框</h1>

  </article>

  <article class="right">

    <h1>我是浮动定位右框</h1>

  </article>

</section>



</body>

</html>
绝对定位
三栏均设置为absolute+left+right。
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

</head>

<style>

    {

    margin: 0;

    padding: 0;

 }

 .middle {

    position: absolute;

    left: 200px;

    right: 200px;

    height: 300px;

    background-color: yellow;

 }



 .left {

    position: absolute;

    left: 0px;

    width: 200px;

    height: 300px;

    background-color: red;

 }



 .right {

    position: absolute;

    right: 0px;

    width: 200px;

    background-color: green;

    height: 300px;

 }

</style>

<body>

<div class="container">

  <div class="middle">

  </div>

  <div class="left"></div>

  <div class="right"></div>

</div>

</body>



</body>

</html>
垂直居中
top属性会影响定位元素的垂直位置。此属性对非定位元素没有影响。
如果position: absolute;或position: fixed; top属性将元素的上边缘设置为其最近定位的祖先的上边缘上方/下方的单位。
如果position: relative; top属性使元素的上边缘在其正常位置上方/下方移动。
如果position: sticky; top当元素在视口内时，属性的行为类似于它的位置，并且当它在外面时它的位置是固定的。
如果position：static; top属性无效。
flex布局
justify-content: center;
align-items: center;
居中元素定宽高适用
absolute相对于包含块进行偏移（所谓包含块就是最近一级外层元素position不为static的元素）。
absolute+margin auto。因为宽高固定，对应方向实现平分
absolute+calc
利用绝对定位，设置 left: 50% 和 top: 50% 现将子元素左上角移到父元素中心位置，然后再通过 margin-left 和 margin-top 以子元素自己的一半宽高进行负值赋值。
居中元素不定宽高
absolute+transform
利用绝对定位，先将元素的左上角通过top:50%和left:50%定位到页面的中心，然后再通过margin负值来调整元素的中心点到页面的中心。
transform: translate(-50%,-50%);
line-height:initial默认
writing-mode:vertical-lr;改变文字的显示方向
table table-cell
css-table PC有兼容性要求，宽高不固定，推荐
flex 兼容性好
grid + align-items兼容性不行
top：定位元素的上外边距边界与其包含块上边界之间的偏移，非定位元素设置此属性无效。
水平居中
不定宽高
定位+margin:auto
定位+transform
定位+margin:负值
flex布局
grid布局
内联元素
水平居中
行内元素可设置：text-align: center
flex布局设置父元素：display: flex; justify-content: center
垂直居中
单行文本父元素确认高度：height === line-height
多行文本父元素确认高度：disaply: table-cell; vertical-align: middle
块级元素
水平居中
定宽: margin: 0 auto
绝对定位+left:50%+margin:负自身一半
垂直居中
position: absolute设置left、top、margin-left、margin-top(定高)
display: table-cell
transform: translate(x, y)
flex(不定高，不定宽)
grid(不定高，不定宽)，兼容性相对比较差
水平垂直居中
水平垂直居中的10种方式
定位 + margin: auto
定位 + margin: 负值
定位 + transform
table布局
flex布局
grid布局
div居中的几种方式
方式一
position: absolute;
top: 0;
bottom: 0;
left: 0;
right: 0;
margin: auto;
方式二 可以给父元素添加下面的属性，利用 flex 布局来实现
display: flex;
align-items: center;
flex-direction: column
方式三 通过定位和变形来实现 给父元素添加 position: relative;相对定位。 给自身元素添加position: absolute;绝对定位。 top: 50%;使自身元素距离上方“父元素的50%高度”的高度。 left: 50%;使自身元素距离上方“父元素的50%宽度”的宽度。 transform: translate(-50%,-50%);使自身元素再往左，往上平移自身元素的50%宽度和高度。
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%,-50%);
方式四 这个是实现内容文本居中的，坑死了，之前没留意在一个全局的文件加了，后面很多组件里面的内容都居中了，还一时没发现，虽然想到会不会是全局文件的问题，但一下子眼拙没看到，结果捣鼓半天
body{ text-align:center} 
CSS画三角形
CSS画三角形的实现方式
实现1px效果
伪元素+缩放
动态viewport+rem(flex)
vw单位适配(未来推荐)
伪元素+缩放
设计稿中的1px，代码要实现0.5px
缩放 避免 直接写小数像素带来的不同手机的兼容性处理不同
<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>Title</title>

  <style>

   /*伪元素实现0.5px border*/

   .border::after {

    content: "";

    /*为了与原元素等大*/

    box-sizing: border-box;

    position: absolute;

    left: 0;

    top: 0;

    width: 200%;

    height: 200%;

    border: 1px solid red;

    transform: scale(0.5);

    transform-origin: 0 0;

   }



   /*实现0.5px 细线*/

   .line::after {

    content: '';

    position: absolute;

    top: 0;

    left: 0;

    width: 200%;

    height: 1px;

    background: red;

    transform: scale(0.5);

    /*更改元素变形的原点*/

    transform-origin: 0 0;

   }



   /*dpr适配 ，当前显示设备的物理像素分辨率与CSS 像素分辨率之比为2*/

   @media (-webkit-min-device-pixel-ratio: 2) {

    .line::after {

     height: 1px;

     transform: scale(0.5);

     transform-origin: 0 0;

    }

   }



   @media (-webkit-min-device-pixel-ratio: 3) {

    .line::after {

     height: 1px;

     transform: scale(0.333);

     transform-origin: 0 0;

    }

   }

  </style>

</head>

<body>

<div class="border">

  <div class="line"></div>

</div>

</body>

</html>
动态viewport+rem
不仅可解决移动端适配，也解决1px的问题
三种viewport中我们常用的layout viewport(浏览器默认)，宽度大于浏览器可视区域宽度，因此会出现横向滚动条
const clientWidth = document.documentElement.clientWidth || document.body.clientWidth
设置meta标签属性避免横向滚动条
 < meta
name = "viewport"

    content = "
    width=device-width,  // viewport宽等于屏幕宽
    initial-scale=1.0,  // 初始缩放为1
    maximum-scale=1.0,
    user-scalable=no,  // 不允许手动缩放
    viewport-fit=cover // 缩放以填充满屏幕
    "
    >
flexible的原理——已弃用！
根据dpr动态修改initial-scale
动态修改viewport大小，以此 统一使用rem布局，viewport动态影响font-size，实现适配
总结
移动端适配主要分为两方面
适配不同机型的屏幕尺寸
对细节像素的处理。如果直接写 1px ，由于 dpr 的存导致渲染偏粗。使用rem 布局计算出对应小数值，有兼容性问题。老项目整体修改 viewport 成本过高，采用第一种实现方案处理；新项目可动态设置 viewport ，一键解决适配问题
移动端对 1px 的渲染适配实现起来配置简单、代码简短，能够快速上手
使chrome支持12px以下文字
在谷歌浏览器中，字体的最小值为 12px，当你设置字体为 10px 的时候，结果显示的还是12px，这是因为 Chrome 浏览器做了如下限制：
font-size 有一个最小值 12px（不同操作系统、不同语言可能限制不一样），低于 12px 的，一律按 12px 显示。
理由是 Chrome 认为低于 12px 的中文对人类是不友好的。但是你可以设置为 0
zoom
"变焦"，可以改变页面上元素的尺寸，属于真实尺寸。有兼容问题，非标准属性，缩放会改变元素占据空间大小，触发重排
zoom:50%，表示缩小到原来的一半
zoom:0.5，表示缩小到原来的一半
 .test1 {

  font-size: 10px;

  zoom: 0.8;

 }

 .test2 {

  font-size: 16px;

 }
-webkit-transform:scale()
针对Chrome使用webkit前缀
使用scale属性只对可以定义宽高的元素生效。不改变页面布局
 .test1 {

  font-size: 5px;

  display: inline-block;

  transform: scale(0.8);

 }

 .test2 {

  font-size: 16px;

  display: inline-block;

 }
-webkit-text-size-adjust:none
设定文字大小是否根据设备(浏览器)来自动调整显示大小
percentage：字体显示的大小；
auto：默认，字体大小会根据设备/浏览器来自动调整；
none:字体大小不会自动调整
响应式布局
响应式布局原理和方案
页面的设计和开发根据用户行为和设备环境进行调整和响应
Content is like water
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no”>
width=device-width: 自适应手机屏幕的尺寸宽度
maximum-scale:缩放比例的最大值
inital-scale:缩放的初始化
user-scalable:用户可以缩放
实现响应式布局的方式
媒体查询
百分比
vw/vh
rem
响应式设计实现通常会从以下几方面思考：
弹性盒子和媒体查询等
百分比布局创建流式布局的弹性UI，同时使用媒体查询限制元素的尺寸和内容变更范围
相对单位使得内容自适应调节
缺点：
仅适用布局、信息、框架并不复杂的部门类型网站
兼容各种设备工作量大，效率低下
代码累赘，出现隐藏无用的元素，加载时间加长
一定程度上改变了网站原有的布局结构
媒体查询
媒体查询可以让我们针对不同的媒体类型定义不同的样式，当重置浏览器窗口大小的过程中，页面也会根据浏览器的宽度和高度重新渲染页面。
百分比
通过百分比单位，可以使得浏览器中组件的宽和高随着浏览器的高度的变化而变化，从而实现响应式的效果。
vw/vh
px、em、rem、vh、vw的区别及使用场景
这几个单位是在写长度的时候常常会用到的：
一、px
px：也就是像素，是基于屏幕分辨率来说的，一旦设置了，就无法适应页面大小的变化。
二、em
em：是相对单位，相对于当前对象内文本的字体大小（也就是它的父元素），如果当前对象内文本的字体没有设置大小，就会相对于浏览器默认字体大小也就是16px。所以在没有设置的情况下 1em = 16px。
为了便于运算你可以在body选择器中声明Font-size=62.5%；这就使em值变为 16px*62.5%=10px, 这样12px=1.2em, 10px=1em, 也就是说只需要将你的原来的px数值除以10，然后换上em作为单位就行了。
三、rem
rem：rem的出现是为了解决em的问题的，em是相对于父元素来说的，这就要求我们进行任何元素设置的时候，都需要知道它的父元素字体的大小。而 rem是相对于根元素，这样就意味着，我们只需要在根元素确定一个参考值，就可以了，同时还能做到只修改根元素就成比例地调整所有字体大小。
四、vh、vw
vh、vw：vw 是根据窗口的宽度。会把窗口的大小分为100份，所以50vw代表窗口大小的一半。并且这个值是相对的，当窗口大小发生改变也会跟着改变，同理，vh则为窗口的高度
四、总的来说，四者的区别：
px 是固定的大小，em 是相对于父元素字体的大小，rem 是相对于根元素字体的大小，vh、vw 是相对可是窗口的大小
五、使用场景的区别：
一般我们在设置边框和边距的时候用 px 比较好
而在一些需要做响应式的页面用 rem 比较便捷
但是具体还是得看你的业务来定的
rem布局
rem单位都是相对于根元素html的font-size来决定大小的,根元素的font-size相当于提供了一个基准，当页面的size发生变化时，只需要改变font-size的值，那么以rem为固定单位的元素的大小也会发生响应的变化。
过渡与动画
transition和animation
javascript直接实现
JS实现动画导致页面频繁性重排重绘，消耗性能.
SVG（可伸缩矢量图形）
控制动画延时
控制属性的连续改变
控制颜色变化
控制如缩放,旋转等几何变化
控制SVG内元素的移动路径
SVG是对图形的渲染，HTML是对DOM的渲染
CSS3 transition
transition是过度动画。但transition不能实现独立的动画，只能在某个标签元素样式或状态改变时进行平滑的动画效果过渡，而不是马上改变
注意在移动端开发中，直接使用transition动画会让页面变慢甚至卡顿。所以我们通常添加transform:translate3D(0,0,0)或transform:translateZ(0)来开启移动端动画的GPU加速，让动画过程更加流畅
transition:transform 1s ease; style="transform: translate(304px, 256px);"
动态改变transform的值，实现拖拽移动的效果
CSS3 animation3
animation 算是真正意义上的CSS3动画。通过对关键帧和循环次数的控制，页面标签元素会根据设定好的样式改变进行平滑过渡
比较CSS3最大的优势是摆脱了js的控制，并且能利用硬件加速以及实现复杂动画效果
Canvas
canvas作为H5新增元素，借助Web API来实现动画
只有width和height两个属性
requestAnimationFrame
requestAnimationFrame是另一种Web API，执行动画的效果，会在一帧(一般是16ms)间隔内根据选择浏览器情况执行相关动作
raf按照系统刷新的节奏调用！！
在性能上比另两者要好。
通常，我们将执行动画的每一步传到requestAnimationFrame中，在每次执行完后进行异步回调来连续触发动画效果。
JavaScript 动画 和 CSS动画
在前端中实现动画的方式有两种，也就是 JavaScript动画 和 CSS动画。
一、JavaScript 动画
JavaScript 动画就是通过对元素样式进行渐进式变化编程完成的。这种变化通过一个计数器来调用。当计数器间隔很小时，动画看上去就是连贯的。 实践中一般需要设置 style = “position: relative” 创建容器元素。通过 style = “position: absolute” 创建动画元素。然后通过定时器（绘图函数）来控制动画元素的变化，也就是按照我们的规则来修改 CSS样式。
二、CSS 动画
与 JavaScript动画使用定时器修改不同，CSS动画是通过指定 @keyframes 来指定动画效果，然后绑定到需要实习的元素上。
一般有属性：
@keyframes：规则中指定了 CSS 样式，动画将在特定时间逐渐从当前样式更改为新样式。 animation-name：用来绑定动画规则 animation-duration：定义需要多长时间才能完成动画 animation-delay：规定动画开始的延迟时间。也就是多久后才开始动画 animation-iteration-count：指定动画应运行的次数。 animation-direction：指定是向前播放、向后播放还是交替播放动画。 animation-timing-function：规定动画的速度曲线。 animation-fill-mode：SS 动画不会在第一个关键帧播放之前或在最后一个关键帧播放之后影响元素。animation-fill-mode 属性能够覆盖这种行为。 animation：实现与上例相同的动画效果，也就是类似我们的 font 可以包含所有的相关属性
//下面的例子将 "example" 动画绑定到 <div> 元素。动画将持续 4 秒钟，同时将 <div> 元素的背景颜色从 "red" 逐渐改为 "yellow"：
/* 动画代码 */
 @ keyframes example {
    from {
        background - color: red;
    }
    to {
        background - color: yellow;
    }
}

/* 向此元素应用动画效果 */
div {
    width: 100px;
    height: 100px;
    background - color: red;
    animation - name: example;
    animation - duration: 4s;
}

三、JavaScript 动画 和 Css动画优缺点
JS动画
优点：
过程可控，在动画中可以实现任何效果，暂停，返回，加速等等
动画效果丰富，可以根据绘图函数实现任意效果，跳跳球，变速等
兼容性好，使用 CSS3 存在兼容问题，但是 JavaScript 几乎没有
缺点：
JavaScript 在浏览器的主线程中运行，而主线程中还有其它需要运行的JavaScript脚本、样式计算、布局、绘制任务等,对其干扰导致线程可能出现阻塞，从而造成丢帧的情况。
代码的复杂度高于CSS动画。
CSS动画
优点（浏览器可以对动画进行优化）：
集中所有DOM，一次重绘重排，刷新频率和浏览器刷新频率相同。
代码简单，方便调试
不可见元素不参与重排，节约CPU
可以使用硬件加速（通过 GPU 来提高动画性能）。
缺点：
运行过程控制较弱，无法附加事件绑定回调函数。
代码冗长。
SCSS
1、 嵌套
$baseColor: red;
$color1: green;
body{
  background-color: $baseColor;
  $color2: yellow;
  div{
    background-color:$color2;
    color: $color1;
  }
   div2{
    background-color:$color2;
    color: $color1;
  }
}
//编译后
body {
  background-color: red;
   }
  body div {
    background-color: yellow;
    color: green; 
   }
 body div2 {
   background-color: yellow;
   color: green; 
}
2、 定义变量
$baseColor: red;
$color1: green;
body{
  background-color: $baseColor;
}

div{
  background-color:$baseColor;
  color: $color1;
}
//编译出的结果
body {
  background-color: red; }

div {
  background-color: red;
  color: green; }
3、 混合
@mixin box-sizing($sizing) {
  -webkit-box-sizing: $sizing;
  -moz-box-sizing: $sizing;
  box-sizing: $sizing;
}

.box-border{
  border: 1px  solid red;
  @include box-sizing(border-box)
}

//编译结果
.box-border {
  border: 1px  solid red;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box; 
  }
4、 继承
.A{
  color: red;
  border: #0D47A1 2px solid;
  background-color: #0e0e0e;
}
.B{
  @extend .A;
}
.C{
  @extend .A;
  border-color: #00a507;
}
//编译结果
.A, .B, .C {
  color: red;
  border: #0D47A1 2px solid;
  background-color: #0e0e0e; 
  }

.C {
  border-color: #00a507;
   }
CSS性能优化
CSS性能优化的8个技巧
内联首屏关键CSS
异步加载CSS
资源压缩
合理使用选择器
减少使用昂贵的属性
不要使用@import
CSS雪碧图
小图片转为BASE64编码
