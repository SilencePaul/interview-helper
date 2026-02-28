Vue
Vue基础
MVVM
MVVM 是 Model-View-ViewModel 的缩写。MVVM 是一种设计思想。 Model 层代表数据模型，也可以在 Model 中定义数据修改和操作的业务逻辑; View 代表 UI 组件，它负责将数据模型转化成 UI 展现出来，View 是一个同步 View 和 Model 的对象 在 MVVM 架构下，View 和 Model 之间并没有直接的联系，而是通过 ViewModel 进行交互， Model 和 ViewModel 之间的交互是双向的， 因此 View 数据的变化会同步到 Model 中，而 Model 数据的变化也会立即反应到 View 上。 对 ViewModel 通过双向数据绑定把 View 层和 Model 层连接了起来，而 View 和 Model 之间的 同步工作完全是自动的，无需人为干涉，因此开发者只需关注业务逻辑，不需要手动操作 DOM，不需要关注数据状态的同步问题，复杂的数据状态维护完全由 MVVM 来统一管理。
Vue的优点和特点
一、优点
首先是双向绑定 这也是我们使用框架的一大优势，VUE使用MVVC架构，在 VUE.2X 中使用Object.definProperty () 来劫持绑定数据，在VUE.3X 中使用 Proxy 劫持。如果按照最初的开发，我们前端开发不仅仅是需要完成业务代码的实现，同时还需要对每个 DOM元素进行获取绑定时间和数据。而双向绑定使得我们只需要专注于业务代码的实现上。
简单易学 VUE以简单，易上手的特点，在国内很多企业得到使用。同时作为国人开发的框架，中文文档，相关的论坛，生态完善，也便于我们学习和遇到问题的解决方案。
虚拟DOM 使用虚拟DOM，结合DIFF 算法能减少性能损耗。他会把我们多次的操作合并为一次，推送到真实的DOM。另外补充，我们说虚拟DOM减少损耗是有条件，是指在频繁操作的情况下，不然肯定简单的获取操作最快的，期间没有很多计算等处理。
组件化的思想 实现组件的封装，我们往往是使用组件开发的思想去封装组件，这样不仅便于复用也好维护修改！
二、缺点
生态不够完善 相比 angular 和 react 来说，生态环境较为不足，在构建大型的应用方面 ，企业使用 react 的比较多。而中小型企业使用 VUE 比较多。
三、react与VUE的区别和优缺点
VUE 和 React 的共同点是，都是组件化的思想，虚拟DOM，数据绑定，而不同点在于，首先两者的设计思想不同，前者定位降低前端开发的门槛，而后者推崇函数式编程。另外在 React 中，是使用 JSX的写法，把HTML 和 CSS都写入到 JavaScript 中。还有的就是他们的 DIFF算法实现也不太一样。
v-show 和 v-if 的区别
1、本质上
v-show 是把标签里的 display 设置为 none，所以页面上是可见的
v-if 是动态的操作DOM元素，页面上不可见的
2、性能上
要是需要频繁的操作的话，肯定是 v-show ，因为他只是操作css的值，不会频繁触发重排。但是 v-if 是不断的向 DOM树添加或删除元素，在比较少改变的时候比较合适。
v-show 无论任何条件，初始都会渲染，v-if是惰性的，如果初始条件为 false，初始不会渲染 DOM ，为 true 才会渲染。因此 v-if 有更高的切换开销，而 v-show 有更高的初始渲染开销
v-if 和 v-for 为什么不建议一起使用呢
v-if：根据表达式的真值来有条件的渲染元素，在切换时元素及它的数据绑定 / 组件被销毁并重建。
v-for：基于源数据多次渲染元素或模板块。此指令之值，必须使用特定语法 alias in expression，为当前遍历的元素提供别名，同时设置 独一无二的 key 。
我们有时候会写出下面的例子：
<div id="app">
    <p v-if="isShow" v-for="item in items">
        {{ item.title }}
    </p>
</div>
而实际上这段代码会先循环然后再进行判断，每次v-for都会执行v-if，造成不必要的计算，这会带来性能上的浪费。避免这种使用在同一个元素的情况，我们可以在外层嵌套template（页面渲染不生成dom节点），在这一层进行v-if判断，然后在内部进行v-for循环
<template v-if="isShow">
    <p v-for="item in items">
</template>
如果条件出现在循环内部，可通过计算属性computed提前过滤掉那些不需要显示的项。
<div>
	<div v-for="(user,index) in activeUsers" :key="user.index" >
		{{ user.name }} 
	</div>
</div>

data () {  
    return {
      users,: [{
        name: '1',
        isShow: true
      }, {
        name: '2',
        isShow: true
      },{
        name: '3',
        isShow: false
      }]
    }
  }
  
