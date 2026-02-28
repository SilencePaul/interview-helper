HTML
DOCUTYPE的作用
DOCTYPE是document type (文档类型) 的缩写。 是HTML5中一种标准通用标记语言的文档类型声明，告诉浏览器文档的类型，便于解析文档。 不同的渲染模式会影响浏览器对 CSS 代码甚⾄ JavaScript 脚本的解析。它必须声明在HTML⽂档的第⼀⾏.
浏览器渲染页面的两种模式
CSS1 Compat：标准模式（Strick mode），浏览器使用W3C的标准解析渲染页面。浏览器以其支持的最高标准呈现页面。
BackCompat：怪异模式(混杂模式)(Quick mode)，默认模式，页面以一种比较宽松的向后兼容的方式显示。
DOCTYPE 不存在或者形式不正确会导致HTML或XHTML文档以混杂模式呈现，就是把如何渲染html页面的权利交给了浏览器，有多少种浏览器就有多少种展示方式。因此要提高浏览器兼容性就必须重视。
html语义化
根据内容的结构选择合适的标签
优点
增加代码可读性，结构清晰，便于开发和维护
对机器友好，文字表现力丰富，有利于SEO。SEO(Search Engine Optimization)是搜索引擎优化，为了让用户在搜索和网站相关的关键词的时候，可以使网站在搜索引擎的排名尽量靠前，从而增加流量。
方便设备解析（如盲人阅读器等），可用于智能分析
在没有 CSS 样式下，页面也能呈现出很好地内容结构、代码结构
常见的语义化标签
title ：页面主体内容
header ： 页眉通常包括网站标志、主导航、全站链接以及搜索框。
nav ： 标记导航，仅对文档中重要的链接群使用。
section ： 定义文档中的节（section、区段）。比如章节、页眉、页脚或文档中的其他部分。
main，帮助到搜索引擎以及搜索工程师找到网站的主要内容，本身并不承载特殊的功能和意义。
article： 定义外部的内容，其中的内容独立于文档的其余部分。
aside ： 定义其所处内容之外的内容。如侧栏、文章的一组链接、广告、友情链接、相关产品列表等。
footer：页脚，只有当父级是body时，才是整个页面的页脚。
address： 作者、相关人士或组织的联系信息（电子邮件地址、指向联系信息页的链接）。
meta标签
meta标签用来描述一个HTML网页文档的属性，例如作者、日期和时间、网页描述、关键词、页面刷新等。
meta标签的作用有：搜索引擎优化（SEO），定义页面使用语言，自动刷新并指向新的页面，实现网页转换时的动态效果，控制页面缓冲，网页定级评价，控制网页显示的窗口等。
meta分类
1）页面描述信息(NAME)：常用的选项有Keywords(关键字) ，description(网站内容描述)，author(作者)，robots(机器人向导)等。
2）HTTP标题信息(HTTP-EQUIV)：可用于代替name项，常用的选项有Expires(期限)，Pragma(cache模式)，Refresh(刷新)，Set-Cookie(cookie设定)，Window-target(显示窗口的设定)，content-Type(显示字符集的设定)等。
3）content项：根据name项或http-equiv项的定义来决定此项填写什么样的字符串。
HTML5特性
新增
新的选择器 document.querySelector、document.querySelectorAll
媒体播放的 video 和 audio 标签
以前用的flash实现
本地存储 localStorage 和 sessionStorage
浏览器通知 Notifications
语义化标签，例如 header，nav，footer，section，article 等标签。
地理位置 Geolocation
鉴于隐私性，除非用户统一，否则不可获取用户地理位置信息
离线应用 manifest
全双工通信协议 websocket
浏览器历史对象 history
多任务处理 webworker
运行在后台的JS，独立于其他脚本，不影响性能
拖拽相关API
增强表单控件 url，date，time，email，calendar，search
页面可见性改变事件 visibilitychange
跨窗口通信 PostMessage
表单 FormData 对象
canvas+SVG
移除
纯表现的元素：basefont、big、center、font、 s、strike、tt、u
对可用性产生负面影响的元素：frame、frameset、noframes
src 和 href 的区别
src ⽤于替换当前元素，href ⽤于在当前⽂档和引⽤资源之间确⽴联系
一、src
src 是 source 的缩写，指向外部资源的位置，指向的内容将会嵌⼊到⽂档中当前标签所在位置；在请求 src 资源时会将其指向的资源下载并应⽤到⽂档内，例如 js 脚本，img 图⽚和 frame 等元素。
当浏览器解析到该元素时，浏览器会对这个文件进行解析，编译和执行，从而导致整个页面加载会被暂停，类似于将所指向资源嵌⼊当前标签内。这也是为什么将js 脚本放在底部⽽不是头部。
二、href
href 是 Hypertext Reference 的缩写，指向⽹络资源所在位置，建⽴和当前元素（锚点）或当前⽂档（链接）之间的链接，浏览器遇到 href 就会并⾏下载资源并且不会停⽌对当前⽂档的处理。 这也是为什么建议使⽤ link ⽅式来加载 css，⽽不是使⽤@import 。
三、总结来说
src 代表这个资源是必备的，必不可少的，最终会嵌入到页面中，而 href 是资源的链接
行内元素 和 块级元素有哪些
一、元素种类
1、行内元素
和其他元素都在一行上；
高，行高及外边距和内边距部分可改变；
宽度只与内容有关；
行内元素只能容纳文本或者其他行内元素。
不可以设置宽高，其宽度随着内容增加，高度随字体大小而改变，内联元素可以设置外边界，但是外边界不对上下起作用，只能对左右起作用，也可以设置内边界，但是内边界在 ie6 中不对上下起作用，只能对左右起作用
<a >
<strong>
<b>
<em>
<del>
<span >
<img> 
<input> 
<select>
2、块级元素
总是在新行上开始，占据一整行；
高度，行高以及外边距和内边距都可控制；
宽带始终是与浏览器宽度一样，与内容无关；
它可以容纳内联元素和其他块元素。
<h1>~<h6>
<p>
<div>
<ul>
<ol>
<li>
<div>
<dl>
3、空元素
<br> <hr> <img> <input> <link> <meta>
二、行内元素和块级元素的转换
//定义元素为块级元素
display：block 
//定义元素为行内元素
display : inline  
//定义元素为行
display：inline-block
三、块级元素和行内元素的区别
我们区分 块级元素 和 行内元素，首先行内元素是在一行中能有多个的，块级元素是自己占一行的。
接着可以从三个方面来查看
是否占据一行，还是能多个处于一行中，行内是可以的；
是否可以设置宽高，行内是不可以的。
行内元素只可以容纳文本和其他行内元素，块级元素啥都可以容纳
总结
行内元素和块级元素很好区分，顾名思义，行内就是能都在一行里的，一行可以有多个 < a > 标签 ，可以有多个 < input > 标签，而同类的还有 < span > / < img > / < strong > 等，这不就很容易记住了。而块级元素就是要自己占一行的，那不就有 < div > ，还有我们使用的列表 < ul > / < ol >，除此之外还有 < h1 >~< h6 > / < p > 等等。
link 与 @import 的区别
一、语法结构
//link
<link href="路径" rel="stylesheet" type="text/css" />