computed: {
	activeUsers: function () {
		return this.users.filter(function (user) {
			return user.isShow;//返回isShow=true的项，添加到activeUsers数组
		})
	}
}
总结
首先，两者的作用分别是 v-if 是根据真值来判断是否渲染组件，而 v-for 是循环渲染组件列表。之所以不能一起使用是因为 v-for 的优先级 比 v-if 高。
这会导致的情况就是，当我们在一个循环列表中做判断时，他会先全部列表渲染出来，然后再根据判断做销毁，这会造成不必要的浪费，就是做好了，多出来的砸坏。一般我们可通过计算属性对数据做过滤，把不必要的数据过滤掉，就不必使用 v-if 。
如果使用v-show就不一样了，v-show 和 v-if 的区别在于v-show 是通过display属性设置为 none 来隐藏属性的，而 v- if 是销毁 DOM上的元素的，所以如果同时使用 v-show 和 v-for 是没有影响的。
双向数据绑定的原理
Vue2.x 采用数据劫持结合发布订阅模式（PubSub 模式）的方式，通过 Object.defineProperty 来劫持各个属性的 setter、getter，在数据变动时发布消息给订阅者，触发相应的监听回调。
当把一个普通 Javascript 对象传给 Vue 实例来作为它的 data 选项时，Vue 将遍历它的属性，用 Object.defineProperty 将它们转为 getter/setter。用户看不到 getter/setter，但是在内部它们让 Vue 追踪依赖，在属性被访问和修改时通知变化。
Vue 的数据双向绑定整合了 Observer，Compile 和 Watcher 三者，通过 Observer 来监听自己的 model 的数据变化，通过 Compile 来解析编译模板指令，最终利用 Watcher 搭起 Observer 和 Compile 之间的通信桥梁，达到数据变化->视图更新，视图交互变化（例如 input 操作）->数据 model 变更的双向绑定效果。
Vue3.x 放弃了 Object.defineProperty ，使用 ES6 原生的 Proxy，来解决以前使用 Object.defineProperty 所存在的一些问题。
computed 和 watch 的区别
一、这两者解决的问题
当我们的数据发生改变的时候，所有和该数据有关的数据都自动更新，执行我们定义的方法。不同于 methods 是需要相关的方法和交互来实现调用执行的。
二、computed 和 watch 以及 methods 的区别
1、性质上 methods ：定义函数，手动调用 computed：计算属性，return 返回结果，自动调用 watch： 观察，监听，发生改变就调用
2、使用场景 methods ：一般不处理数据的逻辑，用于获取数据，和改变状态等情况 computed：多用于一个数据受多个数据影响的情况，具有 缓存的特性，避免每次重新计算 watch： 多用于一个数据影响多个数据的情况，且类似异步等情况的时候建议使用
3、执行时间 computed 和 methods 的初始化是在 beforeCreated 和 created 之间完成的。（以及Props, data都是）
4、缓存 computed：有缓存，重新渲染时，要是值没有改变，会直接返回之前的 watch：无缓存，重新渲染时，要是值没有改变，也会执行
5、是否异步 computed：不支持异步，但异步监听的时候，无法监听数据变化 watch：支持异步监听
三、computed 和 methods 的区别
无论是定义为一个计算属性还是一个函数方法，对于结果来说都是一样的，不同点在于，计算属性是根据依赖值变化才发生改变，而函数方法需要调用执行。
Vue中的插槽使用
在开发中，往往会把一个复杂的页面分为多个组件去组合，或者当复用性比较高的也会提取为一个组件，但是当我们设计的组件还不能在某些特殊的情况满足我们的需求的时候，我们还需要添加额外的时候，那么该怎么办呢？插槽就出现了。
当实际使用的组件不能完全的满足我们的需求的时候，我们就可以用插槽来分发内容，往我们的这个组件中添加一点东西。
基本的使用就是在子组件里面我们需要添加内容的地方加上
<slot></slot>
那么我们在父组件中使用该子组件的时候，就能直接在这个子组件中添加进入内容。这就是最基本的使用。
那么要是我们想在父组件中传递多个内容呢？这时候就有我们的对应使用的具名插槽了，我们可以对插槽命名狮子对应在子组件中的位置。
//我们可以在子组件的插槽中写入内容，也就是默认值，当我们在父组件中没有传递值的时候，就会使用默认值
<slot>我是默认的插槽值</slot>

//具名插槽
如下，我们在子组件中的插槽可以命名，这样我们在父组件中可以通过名字来确定位置

 //子组件B
    const BBorder = {
        template: `<div>我是儿子B       
        <slot name= 'header'> 这里是头部</slot>
        <slot> 这里是默认 </slot>
        <slot name='footer'> 这里是尾部 </slot></div>`,
    }
    const Parents = {
        methods: {
        },
        //实例化BBorder这个子组件
        template: `<div>我是父组件:{{msg}}
            <BBorder>
                <template v-slot:header> 头部 </template>
                <p>A 9999999999999</p>
                <template v-slot:footer> 尾部 </template>
            </BBorder>
            </div>`,
        //注册两个子组件
        components: {
            BBorder
        }
    }
同样的，也能出传递值给到父组件中，但是我么要注意，父子组件的编译作用域是不同的，父级模板里的所有内容都是在父级作用域中编译的；子模板里的所有内容都是在子作用域中编译的。
从子组件中传递值到父组件
//子组件中
  <slot :user="user">
    {{ user.lastName }}
  </slot>

//父组件中
<current-user>
  <template v-slot:default="slotProps">
    {{ slotProps.user.firstName }}
  </template>
</current-user>
Vue中的key
关于 key ，我们常常在 v-for 中会接触到，当我们需要进行列表循环的时候，如果没有使用 key ，就会有警报提示。
//场景一：循环列表
<div v-for="num in numbers" :key="index">
  {{num}}
</div>
//场景二：通过时间戳强制重新渲染
<div :key="+new Date()" >+new Date()</div>
那么为什么需要 key呢？
因为使用 key 相当于给 vnode 添加上一个唯一的 id，主要是在 DOM DIFF算法中使用的下面我们看个例子：
如果上面的场景一 items 的值为 [1,2,3,4,5,6,7,8,9,10] 那么就是渲染出十个div 是吧。如果没有 key ，那么当我们现在 items 的值变为 [0,1,2,3,4,5,6,7,8,9] 呢，那么机会第一个原来是 “1” 的 div内容变为“0”，而原来是“2”的div内容变为“1”…以此类推。（因为没有key属性，Vue无法跟踪每个节点，使用的是“就地复用” 得策略，通过这样的方法来完成变更） 但是如果key的情况下，Vue能跟踪每个节点，就会直接新增一个 div 添加到内容是“1”的div前面。根据key，更准确， 更快的找到对应的vnode节点。 设置key能够大大减少对页面的DOM操作，提高了diff效率，更加的高效更新虚拟DOM
还有的用途就是我们的场景二 用来强制替换元素，当key改变时，Vue认为一个新的元素产生了，从而会新插入一个元素来替换掉原有的元素。所以上面的元素会被删除而而重新添加。但是如果没有添加 key的话，就会直接替换div 里面的内容。而不是删除添加元素。
注意点
尽量不要使用索引 index 做 key 的值，要使用唯一的标识值，比如 id 之类的，因为如果使用数组索引 index 为 key，当向数组中指定位置插入一个新元素后，因为这时候会重新更新 index索引，对应着后面的虚拟DOM的 key 值全部更新了，这时候做的更新是没有必要的，就像没有加key一样，因此index虽然能够解决key不冲突的问题，但是并不能解决复用的情况。如果没有唯一ID的情况下，可以使用用组件的uid拼接index的形式，因为uid是唯一的 。或者生成一个时间戳~。
总结
关于在 v-for 中使用 key 是因为使用 key 相当于给节点添加上一个唯一的 id，在 DOM DIFF算法中能更高效的更新虚拟DOM。
当没有使用的时候，如果我们需要对一个循环渲染的列表插入一个，那么实际上会 “就地复用” 的策略，比如我们需要在最前面插入一个，那么就会后面的全部往后变更，发生多次DOM操作，这是因为 Vue无法跟踪每个节点，而使用 key 后，节点标识，定位到最前面，然后插入修改，只发生一次DOM操作，大大优化了性能。
Vue过滤器
定义过滤器有两种常见的方式: 双花括号插值和 v-bind 表达式
<!-- 在双花括号中 -->
{{ message | capitalize }}

<!-- 在 `v-bind` 中 -->
<div v-bind:id="rawId | formatId"></div>
其实一般用来格式文本，比如我们往往拿到的时间是时间戳，那么就可以很简单的通过过滤器来格式成我们常见的格式。
使用上的我们先要定义过滤的方法，这个可以全局定义或者组件内定义
//组件内定义
filters: {
  capitalize: function (value) {
    if (!value) return ''
    value = value.toString()
    return value.charAt(0).toUpperCase() + value.slice(1)
  }
}
//全局定义
Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

new Vue({
  // ...
})
Vue中Scoped原理
Vue的作用域样式 Scoped CSS 的实现思路如下：
为每个组件实例生成一个能唯一标识组件实例的标识符，记作 InstanceID；
给组件模板中的每一个标签对应的 Dom 元素添加一个标签属性，格式为 data-v-实例标识（示例：< div data-v-e0f690c0=“” >）；
给组件的作用域样式 < style scoped> 的每一个选择器的最后一个选择器单元增加一个属性选择器
特点
1、 将组件的样式的作用范围限制在了组件自身的标签
即：组件内部，包含子组件的根标签，但不包含子组件的除根标签之外的其它标签；所以 组件的 css 选择器也不能选择到子组件及后代组件的中的元素（子组件的根元素除外）；
因为它给选择器的最后一个选择器单元增加了属性选择器 [data-v-实例标识] ，而该属性选择器只能选中当前组件模板中的标签；而对于子组件，只有根元素 即有 能代表子组件的标签属性 data-v-子实例标识，又有能代表当前组件（父组件）的 签属性 data-v-父实例标识，子组件的其它非根元素，仅有能代表子组件的标签属性 data-v-子实例标识；
2、 如果递归组件有后代选择器，则该选择器会打破特性1中所说的子组件限制，从而选中递归子组件的中元素；
原因：假设递归组件A的作用域样式中有选择器有后代选择器 div p ，则在每次递归中都会为本次递归创建新的组件实例，同时也会为该实例生成对应的选择器 div p[data-v-当前递归组件实例的实例标识]，对于递归组件的除了第一个递归实例之外的所有递归实例来说，虽然 div p[data-v-当前递归组件实例的实例标识] 不会选中子组件实例（递归子组件的实例）中的 p 元素（具体原因已在特性1中讲解），但是它会选中当前组件实例中所有的 p 元素，因为 父组件实例（递归父组件的实例）中有匹配的 div 元素；
Vue中的ref
ref
常用来辅助开发者，获取 DOM 元素或组件的引用，以及用于在父子组件中获取对方的某个元素进行取值，调用方法等。
在每个 Vue 的组件实例上， 都包含一个 $refs 对象， 里面存储着对应的 DOM 元素或组件的引用
默认情况下，组件的 $refs 指向一个空对象
如果想要使用 ref 引用页面上的组件实例，则可以按照如下方式：
使用ref属性，为对应的组件添加引用名称
<my-counter ref="counterRef"></my-counter>
<button @click="getRef">获取 $refs 引用</button>
methods: {
  getRef(){
    // 通过 this.$refs. 引用的名称，可以引用组件的实例
    console.log(this.$refs.counterRef)
    // 引用到组件的实例之后，就可以调用组件上的methods方法
    this.$refs.counterRef.add()
  }
}
这个方法可以说很便利，但是不要太依赖了，往往在不能通过其他方法获取的时候回才比较建议使用，毕竟我们因该尽量
减少添加，而是复用可以复用的部分。
$refs 只会在组件渲染完成之后生效，并且不是响应式的。这仅作为一个用于直接操作子组件的“逃生舱”——你应该避免在模板或计算属性中访问 tip：如果获取不到的时候，可以试一试使用nextTick
Vue中$nextTick的使用
$nextTick
官方解释：在下次 DOM 更新循环结束之后执行延迟回调。在修改数据之后立即使用这个方法，获取更新后的 DOM。
因为 vue 中不是数据一发生改变就马上更新视图层的，如果这样会带来比较差的性能优化，而是在 vue 中会添加到任务队列中，待执行栈的任务处理完才执行。所以 vue 中我们改变数据时不会立即触发视图，但是如果我们需要实时获取到最新的DOM，这个时候可以手动调用 nextTick。
Vue中的keep-alive
用 keep-alive 包裹组件时，会缓存不活动的组件实例，而不是销毁，使得我们返回的时候能重新激活。keep-alive 主要用于保存组件状态或避免重复创建。避免重复渲染导致的性能问题。
常见场景 页面的缓存，如上面的，保存浏览商品页的滚动条位置，筛选信息等
注意 这个 keep-alive 和 这个 Connection: Keep-Alive 是不一样的，这个属性的作用是，往往我们三次握手后，传输完数据就会断开连接进行四次挥手，关闭TCP连接，但是当我们在头信息中加入了该属性，那么TCP会在发送后仍然保持打开状态，这样浏览器就可以继续通过同一个TCP连接发送请求，保持TCP连接可以省去下次请求时需要建立连接的时间，提升资源加载速度。
data为什么是函数
组件中的 data 写成一个函数，数据以函数返回值形式定义。这样每复用一次组件，就会返回一份新的 data，类似于给每个组件实例创建一个私有的数据空间，让各个组件实例维护各自的数据。而单纯的写成对象形式，就使得所有组件实例共用了一份 data，就会造成一个变了全都会变的结果。
组件
组件生命周期
一、各个生命周期的作用
首先在 vue 生命周期中有 十个阶段：
1、beforeCreate（创建前）
在实例初始化之后,进行数据侦听和事件/侦听器的配置之前同步调用。
因为 data 和 methods 中的数据都还没有初始化，常常在该阶段执行与 vue 数据无关的事件，比如我们的 loading 等待事件。
2、created（创建后）
在实例创建完成后被立即同步调用。在这一步中，实例已完成对选项的处理，意味着以下内容已被配置完毕：数据侦听、计算属性、方法、事件/侦听器的回调函数。然而，挂载阶段还没开始，且 $el property 目前尚不可用。
在该阶段已经完成 data 和 methods 的初始化了，只是页面还未渲染，可以在该阶段来发起请求获取数据等，以及操作 data 和 调用 methods 等
3、beforeMount（挂载前）
在挂载开始之前被调用：相关的 render 函数首次被调用。 该钩子在服务器端渲染期间不被调用
4、mounted（挂载后）
实例被挂载后调用，这时 el 被新创建的 vm.$ el 替换了。如果根实例挂载到了一个文档内的元素上，当 mounted 被调用时 vm.$ el 也在文档内。 注意 mounted 不会保证所有的子组件也都被挂载完成。如果你希望等到整个视图都渲染完毕再执行某些操作，可以在 mounted 内部使用 vm.$nextTick 该钩子在服务器端渲染期间不被调用
这时候 vue实例完成初始化，且挂载渲染到页面了，最早我们可以在这个阶段来操作 页面上的 DOM节点。
5、beforeUpdate（更新前）
在数据发生改变后，DOM 被更新之前被调用。这里适合在现有 DOM 将要被更新之前访问它，比如移除手动添加的事件监听器。 该钩子在服务器端渲染期间不被调用，因为只有初次渲染会在服务器端进行
该阶段此时实例中的数据已经是最新的啦，但是页面的还未更新
6、update（更新后）
在数据更改导致的虚拟 DOM 重新渲染和更新完毕之后被调用。 当这个钩子被调用时，组件 DOM 已经更新，所以你现在可以执行依赖于 DOM 的操作。然而在大多数情况下，你应该避免在此期间更改状态。如果要相应状态改变，通常最好使用计算属性或 watcher 取而代之。 注意，updated 不会保证所有的子组件也都被重新渲染完毕。如果你希望等到整个视图都渲染完毕，可以在 updated 里使用 vm.$nextTick 该钩子在服务器端渲染期间不被调用
避免在这个阶段更改状态的，因为这样可能会导致更新无限循环，曾经我做过个获取表格的高度，如果页面大小发送改变就更新表格的大小，在该阶段执行导致了页面的无限循环，结果死机啦~
7、activated（激活前）
被 keep-alive 缓存的组件激活时调用。 该钩子在服务器端渲染期间不被调用
8、deactivated（激活后） 
被 keep-alive 缓存的组件失活时调用。 该钩子在服务器端渲染期间不被调用
9、beforeDestory（销毁前） 
实例销毁之前调用。在这一步，实例仍然完全可用。 该钩子在服务器端渲染期间不被调用
10、destoryed（销毁后） 
实例销毁后调用。该钩子被调用后，对应 Vue 实例的所有指令都被解绑，所有的事件监听器被移除，所有的子实例也都被销毁。 该钩子在服务器端渲染期间不被调用
总结
Vue 的生命周期也就是 Vue实例从创建到销毁的过程，总共分为8个阶段 创建前/后，载入前和后，更新前和后，销毁前和后。
创建前和后：
在 beforeCreated 阶段，Vue 实例刚在内存中被创建出来，data 和 methods 还未初始化，都为 undefined
在 created 阶段，vue实例的 data 和 methods 就已经存在了，但是DOM 还未挂载渲染
载入前和后：
在 beforeMount 阶段，DOM挂载完成，数据也初始化完成，但是数据的双向绑定还是显示{{}}，这是因为 Vue采用了Virtual DOM（虚拟Dom）技术。先占住了一个坑
在 mounted 阶段，DOM挂载完成，上一个阶段留的萝卜坑也补上了
更新前/后：
在 beforeUpdate 阶段，此时实例中的 data 以及是最新的了，但是界面上显示的数据还是旧的，此时还没有开始重新渲染DOM节点
在 update 阶段，此时实例中的 data 和界面上显示的数据都是新的了，已经完成了 DOM节点 的渲染
销毁前/后：
在 beforeDestroy 阶段， Vue实例销毁之前调用。在这一步，实例仍然完全可用。
在 beforeDestroy 阶段 ，Vue实例所有的事件监听以及和 dom的绑定都解除了
Vue中实现组件通信的方式
在VUE中实现通信有很多种的方式，每一种都有其对应的使用情况。
首先我们看看有哪些方式：
props
emit
v-model
refs
provide/inject
eventBus
vuex/pinia(状态管理工具)
常见的是上面的这几种，少见的其实还可以算上插槽 slot， 混入，路由携带参数，localStorage， $parent / $children等
1. props 常常使用在父组件传递給子组件通信的过程中，首先在子组件中使用 props，来接收对应的属性，而在父组件中使用子组件的地方，添加上面定义的属性。
2. emit 这个就和上面的相反，是使用在子组件给父组件传递值的中。子组件中声明对应的事件，当子组件触发事件，就会通过 this.$emit(‘事件’ , ‘数据’)传递到，而在父组件中使用子组件的地方，添加上面定义的事件，这个可以获取子组件传来的值。
3. provide/inject 这对组合往往使用在层级比较深的时候，比如A组件下可能还有 B组件 ，B组件下有C组件…E组件.而使用这对 API，就能无论层级有多深都能获取到
4. eventBus
也就是事件总线，简单粗暴，可以到处飞。可以不管你是不是父子关系，通过新建一个Vue事件bus对象，然后通过 bus.emit 触发事件，bus.on 监听触发的事件。但不建议乱用，不好维护。
5. vuex 对于大型的项目来说往往是很必要的，尤其单页面应用，很多页面嵌套页面，关系很多。而使用 VUEX 就能便捷的统一管理。
总结
常见的组件通信方式有通过 props / emit / provide 和 inject / eventBus / vuex 等，一般根据不同的场景来决定使用的方式。比如父子组件通信使用 props ，反过来使用 emit 。而当层级很多的时候使用 provide ，全局的状态管理使用 vuex等。
Vue事件总线（EventBus）
简单来说，我们知道Vue中有多种的方式来父子组件传值
父传子：props
子传父：this.$emit(‘事件’ , ‘数据’)
兄弟组件：中间事件总线思想（也叫事件巴士）
多层级：父组件中使用 provide ，在子组件中使用 inject
今天我们要来讲的就是事件总线这个，简单来说，它的使用就是首先创建事件总线
//两种方式，一种是创建一个单独的文件如下面的的bus.js在用到的地方导入，
//还有中就是在项目的main中实例化