//import
@import url(路径地址);
二、区别
1、从属关系区别
@import是 CSS 提供的语法规则，只有导入样式表的作用；link是HTML提供的标签，不仅可以加载 CSS 文件，还可以定义 RSS、rel 连接属性等。
2、加载顺序区别
加载页面时，link标签引入会和 html 同时加载；而 @import 引入的 CSS 将在页面加载完毕后被加载。
3、兼容性区别
@import是 CSS2.1 才有的语法，可在 IE5+ 才能识别；link标签作为 HTML 元素，不存在兼容性问题。
4、DOM可控性区别
可以通过 JS 操作 DOM ，插入link标签来改变样式；由于 DOM 方法是基于文档的，无法使用@import的方式插入样式。
5、权重
link方式的样式权重高于@import的权重。
总的来说，使用 link 会比 @import 好，首先兼容性， link 作为 html 的标签是不会存在这个问题的。并且如果使用 @import 是在 dom 树渲染完才会进行渲染的，所以是不被 JavaScript 动态的修改的
常见的图片格式
图片格式	优点	缺点	使用场景
GIF	文件小，支持动画、透明，无兼容性问题	只支持256种颜色	色彩简单的logo、icon、动图
JPG	色彩丰富，文件小	有损压缩，反复保存图片质量下降明显	色彩丰富的图片/渐变图像
PNG	无损压缩，支持透明，简单图片尺寸小	不支持动画，色彩丰富的图片尺寸大	logo/icon/透明图
WEBP	文件小，支持有损和无损压缩，支持动画、透明	浏览器兼容性相对而言不好	支持webp格式的app和webview
iframe
iframe 元素 可以在一个网站里面嵌入另一个网站内容
优点
实现一个窗口同时加载多个第三方域名下内容
增加代码复用性
缺点：
搜索引擎无法识别
影响首页首屏加载时间
兼容性差
限制iframe访问另一个页面
设置X-Frame-Options 响应头 ——是否允许网页通过iframe 嵌套
deny：完全禁止任何网页嵌套
sameorigin：只允许同源域名访问
allow-from url：允许url的域名可嵌套
设置Content-Security-Policy
CSP，内容安全策略，限定网页允许加载的资源，防范XSS攻击
"Content-Security-Policy": "frame-ancestors 'self'"//限定iframe的嵌套
判断 window.top 页面顶级窗口和 自身窗口 window.self 是否相等，若不等则是嵌入了iframe
defer 和 async
defer和async是script标签的两个属性，用于在不阻塞页面文档解析的前提线下，控制脚本的下载和执行。
先了解一下页面的加载和渲染过程：
浏览器发送请求，获取HTML文档开始从上到下解析并构建DOM
构建DOM过程中，若遇到外联样式声明和脚本声明，会暂停文档解析，并开始下载样式脚本和文件
样式文件下载完成后，构建CSSDOM；脚本文件下载完成后，解析并执行，再继续解析文档构建DOM
文档解析完成后，将DOM和CSSDOM进行关联和映射，最后将视图渲染到浏览器窗口
注意，在上述过程中，脚本文件的下载和执行是和文档解析同步的，即它会阻塞文档的解析，若控制的不好，会影响用户体验，造成页面卡顿。
因此我们可以在script中声明defer和async这两个属性。
defer：用于开启新的线程下载脚本文件，并使脚本在文档解析完成后执行。 async：HTML5新增属性，用于异步下载脚本文件，下载完毕立即解释执行代码。
共同点
都是异步加载外部脚本文件
不会阻塞页面的解析
区别
async表示异步加载，表后续文档的加载和渲染与JS脚本加载和执行并行进行,脚本文件一旦加载完成，会立即执行，我们无法预测每个脚本的下载和执行时间顺序，谁先下载好谁执行。
defer表示延迟加载，加载后续文档和JS脚本加载（仅加载不执行)并行进行，JS脚本的执行需要等待文档所有元素解析完之后，load和DOMContentLoaded事件之前执行，有顺序而言。