// bus.js
import Vue from 'vue'
export const EventBus = new Vue()

// main.js
Vue.prototype.$EventBus = new Vue()
创建好之后我们就很简单啦
//在需要发送事件的地方用通过 this.$emit(‘事件’ , ‘数据’)来发送
//在需要接收的地方用xxx.$on('事件',(数据)=>{ })来接收
//下面是一个完整的例子

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<div id="app">
    <Parents></Parents>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
    //创建一个媒介来连通两个是组件
    const medium = new  Vue()

    const ABorder = {
        template: `<div>我是儿子A
        <div>我的名字叫：{{name}}</div>
        <button @click="newName">给自己命名</button>
        </div>`,
        created () {
            medium.$on('letDiscussionName',(val)=>{
              alert(val)
            })
        },
        //用props来接收父组件传来的值，同时父组件要绑定属性
        props: {
            name:{
                //设置类型，符合才接收
                type: String,
                //不传默认为这个
                default: '我也不知道呀'
            }
        },
        methods: {
          newName() {
              this.$emit('newName','大黄狗')
          }
        }
    };
    const BBorder = {
        template: `<div>我是儿子B
                    <button @click="discussionName">讨论</button>
                   </div>`,
        methods: {
            discussionName() {
                medium.$emit('letDiscussionName','儿子A来讨论')
            }
        }
    }

    const Parents = {
        data() {
            return {
                msg: '孩儿们好呀！',
                aName: '大花猫',
                bName: '大黄狗'
            }
        },
        methods: {
            chang(value) {
                this.aName = value
            }
        },
        //可以有下面两种形式来调用组件
        template: `<div>我是父组件:{{msg}}
        <hr/>
        <a-border :name= 'this.aName'  @newName = 'chang'></a-border>
        <hr/>
        <BBorder></BBorder></div>`,
        components: {
            ABorder,
            BBorder
        }
    }
    //实例化一个vue，并且绑定到app这个元素
    const vm = new Vue({
        el: '#app',
        components: {
            Parents,
        }
    })
</script>
</body>
</html>
Vue-router
一、路由常见的属性
路由的两个属性$router和$route。
$router
$router.app
$router.mode
$router.currentRoute
router.addRoutes(routes)
router.beforeEach(to,from,next)
router.afterEach()
router.go(n)
router.push( location )
router.replace( location )
router.back()
router.forward()
router.resolve(location)
router.onReady(callback,[errorCallback]){}
router.onError(callback)
$route
$route.path
$route.query
$route.params
$route.hash
$route.fullPath
$route.name
$route.matched
$route.redirectedFrom
Vue-router中hash模式和history模式的区别
最明显的是在显示上，hash模式的URL中会夹杂着#号，而history没有。
Vue底层对它们的实现方式不同。hash模式是依靠onhashchange事件(监听location.hash的改变)，而history模式是主要是依靠的HTML5 history中新增的两个方法，pushState()可以改变url地址且不会发送请求，replaceState()可以读取历史记录栈,还可以对浏览器记录进行修改。
当真正需要通过URL向后端发送HTTP请求的时候，比如常见的用户手动输入URL后回车，或者是刷新(重启)浏览器，这时候history模式需要后端的支持。因为history模式下，前端的URL必须和实际向后端发送请求的URL一致，例如有一个URL是带有-路径path的(例如www.lindaidai.wang/blogs/id)，如果后端没有对这个路径做处理的话，就会返回404错误。所以需要后端增加一个覆盖所有情况的候选资源，一般会配合前端给出的一个404页面
Vue路由传参
路由传参方式可划分为 params 传参和 query 传参，而 params 传参又可分为在 url 中显示参数和不显示参数两种方式
方式A：这种需要在路由配置好可以传递参数XXX的，不是最方便的
路由配置
{
 path: '/child/:XXX',
 component: Child
}
父组件
<router-link to = "/child/XXX"></router-link>
子组件读取
this.num = this.$route.params.XXX
方式B：这种同样需要在路由配置好可以传递参数XXX的，不过是用到push方法的
路由配置
{
 path: '/child/:XXX',
 component: Child
}
父组件
this.$router.push({
        path: `/child/${XXX}`
      })
子组件读取
this.num = this.$route.params.XXX
上面两种方式都会在地址显示出传递的参数，类似get请求
方式C：这种不需要在路由配置好根据路由的名称，需要保持一致
路由配置
不需要配置，但是子组件的name必须与父组件传递的路由一致
父组件
this.$router.push({
        name: 'B',
        params: {
          XXX: '妈呀'
        }
      })
子组件读取
this.num = this.$route.params.XXX  //妈呀
方式D：这种不需要在路由配置好根据路由的名称，通过query来传递
路由配置
不需要配置，但是子组件的name必须与父组件传递的路由一致{
父组件
this.$router.push({
        path: '/child',
        query: {
            XXX: '妈呀'
        }
      })
子组件读取
this.num = this.$route.query.XXX
总的来说使用方式C和D最为多，毕竟不需要对路由配置做修改
前端路由
把不同路由对应不同内容或页面的任务交给前端来做，之前通过服务端根据 url 的不同返回不同的页面实现
前端路由实质上就是检测 URL 的变动，截获 URL 地址，通过解析、匹配路由规定实现 UI 更新
单页面应用中的路由分为hash和history模式
hash模式
监听浏览器地址hash值变化，执行事件
hash会在浏览器URL后增加 # 号
一个完整的的 URL 包含：协定、域名、端口、虚拟目录、文件名、参数、锚
比如 https://www.google.com/#abc中的hash值为abc 特点：hash的变化不会刷新页面，也不会发送给服务器
但hash的变化会被浏览器记录下来，来指导浏览器中的前进和后退
window.location.hash变化触发窗口onhashchange事件，监听hash变化
触发路由时视图容器更新——多数前端框架哈希路由的实现原理
触发hashchange的情况
URL变化(包括浏览器的前进、后退)修改window.location.hash
浏览器发送http://www.baidu.com/ 至服务器，请求完毕后设置散列值为#/home
只修改hash部分，不发请求
a标签可设置页面hash，浏览器自动设置hash
window.location.hash='abc';
let {hash}=window.location
window.addEventListener('hashchange',function(){
    //监听hash变化
})
特点
兼容性好
路径在#后面，不好看
history模式
H5新特性，允许直接修改前端路由，更新URL但不重新发请求，history可自定义地址
window.history属性指向 History 对象，表示当前窗口的浏览历史，保存了当前窗口访问过的所有页面网址
由于安全原因，浏览器不允许脚本读取这些地址，但允许在地址间导航
// 后退到前一个网址
history.back()

// 等同于
history.go(-1)
浏览器工具栏的“前进”和“后退”按钮，就是对 History 对象进行操作 History 对象主要有两个属性
History.length：当前窗口访问过的网址数量（包括当前网页）
History.state：History 堆栈最上层的状态值（详见下文）
// 当前窗口访问过多少个网页
window.history.length 
// History 对象的当前状态
// 通常是 undefined
window.history.state
history.back()、history.forward()、history.go()
用于在历史之中移动
History.back()：移动到上一个网址，等于点击浏览器后退键。对于第一个访问的网址，该方法无效
History.forward()：移动到下一个网址，等于点击浏览器前进键。对于最后一个访问的网址，该方法无效果
History.go()：接受一个整数作为参数，以当前网址为基准，移动到参数指定的网址，go(1)相当于forward()，go(-1)相当于back()。如果参数超过实际存在的网址范围，该方法无效；如果不指定参数，默认0，相当于刷新页面
history.pushState()
在历史中添加一条记录，不会导致页面刷新
window.history.pushState(state, title, url)
state：对象，触发popstate事件将该对象传递到新页面。不需要可以填null
title：新页面标题。但现在所有浏览器都忽视这个参数，所以可以填空串
url：新网址，必须与当前页面在同域。地址栏将显示这个网址
假定当前网址是example.com/1.html，使用pushState()在浏览记录（History 对象）中添加一个新记录
var stateObj = { foo: 'bar' };
history.pushState(stateObj, 'page 2', '2.html');
添加新记录后，浏览器地址栏显示example.com/2.html，但不会跳转到2.html，也不会检查2.html是否存在，它只是成为浏览历史的最新记录。这时，在地址栏输入一个新的地址(如访问google.com)，然后点击倒退按钮，页面的 URL 将显示2.html；再点击一次倒退，URL 将显示1.html
pushState()不触发页面刷新，只导致 History 对象变化，地址栏有反应 使用该方法后，可以用History.state读出状态对象
var stateObj = { foo: 'bar' };
history.pushState(stateObj, 'page 2', '2.html');
history.state // {foo: "bar"}
如果pushState的 URL 参数设置了一个新的锚点值（即hash），不会触发hashchange事件。反过来，如果 URL 的锚点值变了，会在 History 对象创建一条浏览记录 如果pushState()方法设置了一个跨域网址，报错
// 报错
// 当前网址为 http://example.com
history.pushState(null, '', 'https://twitter.com/hello');
pushState想要插入一个跨域的网址，导致报错。防止恶意代码让用户以为他们是在另一个网站上，因为这个方法不会导致页面跳转
history.replaceState()
修改 History 当前记录，其他与pushState()一模一样
假定当前网页是example.com/example.html
history.pushState({page: 1}, 'title 1', '?page=1')
// URL 显示为 http://example.com/example.html?page=1

history.pushState({page: 2}, 'title 2', '?page=2');
// URL 显示为 http://example.com/example.html?page=2

history.replaceState({page: 3}, 'title 3', '?page=3');
// URL 显示为 http://example.com/example.html?page=3

history.back()
// URL 显示为 http://example.com/example.html?page=1

history.back()
// URL 显示为 http://example.com/example.html

history.go(2)
// URL 显示为 http://example.com/example.html?page=3
popstate事件
当同一个文档的浏览历史变化触发popstate 注意
仅调用pushState()/replaceState()，不会触发
只有点击浏览器倒退/前进，或调用History.back()、History.forward()、History.go()才会触发
只针对同一个文档，如果浏览历史切换，导致加载不同文档，不会触发
popstate指定回调函数
window.onpopstate = function (event) {
    console.log('location: ' + document.location);
    console.log('state: ' + JSON.stringify(event.state));
};

// 或者
window.addEventListener('popstate', function (event) {
    console.log('location: ' + document.location);
    console.log('state: ' + JSON.stringify(event.state));
});
回调函数参数event事件对象，它的state指向当前状态对象，这个state也可以通过history对象读取
var currentState = history.state;
页面第一次加载不会触发popstate事件
特点
路径正规
兼容性不比hash，需服务端支持
对于一个应用而言，url 的改变(不包括 hash 值改变)只能由下面三种情况引起：
点击浏览器的前进或后退按钮 => 可以监听popstate事件
点击 a 标签
JS 触发 history.pushState()、history.replaceState()
Vuex
一、Vuex是什么
Vuex 是一个专为 Vue.js 应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。
也就是说，vuex是基于 vue 框架的一个状态管理库，那么什么是状态管理呢？
状态管理模式：简单来说就是集中式的存储管理组件的状态思想
二、Vuex 解决了什么
我们思考一个场景：
比如我们有一个在线多人聊天的，类似微信的，我们有一个通知栏来告诉用户是否有未读信息，但是出现了通知栏偶尔会给出错误的通知，也就是用户收到一条新的未读消息的通知，但是当他们检查它是什么时，这只是他们已经看到的消息。
这是为什么呢？因为这里面
多个组件 / 实例依赖于同一状态，兄弟组件之间的状态是无法传递。
并且来自不同视图的行为当需要变更同一状态的时候， 经常需要通过事件等来变更和同步状态，当遗漏的时候就会出现有些地方状态更新错误。
var Vo= {}

var A = new Vue({
  data: Vo
})

var B = new Vue({
  data: Vo
})
比如某个数据，在实例A和实例B中使用了，而这个数据在实例A中修改了，如果我们不做处理，这个状态是不会更新到实例B中的，对于实例B来说，这个数据是没有发生改变的。小型的项目我们还比较好处理，对实例B更新就好了。
但是，当我们在做大型的开发的时候的话，往往会有多个实例 / 组件（A，B，C，D…）共享 一个数据，这种情况它们之间互相关联，导致数据的复杂性大大增加，数据的状态变得不可预测或难以理解。结果就是应用程序变得无法扩展或维护，变得臃肿难以维护及复用
所以我们需要使用 vuex 统一的管理（思想是实现 Flux 模式），不必考虑各处的处理，只需要考虑一个，且具有下面的优点：
全局管理
状态变更跟踪
规范化
便于调试
Flux 模式的基本思想:
单一数据来源
数据是只读的
更新是同步的
二、Vuex 的好处
首先多层嵌套的组件、兄弟组件间的状态会更好管理维护，且使用 vuex 也是组件通信中的一种
减轻服务端压力，对于同一份数据集，请求会缓存，所有共用
当一个项目比较大型的时候，这是便于团队之间开发和维护的，和便于调试
二、五个核心的概念 state / getters / mutations / action / modules
在 Vuex 中，核心就是 一个 “store” 仓库，包含我们应用中的大部分状态，同时提供包含 state / getters / mutations / action / modules等在内的管理调用方法。
1、state state 的存储状态类似于就组件中data，是我们所有的集中数据的地方，访问 “store” 的状态可以使用两种方式 ，通过 this.$store.state属性 的方式或者 mapState 辅助函数。
//存储
 const store = new Vuex.Store({
  // 存储状态数据
  state: {
      count: 0,
      info:{
          name:"wenmo",
          age:18
      }
  },
)
//读取方式
 computed: {
    count () {
      return store.state.count
    }
  }

//下面这种是全局注册了store的
 computed: {
    count () {
      return this.$store.state.count
    }
  }
每当 store.state.count 变化的时候, 都会重新求取计算属性，并且触发更新相关联的 DOM。
辅助函数 mapState：当一个组件需要获取多个状态的时候，将这些状态都声明为计算属性会有些重复和冗余
computed: {
  // 使用对象展开运算符将此对象混入到外部对象中
  ...mapState({
    // ...
  })
}
2、getters getters 就是类似组件中的计算属性，可以简单理解为 state 的计算属性，依赖于 state 的值，state 发生改变就会同时改变
const store = new Vuex.Store({
  state: {
    todos: [
      { id: 1, text: '...', done: true },
      { id: 2, text: '...', done: false }
    ]
  },
  getters: {
    doneTodos: state => {
      return state.todos.filter(todo => todo.done)
    }
  }
})
3、mutations
mutations的作用是用来修改 “store” 里面的值，并且是唯一的方式。
我们不能直接修改 store 容器中的状态，需要先在容器中注册一个事件函数，当需要更新状态时候要通过触发该事件来完成。
const store = new Vuex.Store({
  state: {
    name: "wenmo"
  },
  mutations：{
	// 注册事件
	addCount(state){
	state.name = "WENMO"
	}
}
})
//在实例中显式的调用执行
new Vue({ 
   el: '#app',
    store,
    methods:{
        // 显示的调用
        handleAdd(){
            this.$store.commit('addCount')
        }
    }
})
4. action
Action类似于Mutation, 但是是用来代替Mutation进行异步操作的.action用于异步的修改state，它是通过muation间接修改state的。
若需要异步操作来修改state中的状态，首先需要action来注册事件，组件视图在通过 dispatch 分发方式调用该事件，该事件内部提交mutation中的事件完成改变状态操作，总之，通过action这个中介来提交mutation中的事件函数.
const store = new Vuex.Store({
  state: {
    name: "wenmo"
  },
  mutations：{
	// 注册事件
	setName(state){
	state.name = "WENMO"
	}
};
    // 注册事件,提交给 mutation
  actions：{
      setAction(context){
          setTimeout(() => {
              context.commit('setName')
          }, 1000)
      },
   }
})
//在实例中显式的调用执行
new Vue({ 
   el: '#app',
    store,
    methods:{
        // 显示的调用
        handleAdd(){
             this.$store.dispatch('setAction')
        }
    }
})
5. modules
const moduleA = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... },
  getters: { ... }
}

const moduleB = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... }
}

const store = createStore({
  modules: {
    a: moduleA,
    b: moduleB
  }
})

store.state.a // -> moduleA 的状态
store.state.b // -> moduleB 的状态
6、关于这五个方法的总结
state 对应的是在 store 中存储数据，类似组件中的 data
getter 对应的是 store 中访问数据，类似组件中的 计算属性
mutation 对应的是 store 中修改数据，并且是唯一的更新方式
action 类似于 mutation，用来代替 mutation进行异步操作的
modules 的作用是用来分割 store 的，每个 module 拥有自己的state、mutation、action、getters等
总结
Vuex 是一个专为 Vue开发的状态管理模式，使用集中式存储，管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。内部实现是 FLUX 模式，也就是约定数据的单向流动。
主要有五个属性，state / getter / mutation / action / modules ，分别是用来存储数据，访问数据，修改数据，进行异步操作的，和划分模块的。
Flux 模式
一、解决什么问题 当应用程序中有多个组件共享数据时，它们互连的复杂性会增加到数据状态不再可预测或不可理解的程度。因此，应用程序变得无法扩展或维护。
举个例子就是，比如我们一个在线多人聊天，类似微信的，我们有一个通知栏来告诉用户未读信息，但是通知栏偶尔会给出错误的通知。用户将收到一条新的未读消息的通知，但是当他们检查它是什么时，这只是他们已经看到的消息。
这就是多组件之间状态管理的混乱，因为 MVC架构中没法保证数据的单向流动。
二、 特点
单一事实来源，任何要在组件之间共享的数据，都需要保存在一个地方，与使用它的组件分开。这个单一的位置被称为“商店”。组件必须从该位置读取应用程序数据，而不是保留自己的副本以防止冲突或分歧。
数据只可读，组件可以自由地从存储中读取数据。但他们不能更改存储中的数据，至少不能直接更改。相反，他们必须通知存储他们更改数据的意图，并且存储将负责通过已定义“更新”的函数进行这些更改。
更新是同步的，我们根据上面的两个原则，就能很便利的追踪数据的状态变化和调试，但是如果是异步的话，我们就不能很好的判断执行的顺序。
三、具体使用
具体的应用就是我们常见的 VUEX 和 React 中。
虚拟DOM
一、什么是虚拟 DOM呢？
再过去或者我们原生JavaScript的时候，我们可以发现，当我们需要改变视图的数据的时候，我们往往需要先获取到这个 DOM 元素，然后对其进行更新。也就是：
数据改变-->操作DOM--> 视图更新
但是我们在 VUE或者 React 中是直接改变 Data 就能实现视图的更新了。
数据改变-->视图更新
那么要是我们每一次数据改变都需要操作 DOM，那就非常麻烦，而且慢。因为 JavaScript执行时很快的，但是操作 DOM就不是了。所以就有了虚拟 DOM了
数据改变-->操作虚拟 DOM（计算变更）-->操作真实的 DOM--> 视图更新
那么什么虚拟 DOM 呢？
可以说虚拟 DOM 本质上是 JS 和 DOM 之间的映射，表现为是一个能描述 DOM结构 及其属性信息的 JS对象。那么下面我们看一个例子为什么这么说吧：
//我们定义的 DOM
<div id="app">
  <p class="text">hello</p>
  <h1 class="text">hello world!!!</h1>
</div>

//转换为虚拟 DOM
{
  tag: 'div',
  props: {
    id: 'app'
  },
  chidren: [
    {
      tag: 'p',
      props: {
        className: 'text'
      },
      chidren: [
        'hello'
      ]
    },
     {
      tag: 'h1',
      props: {
        className: 'text'
      },
      chidren: [
        'hello world!!!'
      ]
    }
  ]
}

实际上就是通过 JavaScript 对象来作为基础的树，用对象的属性来描述节点，然后通过映射成真实的 DOM 结构。
二、那么这么做有什么好处呢
1、 优化性能
我们常说要减少重排的发生，那是为什么呢，因为那会涉及到 DOM 树的重新渲染。而操作 DOM 树是比较慢的，且 DOM 元素的数量谁很庞大的，当操作 DOM 很容易带来页面的性能问题。很容易给用户带来不好的体验，而这点是很重要的，可以说我们前端页面是与用户的第一个窗口。
比如，正常情况下，当我们要更新10个节点的时候，浏览器就会计算 10次 ，一次一次的进行更新。而在使用虚拟 DOM ，他相对就好像多了一个缓存区，当 DOM 操作（渲染更新）比较频繁时，它会先将前后两次的虚拟 DOM 树进行对比，定位出具体需要更新的部分，生成一个“补丁集”（也就是一个 js对象），最后只把“补丁”一次性打在需要更新的那部分真实的 DOM 树上，避免了很多没必要的计算，提高了性能。
2、抽象化渲染过程
很多人认为虚拟 DOM 最大的优势是 diff 算法，减少 JavaScript 操作真实 DOM 的带来的性能消耗。虽然这一个虚拟 DOM 带来的一个优势，但并不是全部。虚拟 DOM 最大的优势在于抽象了原本的渲染过程，实现了跨平台的能力，而不仅仅局限于浏览器的 DOM，可以是安卓和 IOS 的原生组件，可以是近期很火热的小程序，也可以是各种GUI。 解耦了视图层和渲染平台，带来了更多的可能性
有点像我们语言中，都会编译成 AST ，而在这个阶段，可以实现多种转化，就像 Babel ，和 ESList 等。
3、缺点也是有的：在初次渲染的时候，会多出一层 虚拟DOM的计算，而且使用虚拟DOM也不一定是高效的，往往当我们每一次改动不大的时候，才是相对高效的，但是如果我们改动大的话，相比还多出了更多的计算，是不利的。
总结
虚拟 DOM 本质上是 JS 和 DOM 之间的映射，表现为一个能描述 DOM结构 及其属性信息的 JS对象。没有使用 虚拟DOM 时，当我们改变数据–>就需要操作DOM–>然后视图更新，当是当我们使用虚拟DOM，就是我们改变数据–>框架就会操作虚拟 DOM进行计算变更–>之后映射到真实的 DOM上–> 完成视图更新。
当我们说虚拟DOM的优点，我们常说 虚拟DOM 提高效率，其实这需要根据场景而言的！当操作 DOM 的数量比较少的时候，使用 虚拟DOM 反而效率低，因为添加了更多的计算等操作。而当操作大量 DOM 的时候，使用 虚拟DOM 会将多次操作合并为一次更新，减少 JavaScript 操作真实 DOM 的带来的性能消耗。另外一个重要的优点是 虚拟 DOM 抽象了原本的渲染过程，实现了跨平台，跨端的能力！不再局限于浏览器！
DIFF 算法
DIFF算法的作用：同层树节点比较的算法
那么 DIFF算法是如何工作的？
一、首先是先计算新老DOM的最小变化
该算法会先遍历一遍老的DOM，然后在遍历新的DOM，最后会判断是改变/新增/删除来重新排序。 这样无疑是非常耗费计算的，我们看一看出总共遍历了三回，如果有一千个节点，那么就湖发生了十亿次的计算。
二、diff算法的优化 diff 算法的优化，也就是这个算法的核心部分了，简单来说就是针对具有相同父节点的同层新旧子节点进行比较，不相同的话就会新增或者删除，而不是使用逐层搜索递归遍历的方式。时间复杂度为O(n)。
只比较同一层级，不跨级比较
标签不同，直接删除，不继续比较
标签名相同，key相同，就认为是相同节点，不继续深度比较
Vue3
Vue3 Composition API和Vue2 Options API有什么不同
代码组织形式
Vue2使用data、methods、computed等选项将相关功能组织在一起。当组件变得复杂，对应属性的列表会变得很长，且分布在不同的选项中，导致代码难以阅读。
Vue3可以根据逻辑功能来组织代码，将一个功能定义的API都放在一起。
逻辑复用
Vue2逻辑复用通常需要使用混入（mixins）或者通过全局函数的方式，这会导致命名冲突以及数据来源不明确的问题。
Vue3通过函数的方式将逻辑组合在一起，使用setup函数可以更灵活地实现逻辑复用。
响应式
Vue2使用this关键字来访问组件实例，通过this.$data来访问响应式数据。
Vue3 使用ref、reactive等函数来创建响应式数据。
Ts支持
Vue2 支持存在TypeScript，但可能需要额外的配置和类型声明。
Vue3 对于TypeScript提供更好的支持
Vue3和Vue2有哪些区别
引入了tree-shaking, 构建时可以更轻松地剔除没有使用的代码。使得整体体积变小
引入了 Composition API，使得组件的逻辑更容易组织和复用。
Vue 3 对 TypeScript 提供更好的支持，包括更准确的类型推断和更丰富的类型定义。
使用 Proxy 替代 Object.defineProperty，提高了响应式系统的性能。
源码组织方式变化：使用 TS 重写
支持 Composition API：基于函数的API，更加灵活组织组件逻辑（vue2用的是options api）
响应式系统提升：Vue3中响应式数据原理改成proxy，可监听动态新增删除属性，以及数组变化
编译优化：vue2通过标记静态根节点优化diff，Vue3 标记和提升所有静态根节点，diff的时候只需要对比动态节点内容
打包体积优化：移除了一些不常用的api（inline-template、filter）
生命周期的变化：使用setup代替了之前的beforeCreate和created
Vue3 的 template 模板支持多个根标签
Vuex状态管理：创建实例的方式改变,Vue2为new Store , Vue3为createStore
Route 获取页面实例与路由信息：vue2通过this获取router实例，vue3通过使用 getCurrentInstance/ userRoute和userRouter方法获取当前组件实例
Props 的使用变化：vue2 通过 this 获取 props 里面的内容，vue3 直接通过 props
父子组件传值：vue3 在向父组件传回数据时，如使用的自定义名称，如 backData，则需要在 emits 中定义一下
为什么使用Proxy替换defineProperty
使用 Object.defineProperty 可以拦截对数组元素的读写操作，但无法直接监测数组索引的变化，也无法监测 length 属性的变化。因此，通过直接修改数组索引或 length 属性时，不会触发响应式更新。
Object.defineProperty 仅能拦截 get 和 set 操作。这也使得defineProperty无法劫持到对一个对象的删除和添加属性操作。
还有一个问题是，如果存在深层的嵌套对象关系，需要深层的进行监听，在性能上存在一定的开销。
总结来说就是下面几点：
无法监听到数组方法
添加或删除元素并不会触发属性的 get 或 set 操作，也无法监听。
Object.defineProperty 在处理嵌套对象时需要递归观察，有性能问题。
而Vue 3 中引入了 Proxy，提供了丰富的拦截操作，包括 get、set、has、deleteProperty 等，可以直接劫持整个对象，轻松地实现递归观察整个对象树的变化，也可以更准确地拦截数组的变化。
