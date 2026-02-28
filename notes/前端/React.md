React
基础语法层面
说一说你对React的理解
拥有构建界面的JS库，具有以下特性
JSX语法
单向数据绑定
组件化开发
虚拟DOM
声明式编程
如何理解state和props
state是变量，一般情况下，state改变之后，组件会更新。
props是属性，用于父子通信，且props不可修改。
JSX是什么
React中用JSX语法描述视图(View)，JSX 是一个看起来很像 XML 的 JavaScript 语法扩展，本质是React.createElement

const ele=<h1>hello world</h1>
既不是字符串也不是HTML，是jsx，是JS的语法扩展，可以生成React元素
React认为渲染逻辑本质与其他UI逻辑内在耦合，将标签和逻辑共同存放在组件中，实现关注点分离
编译之后，JSX被转换为JS普通函数调用，取值后得到JS对象
允许在条件或循环语句中使用JSX，将其赋值给变量，传入JSX作为参数，以及从函数中返回JSX
防止注入攻击
可以安全地在JSX中插入用户内容
React的DOM在渲染所有内容后，会进行转义，确保应用中永不会注入那些不是自己写的内容
JSX表示对象
Babel将JSX转译为一个名为React.createElement()函数调用
React读取这些React元素对象并使用它们构建DOM以保持随时更新
React事件机制
充当浏览器原生事件的跨浏览器包装器 的对象
将不同浏览器行为组合到一个 API中，确保事件显示一致的 属性
React 事件机制
 < div onClick =
{
    this.handleClick.bind(this)
}
> 点我 <  / div >
React不是将click事件绑定到了真实DOM上，而是在document处监听了所有的事件，当事件发生并且冒泡到document处的时候，React将事件内容封装并交由真正的处理函数运行。
这样可以 减少内存消耗，还能在组件挂在销毁时统一订阅和移除事件
冒泡到document上的事件也不是原生浏览器事件，而是由react自己实现的合成事件（SyntheticEvent）。
如果不想要事件冒泡的话应调用event.preventDefault()方法，而不是调用event.stopProppagation()方法
合成事件的目的如下：
合成事件抹平了浏览器间的兼容问题，这是一个跨浏览器原生事件包装器，赋予了跨浏览器开发的能力
对于原生浏览器事件来说，浏览器会给监听器创建一个事件对象。如果你有很多的事件监听，就需要分配很多的事件对象，造成高额内存分配问题。但是对于合成事件来说，有一个事件池专门来管理它们的创建和销毁，当事件需要被使用时，会从池子中复用对象，事件回调结束后，销毁事件对象上的属性，便于复用
React引入CSS的方式
内联样式，组件内直接使用： 通过style属性直接引入
组件中引入.CSS 文件， 全局生效，样式之间互相影响
css in js： 第三方库支持
引入.module.css 文件
setState 同步还是异步
setState执行机制
API层面上，setState是普通的调用执行的函数，自然是同步API
此 同步 非 彼 同步
同步还是异步 指的是调用API后更新DOM是异步还是同步？——取决于 被调用的环境
React能控制的范围调用，如 合成事件处理函数、生命周期函数，会批量更新，将状态合并后再进行DOM更新，为异步
原生JS控制的范围调用，如 原生事件处理函数，定时器回调函数，Ajax回调函数，此时setState被调用后立即更新DOM，为同步
所谓 异步 就是 批量更新，减少ADOM渲染次数，在React能控制范围内，一定是批量更新(为了性能着想)，先合并 状态，再一次性 更新DOM
setState意味着一个完整的渲染流程，包括
shouldComponentUpdate->componentWillUpdate->render->componentDidUpdate
setState 批量更新(异步) 就是为了避免 频繁 re-render，消耗性能非常恼火
批量更新 过程 和 事件循环 类似，来一个setState就将其加入 一个队列，待时机成熟， 将队列中 state 结果合并，最后只会对最新的state 进行一个更新流程
在 react17 中，setState 批量执行，但如果在 setTimeout、事件监听器等函数里，setState 会同步执行。可以在外面包一层 batchUpdates 函数，手动设置 excutionContext 切换成批量执行
react18 中所有的 setState 都是异步批量执行
说一说你对react refs的理解
React 之 Refs 的使用
ref --> reference：引用
React中 引用简写，是一个 属性，助于 存储 对React元素 或 组件的引用，引用由组件渲染配置函数返回
ref使用有三种方式：字符串(不推荐使用)，对象，函数
1、字符串 React16 之前用的最多的，如
<p ref="info">text</p>
2、函数格式，ref对应一个方法，该方法有一个参数，即，对应的节点实例
<p ref={ele=>this.info=ele}>test</p>
3、createRef方法，React16 提供的API，使用React.createRef()实现
使用场景
input标签聚焦
希望直接使用DOM元素中的某个方法，或者直接使用自定义组件中的某一个方法
ref作用于内置的HTML组件，得到的将是真实的DOM元素
ref作用于类组件，得到的将是类的实例
ref不能作用于函数组件，但是函数组件中可以传递ref
如何使用
在 class 组件用 React.createRef() 来声明，例如
class MyComponent extends React.Component
{
    constructor(props)
    {

        super(props);

        this.myRef = React.createRef();

    }

    render()
    {

        return  < div ref =
        {
            this.myRef
        }
        />;

            }

        }
在函数组件使用 React.forwardRef() 来暴露函数组件的 DOM 元素
const Input = forwardRef((props, ref) =>
    {

        return (

             < input
        {
            ...props
        }
            ref =
            {
                ref
            }
             > )

    }
    )

    class MyComponent extends React.Component
{

    constructor()
    {

        this.ref = React.createRef(null);

    }

    clickHandle = () =>
    {

        // 操作Input组件聚焦

        this.ref.current.focus();

    }

    render()
    {

        return (

             < div >

             < button onClick =
            {
                this.clickHandle
            }
             >

            点击

             <  / button >

             < Input ref =
            {
                this.ref
            }
             >

             <  / div > )

    }

}
render不能访问refs
因为 render 阶段 DOM还未生成，无法获取 DOM，DOM的获取需要在 pre-commit 和 commit 阶段
react中key的作用
浅谈React 虚拟DOM，Diff算法与Key机制
React生命周期
React生命周期图示
React15
constructor() // 构造函数

componentWillReceiveProps() // 父组件状态属性更新触发

shouldComponentUpdate() // 组件更新时调用，在此可拦截更新

componentWillMount() // 初始化渲染时调用（挂载前调用）

componentWillUpdate() // 组件更新时调用

componentDidUpdate() // 组件更新后调用

componentDidMount() // 初始化渲染时调用（挂载后调用）

render() // 生成组件虚拟Dom

componentWillUnmount() // 组件卸载时调用
React16
constructor() // 构造函数

getDerivedStateFromProps() // 组件初始化和更新时调用

shouldComponentUpdate() // 组件更新时调用，在此可拦截更新

render() // 生成虚拟Dom

getSnapshotBeforeUpdate() // 组件更新时调用

componentDidMount() // 组件初始化时调用（挂载后调用）

componentDidUpdate(prevProps, prevState) // 组件更新后调用

componentWillUnmount() // 组件卸载时调用
constructor
实例过程中自动调用，方法内部通过super关键字获取父组件的props
通常初始化state或者this上挂载方法
16新增2个
static getDerivedStateFromProps(nextProps, prevState)
静态方法(纯函数)
执行时机：组件创建和更新阶段，不论是props变化还是state变化，都会调用
在每次render方法前调用，第一个参数为即将更新的props，第二个参数为上一个状态的state，比较props 和 state来加一些限制条件，防止无用的state更新
该方法返回一个新对象作为新的state或者返回null表示state状态不需要更新
getDerivedStateFromProps() contains the following legacy lifecycles:
componentWillMount
componentWillReceiveProps
componentWillUpdate
React 16.4后对getDerivedStateFromProps做了微调。在>=16.4以后的版本中，组件任何的更新流程都会触发getDerivedStateFromProps，而在16.4以前，只有父组件的更新会触发该生命周期
getSnapshotBeforeUpdate(prevProps, prevState)
该周期函数在render后执行，执行之时DOM元素还没有被更新
该方法返回一个Snapshot值，作为componentDidUpdate第三个参数传入
getSnapshotBeforeUpdate(prevProps, prevState) {

console.log('#enter getSnapshotBeforeUpdate');

return 'foo';

}

componentDidUpdate(prevProps, prevState, snapshot) {

console.log('#enter componentDidUpdate snapshot = ', snapshot);

}
目的在于获取组件更新前的信息，比如组件的滚动位置之类的，在组件更新后可以根据这些信息恢复UI视觉上的状态
componentDidMount
组件挂载到ADOM节点后执行，在render之后执行，执行一些数据获取，事件监听等操作
shouldComponentDidMount
告知组件本身基于当前的props和state是否需要重新渲染组件，默认情况返回true。
执行时机：到新的props或者state时都会调用，通过返回true或者false告知组件更新与否
一般情况，不建议在该周期方法中进行深层比较，会影响效率
同时也不能调用setState，会导致无限循环
componentDidUpdate
执行时机：组件更新结束后触发
在该方法中，可以根据前后的props和state的变化做相应的操作，如获取数据，修改DOM样式等
componentWillUnmount
组件卸载前，清理一些注册或监听事件，或者取消订阅的网络请求
一旦一个组件实例被卸载，其不会被再次挂载，只可能被重新创建
准备废弃的生命周期
componentWillMount
风险很高，鸡肋
componentWillReceiveProps(nextProps)
一个API并非越复杂才越优秀。从根源帮助开发者避免不合理的编程方式和对生命周期的滥用
判断另个props是否相同，若不同将新的props更新到相应的state上
破坏state数据的单一数据源，导致组件状态不可预测
增加组件的重绘次数
componentWillUpdate( nextProps, nextState )
挡了Fiber架构的路
组件更新前，读取某个DOM元素状态，并在componentDidUpdate中处理
由getSnapshotBeforeUpdate(prevProps,prevState) 代替.在最终的render之前调用
为何要废弃它们？
在Fiber机制下，render阶段允许被暂停、终止和重启
**导致render阶段的生命周期都可能重复执行。**这几个方法常年被滥用，执行过程中存在风险。比如setState fetch发起请求 操作真实Dom等
这些操作完全可以转移到其他方法中做
即使没有开启异步渲染，Recat15中也可能导致一些严重的问题，比如componentWillReceiveProps和componentWillUpdate里滥用setState导致重复渲染
首先确保了Fiber机制下数据安全性，同时也确保生命周期方法的行为更纯粹
组件开发
有状态组件和无状态组件
有状态组件
特点
是类组件
有继承
有this
有生命周期
使用较多，易触发生命周期钩子函数
内部使用state，根据外部组件传入的props和自身state渲染
使用场景
需要使用状态的
需要状态操作组成的
总结
可维护自己的state，可以对组件做更多的控制
无状态组件
特点
不依赖自身state
可以是类组件或函数组件
可避免使用this
组件内部不维护state，props改变，组件re-render
使用场景
组件不需要管理state
优点
简化代码 专注render
组件不需要实例化，无生命周期
视图和数据解耦
缺点
无法使用ref
无生命周期
无法控制组件re-render
当一个组件不需要管理自身状态时，就是无状组件，应该优先设计为函数组件，比如定义的
函数式组件和类组件的区别
编写形式：函数形式和类形式，函数组件语法简单，类组件更复杂。
状态：函数组件无状态，类组件有状态
生命周期：函数组件不存在生命周期，而是用React Hooks，类组件有生命周期
受控组件和非受控组件
受控组件
表单状态变化，触发onChange事件，更新组件state
受控组件中，组件渲染出的状态和它的value或checked属性相对应，react通过这种方式消除了组件的局部状态，使组件变得可控
缺点
多个输入框需要获取到全部值时，需要每个都编写事件处理函数，代码变得臃肿
后来，出现了非受控组件
非受控组件
表单组件没有value props
可使用ref 从 DOM 中获取表单值，而不是编写事件处理函数
使用非受控组件可以减少代码量
React组件通信
父组件向子组件传递
子组件向父组件传递
兄弟组件之间的通信
父组件向后代组件传递
非关系组件传递
父组件向子组件传递
React的数据流是单向的，这是最常见的方式，props
子组件向父组件传递
父组件向子组件传一个函数，然后通过这个函数的回调拿到子组件传递的值
兄弟组件之间的通信
父组件作为中间层实现数据互通
父组件向后代组件传递
最普通的事情，像全局数据一样。
使用context可共享数据，其他数据都能读取对应的数据。
非关系组件传递
组件间关系类型复杂，可以将数据进行一个全局资源管理，从而实现通信，例如redux dva
PureComponent&Component
Component需要手动实现shouldComponentDidMount，而PureComponent通过浅对比默认实现了shouldComponentDidMount
浅比较，只比较第一层
PureComponent不仅影响本身，而且会影响子组件，所以其最佳情况是展示组件
高阶组件
一文吃透React高阶组件
高阶组件，它是个函数，接收组件作为参数，返回一个新的组件。
React Hooks
React 全部 Hooks 使用大全
React16.8之后，推出新功能：Hooks。这样可以在函数定义的组件中使用类组件的特性
Hooks好处
跨组件复用，轻量，改造成本小，不影响原来组件层级结构和嵌套地狱
hook没生命周期，class有（hook可以使用钩子函数模仿生命周期）
状态与UI隔离，状态逻辑粒度更小，可以把业务逻辑抽离出来做自定义hook
hook缺点
状态不同步，容易产生闭包，需要使用useRef去记录
注意
React函数组件中使用Hooks
避免循环/条件中调用hooks，保证调用顺序的稳定
不能在useEffect中使用useState，React会报错
hooks前，类组件边界强于函数组件
UI=render(data) 或 UI=func(date)
为啥useState使用数组
解构赋值！！
如果使用数组，我们可以对数组中元素命名，代码比较干净
如果使用对象，解构时必须要和useState内部实现返回对象同名，多次使用只能设置别名
// 第一次使用
const
{
    state,
    setState
} = useState(false);

// 第二次使用
const
{
    state: counter,
    setState: setCounter
} = useState(0)
解决问题
组件间逻辑复用
复杂组件理解
难以理解的class
使用限制
不再循环、条件和嵌套函数中调用(链表 实现Hook，可能导致 数组取值错位)
仅在函数组件中调用hook(因为没有 this)
useLayoutEffect和useEffect
共同点
都是处理副作用，包括 DOM改变，订阅设置，定时器操作
不同点
useEffect异步调用，按顺序执行，屏幕像素改变后执行，可能会闪烁
useLayoutEffect在所有DOM变更后同步调用，处理 DOM操作，样式调整；改变屏幕像素之前执行(会推迟页面显示的时间，先改变DOM后渲染)，不会闪烁，总是比 useEffect先执行！
useLayoutEffect 和 componentDidMount，componentDidUpdate 执行时机一样，在浏览器将所有变化渲染到屏幕之前执行
建议使用 useEffect！建议使用 useEffect！建议使用 useEffect！ 避免阻塞视觉更新
页面有异常就再替换为 useLayoutEffect
常见 Hooks
useState，useEffect，useContext，useReducer，useRef，useMemo，useCallback，useLayoutEffect，useImperativeHandle，useDebugValue
useMemo
当父组件中调用子组件时，父组件的state变化，会导致父组件更新，子组件即使没有变化，也会更新
函数式组件从头更新到尾，只要一处改变，所有模块都会刷新——没必要！
理想状态是 各个模块只进行 自己的更新，不相互影响
useMemo为了防止一种情况——父组件更新，无论是否最子组件操作，子组件都会更新
memo 结合了 PureComponent 纯组件 和 componentShouldUpdate 功能，会对传入的props进行一次对比，根据第二个函数返回值判断哪些props需要更新
useMemo和memo类似，都是 判断 是否满足当前限定条件决定是否执行 callback ，useMemo的第二个参数是一个数组，通过这个数组判断是否更新回调函数
好处
减少不必要 循环 和 渲染
减少 子组件 渲染次数
避免不必要 的开销
useCallback
和useMemo 可以说是一模一样，唯一不同的是useMemo返回函数运行结果，而useCallback返回函数
这个函数是父组件传递子组件的 一个函数，防止无关 刷新，这个组件必须配合 memo，否则可能 还会降低 性能
useRef
获取当前元素的所有属性，返回一个可变的ref对象，且这个对象 只有 current 属性，可设置 initialValue
获取对应属性值
缓存数据
react-redux 源码中，hooks推出后，react-redux用大量的useMemo重做了 Provide 等核心模块，运用了useRef 缓存数据，所运用的useRef() 没有一个是绑定在dom元素上的，都是用于数据缓存
react-redux 利用 重新赋值，改变了缓存的数据，减少不必要更新，如果使用userState势必会re-render
总结
一个优秀的hooks一定具备 useMemo useCallback 等api 优化
制作自定义hooks遇到传递过来的值，优先考虑使用useRef，再考虑使用useState
封装时，应该将存放的值放入useRef中
状态管理
Redux
Redux名字的含义是Reducer+Flux，——视图层框架
context“上下文环境”，让一个树状组件上所有的组件都能访问一个共同的对象，context 由其父节点链上所有组件通过 getChildContext() 返回context对象组合而成，因此，通过context 可以访问其父组件链上context
创建一个特殊的react组件，它将是通用的一个context提供者，可以应用在任何一个应用中——Provider！
Provider只是把渲染工作完全交给子组件，只是提供Context包住最顶层组件，context覆盖了整个应用
Context=提供一个全局可访问的对象，但是全局对象应该避免，只要有一个地方做了修改，其他地方会受影响
context 只有对个别组件适用，不要滥用！
Redux的store封装得好，没有提供直接修改状态功能，克服了全局对象的缺点。且一个应用只有一个Store，store是context唯一需要，不算是滥用
工作原理
用户(View)发出 action，使用dispatch
store 自动调用 reducer，传入参数：state 和收到的action，reducer返回新的state
state变化，store调用监听函数，更新 View
异步请求处理
借助 redux 的中间件 异步处理
主要有 redux-thunk，redux-saga(常用)
此处主要介绍 redux-saga
优点：
异步解耦，不会掺杂在 action 或 component 中，代码简洁度提高
异常处理，可使用 try/catch 捕获异常
功能强大，无需封装或简单封装 即可使用
灵活，可将saga 串行 起来，形成异步 flow
易测性
缺陷：
学习成本高
体积略大
功能过剩
yield无法返回 TS 类型
@connect
连接React和Redux
connect通过context获取Provider中的state，通过store.getState()获取store tree上所有state
将state和action通过 props 的方式传入组件内部，wrapWithConnect 返回一个Component对象connect，connect重新render 外部传入的元组件 wrapWithConnect ，将connect中传入的mapStateToProps ，mapDispatchToProps 与组件上原有的props 合并，通过属性的方式传给 WrappedComponent
监听 state tree 变化。connect缓存了store tree中state的状态，根据state当前和变更前状态比较，确定是否setState触发connect及re-render
connect的工作
把store上的状态转化为内层傻瓜组件的prop
把内层傻瓜组件的用户动作 转化为派送给store的动作
@有时候使用Symbol代替字符串表示枚举值更合适，但是有的浏览器不支持
action构造函数返回一个action对象
Redux和Vuex
区别
vuex改进了redux中的action和reducer，以mutations 变化函数取代 reducer，无需 switch，只需在mutations中修改对应state即可
vuex无需订阅重新渲染，只需要生成新的state
vuex数据流，view调用store，commit提交对应请求到store中对应mutations，store修改，vue检测state修改自动渲染
vuex弱化dispatch和reducer，更简易
共同点
单一数据流
可预测变化
都是对MVVM思想服务
中间件如何拿到store和action
redux 中间件本质是一个函数柯里化，
涉及 源码
redux toolkit
Redux 最佳实践 Redux Toolki
Redux Toolkit 是 Redux 官方推荐的 Redux 开发工具。注意，RTK只是封装了一层Redux而已。
它包括几个实用程序功能，这些功能可以简化最常见场景下的 Redux 开发，包括配置 store、定义 reducer，不可变的更新逻辑、甚至可以立即创建整个状态的 “切片 slice”，而无需手动编写任何 action creator 或者 action type。它还自带了一些最常用的 Redux 插件，例如用于异步逻辑 Redux Thunk，用于编写选择器 selector 的函数 Reselect ，你都可以立刻使用。
路由
react-router完全指南
原理
客户端路由 实现原理
基于hash 路由，监听hashchange 事件，location.hash=xxxx 改变路由
基于H5的 history，通过history，pushState 和 replaceState 修改URL，能应用 history.go() 等 API，允许通过 自定义事件 触发实现
react-router实现原理：
基于 history 库实现，可 保存 浏览器 历史记录
维护列表，每次回收URL发生变化的回收，通过配置的路径，匹配对应的 Component 并 render
路由切换
组件 ，通过 比较 的path属性和当前地址的 pathname 实现，匹配成功则 render，否则渲染null
// when location = { pathname: '/about' }

 < Route path = '/about' component =
{
    About
}
/> / / renders < About /  >

 < Route path = '/contact' component =
{
    Contact
}
/> / / renders null

 < Route component =
{
    Always
}
/> / / renders < Always /  >
+，对进行分组，遍历所有的子 ，渲染匹配的第一个元素
 < Switch >

 < Route exact path = "/" component =
{
    Home
}
/>

      <Route path="/about" component={About} />

<Route path=" / contact " component={Contact} />

</Switch>
<Link> <NavLink> <Redirect>，<Link> 组件创建链接，会在HTML处 渲染锚(<a>)
 < Link to = "/" > Home <  / Link >

    // <a href='/'>Home</a>

    当 < NavLink > 的 to 属性与当前地址匹配时，可将其定义为活跃的

    // location = { pathname: '/react' }

     < NavLink to = "/react" activeClassName = "hurray" >

    React

     <  / NavLink >

    // <a href='/react' className='hurray'>React</a>
渲染<Redirect>强制导航
重定向
实现路由重定向
请求 /users/:id 被重定向去 '/users/profile/:id'：
属性 from: string：匹配的将要被重定向路径
属性 to: string：重定向的 URL 字符串
属性 to: object：重定向的 location 对象
属性 push: bool：若为真，重定向将会把新地址加入到访问历史记录里，且无法回退到前面的页面
Link和a
都是链接，都是标签
是 react-router 中实现路由跳转的链接，一般配合 使用，跳转 只会触发相匹配的 对应页面内容更新，不会刷新all page 行为
有onClick 就 onClick
click 时阻止a 默认事件
根据to属性，使用histor 或 hash 跳转，跳转只是链接变了，没有all page 刷新，<a>是普通的超链接
<a> 禁用后咋实现跳转？
手动赋值给<a>标签 location 属性
let domArr = document.getElementsByTagName('a')

    [...domArr].forEach(item =>
    {

        item.addEventListener('click', function ()
        {

            location.href = this.href

        }
        )

    }
    )
获取URL参数
get 方法
this.props.location.search 获取 URL 得到字符串，解析参数，或者自己封装方法获取参数
动态路由传值
如 path='/admin/:id'，this.props.match.params.id 获取 URL中动态部分路由 id值，或者使用hooks的 API获取
query 或 state传值
组件 的 to属性可以传递对象 {pathname:'/admin',query:'111',state:'111'}，this.props.location.state或 this.props.location.query 获取，一旦刷新页面 数据丢失
获取历史对象
React>=16.8 ，使用 React Router的Hooks
import
{
    useHistory
}
from "react-router-dom";

let history = useHistory();
this.props.history
路由模式
BrowserRouter
H5的history API控制路由跳转
HashRouter
URl的hash 属性控制路由挑转
React18新特性
正式支持Concurrent
Concurrent最主要的特点就是渲染是可中断的。以前是不可中断的，也就是说，以前React中的update是同步渲染，在这种情况下，一旦update开启，在任务完成前，都不可中断。
为什么要这样修改：react-dom/
client中的createRoot取代以前的ReactDOM.render
以前root只存在于React内部，现在用户也可以复用root了。
const root = createRoot(document.getElementById("root"));
root.render(jsx);
自动批量处理 Automatic Batching / setState是同步还是异步
可同步可异步。
在React18以前，可以把setState放在promises、setTimeout或者原生事件中实现同步。
而所谓异步就是个批量处理，为什么要批量处理呢。举个例子，老人以打渔为生，难道要每打到一条沙丁鱼就下船去集市上卖掉吗，那跑来跑去的成本太高了，卖鱼的钱都不够路费的。所以老人都是打到鱼之后先放到船舱，一段时间之后再跑一次集市，批量卖掉那些鱼。对于React来说，也是这样，state攒够了再一起更新。
但是以前的React的批量更新是依赖于合成事件的，到了React18之后，state的批量更新不再与合成事件有直接关系，而是自动批量处理。
// 以前: 这里的两次setState并没有批量处理，React会render两次
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
}, 1000);

// React18: 自动批量处理，这里只会render一次
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
}, 1000);
所以如果你项目中还在用setTimeout之列的“黑科技”实现setState的同步的话，升级React18之前，记得改一下~
虽然建议setState批量处理，但是如果你有一些其它理由或者需要应急，想要同步setState，这个时候可以使用flushSync，下面的例子中，log的count将会和button上的count同步:
// import { flushSync } from "react-dom";

changeCount = () => {
  const { count } = this.state;
  
  flushSync(() => {
    this.setState({
      count: count + 1,
    });
  });
  
  console.log("改变count", this.state.count); //sy-log
};

// <button onClick={this.changeCount}>change count 合成事件</button>
Suspense
支持Suspense，可以“等待”目标UI加载，并且可以直接指定一个加载的界面（像是个 spinner），让它在用户等待的时候显示。
<Suspense fallback={<Spinner />}>
  <Comments />
</Suspense>
错误处理边界
在 Suspense 中，获取数据时抛出的错误和组件渲染时的报错处理方式一样——你可以在需要的层级渲染一个错误边界组件来“捕捉”层级下面的所有的报错信息。
export default class ErrorBoundaryPage extends React.Component {
  state = {hasError: false, error: null};
  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      error,
    };
  }
  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

SuspenseList
用于控制Suspense组件的显示顺序。目前正式环境中还不支持，预计在18.X再支持。
transition
React把update分成两种：
Urgent updates 紧急更新，指直接交互，通常指的用户交互。如点击、输入等。这种更新一旦不及时，用户就会觉得哪里不对。
Transition updates 过渡更新，如UI从一个视图向另一个视图的更新。通常这种更新用户并不着急看到。
并引入了相关API，startTransition、useTransition与useDeferredValue。
startTransition可以用在任何你想更新的时候。但是从实际来说，以下是两种典型适用场景：
渲染慢：如果你有很多没那么着急的内容要渲染更新。
网络慢：如果你的更新需要花较多时间从服务端获取。这个时候也可以再结合Suspense。
useTransition：在使用startTransition更新状态的时候，用户可能想要知道transition的实时情况，这个时候可以使用它。
使用方法：const [isPending, startTransition] = useTransition();
useDeferredValue使得我们可以延迟更新某个不那么重要的部分，相当于参数版的transitions。
新的Hooks
useTransition：如上。
useId：用于产生一个在服务端与Web端都稳定且唯一的ID，也支持加前缀，这个特性多用于支持ssr的环境下。
useSyncExternalStore：此Hook用于外部数据的读取与订阅。
useInsertionEffect：函数签名同useEffect，但是它是在所有DOM变更前同步触发。主要用于css-in-js库，往DOM中动态注入<style> 或者 SVG <defs>。因为执行时机，因此不可读取refs。
虚拟DOM
什么是虚拟DOM
用 JavaScript 对象表示 DOM 信息和结构，当状态变更的时候，重新渲染这个 JavaScript 的对象结构。这个 JavaScript 对象称为虚拟DOM。
DOM操作很慢，轻微的操作都可能导致页面重新排版，非常耗性能。相对于DOM对象，js对象处理起来更快，而且更简单。通过diff算法对比新旧vdom之间的差异，可以批量的、最小化的执行dom操作，从而提升用户体验。
VDom
一个对象，将真实的DOM树转换为JS对象树
 < button class = "myButton" >

     < span > this is button <  / span >

     <  / button >

    //转换

{

    type: 'button',

    props:
    {

        className: 'myButton',

        children: [
            {

                type: 'span',

                props:
                {

                    type: 'text'

                    children: 'this is button'

                }

            }
        ]

    }

}
将多次DOM修改的结果一次性更新到页面上，有效减少页面渲染次数，减少修改DOM的重排重绘次数，提高渲染性能
优越之处在于，提供更爽的、更高效的研发模式(函数式的UI编程模式)的同时，仍然保持还不错的性能
保证性能下限，不手动优化时，提供过得去的性能
跨平台
VDOM生成真实对象render方法
1.构建虚拟 DOM
2.通过虚拟 DOM 构建真正的 DOM
3.生成新的 VDOM
4.比较两棵 VDOM 异同
5.应用变更于 DOM
diff算法
ADOM映射为VDOM
VDOM变化后，根据差距生成patch，这个patch是结构化数据，包括增加 更新 和移除
根据patch更新 ADOM
diff 从 树 组件 及 元素 3个层面进行复杂度的优化
1、忽略节点跨层级操作
若节点不存在了，则该节点及其子节点会被删除掉，不会进一步比较
2、若组件 是同一类型就进行树 对比，如果不是就直接放入 patch中，只要父组件类型不一致，就会re-render
3、同一层级子节点，通过key 进行列表对比
标记key，React 可以直接移动 DOM节点，降低消耗
VDom一定更快吗
VDOM是JS对象，模拟DOM节点，是通过特定算法计算出一次操作所带来的DOM变化。react和vue中都使用了VDOM
react中涉及到VDOM的代码主要分为三部分，第二步domDiff是核心：
把render中的JSX(或者createElement这个API)转化成VDOM
状态或属性改变后重新计算VDOM并生成补丁对象(domDiff)
通过补丁对象更新视图中的DOM节点
不一定更快
DOM操作是性能杀手，因为操作DOM会引起页面回流或重绘。相比，通过预先计算减少DOM的操作更划算
但是，“使用VDOM会更快”不一定适用所有场景。例如：一个页面就有一个按钮，点击一下，数字加一，肯定是直接操作DOM更快。使用VDOM无非白白增加计算量和代码量。即使是复杂情况，浏览器也会对我们的DOM操作进行优化，大部分浏览器会根据我们操作的时间和次数进行批量处理，所以直接操作DOM也未必很慢
那为什么现在的框架都使用VDOM？因为VDOM可以提高代码的性能下限，并极大优化大量操作DOM时产生的性能损耗。同时也保证了，即使在少数VDOM不太给力的场景下，性能也在我们接受的范围内
Diff算法
react diff算法
React性能优化
思路
减少render执行次数
减少渲染的节点
降低渲染计算量
VDOM
使用工具分析性能
使用不可突变数据结构，数组使用concat，对象使用Object.assign()
组件尽可能拆分
列表类组件优化
bind函数优化
不滥用props
reactDOMServer服务端渲染组件
React.memo
缓存组件
记忆组件渲染结果，提高组件性能
只检查props是否变化
做浅比较
第二个参数可传入自定义比较函数
areEqual方法和shouldComponentUpdate返回值相反
const App = React.memo(

        function myApp(props) {
        //使用props渲染
    }

        function areEqual(prevProps, nextProps) {
        //如果把prevProps传入render方法的返回结果和将nextProps传入render的返回结果一样，则返回true，否则返回false
    });
React.useMemo
缓存大量计算
useMemo 的第一个参数就是一个函数，这个函数返回的值会被缓存起来，同时这个值会作为 useMemo 的返回值，第二个参数是一个数组依赖，如果数组里面的值有变化，那么就会重新去执行第一个参数里面的函数，并将函数返回的值缓存起来并作为 useMemo 的返回值。
// 避免这样做
function Component(props) {

    const someProp = heavyCalculation(props.item);

    return  < AnotherComponent someProp = {
        someProp
    }
    />
    }

    // 只有 `[props.item](http://props.item)` 改变时someProp的值才会被重新计算
    function Component(props) {

        const someProp = useMemo(() => heavyCalculation(props.item), [props.item]);
        return  < AnotherComponent someProp = {
            someProp
        }
        />
        }
PureComponent
避免重复渲染
React.Component并未实现 shouldComponentUpdate()，而 React.PureComponent中以浅层对比 Prop 和 State 的方式来实现了该函数。
shouldComponentUpdate函数中做的是“浅层比较”。若是“深层比较”，那时某个特定组件的行为，需要我们自己编写。
父组件状态的每次更新，都会导致子组件的重新渲染，即使是传入相同props。但是这里的重新渲染不是说会更新DOM,而是每次都会调用diif算法来判断是否需要更新DOM。这对于大型组件例如组件树来说是非常消耗性能的。
shouldComponentUpdate生命周期来确保只有当组件props状态改变时才会重新渲染.
PureComponent会进行浅比较来判断组件是否应该重新渲染，对于传入的基本类型props，只要值相同，浅比较就会认为相同，对于传入的引用类型props，浅比较只会认为传入的props是不是同一个引用，如果不是，哪怕这两个对象中的内容完全一样，也会被认为是不同的props。
PureComponent，因为进行浅比较也会花费时间，这种优化更适用于大型的展示组件上。大型组件也可以拆分成多个小组件，并使用memo来包裹小组件，也可以提升性能。
确保数据类型是值类型
如果是引用类型，不应当有深层次的数据变化(解构)
避免使用内联对象
使用内联对象时，react会在每次渲染时重新创建对此对象的引用，这会导致接收此对象的组件将其视为不同的对象,因此，该组件对于prop的浅层比较始终返回false,导致组件一直重新渲染。
// Don't do this!

function Component(props) {

const aProp = { someProp: 'someValue' }

return <AnotherComponent style={{ margin: 0 }} aProp={aProp} /> 

}



// Do this instead :)

const styles = { margin: 0 };

function Component(props) {

const aProp = { someProp: 'someValue' }

return <AnotherComponent style={styles} {...aProp} /> 

}
避免使用匿名函数
// 避免这样做

function Component(props) {

return <AnotherComponent onChange={() => props.callback(props.id)} /> 

}

// 优化方法一

function Component(props) {

const handleChange = useCallback(() => props.callback(props.id), [props.id]);

return <AnotherComponent onChange={handleChange} /> 

}

// 优化方法二

class Component extends React.Component {

handleChange = () => {

this.props.callback(this.props.id) 

}

render() {

return <AnotherComponent onChange={this.handleChange} />

}

}
组件懒加载
可以使用新的React.Lazy和React.Suspense轻松完成。
React.lazy
定义一个动态加载的组件，这可以直接缩减打包后 bundle 的体积，延迟加载在初次渲染时不需要渲染的组件
React.Suspense
悬挂 终止 暂停
配合渲染 lazy 组件，在等待加载 lazy组件时展示 loading 元素，不至于直接空白，提升用户体验；
<Suspense fallback={<PageLoading />}>{this.renderSettingDrawer()}</Suspense>

const SettingDrawer = React.lazy(() => import('@/components/SettingDrawer'));
用 CSS
而不是强制加/卸载组件
渲染成本很高，尤其是在需要更改DOM时。此操作可能非常消耗性能并可能导致延迟
// 避免对大型的组件频繁对加载和卸载

function Component(props) {

const [view, setView] = useState('view1');

return view === 'view1' ? <SomeComponent /> : <AnotherComponent /> 

}

// 使用该方式提升性能和速度

const visibleStyles = { opacity: 1 };

const hiddenStyles = { opacity: 0 };

function Component(props) {

const [view, setView] = useState('view1');

return (

<React.Fragment>

<SomeComponent style={view === 'view1' ? visibleStyles : hiddenStyles}>

<AnotherComponent style={view !== 'view1' ? visibleStyles : hiddenStyles}>

</React.Fragment>

)

}
React.Fragment
聚合子元素列表，不在DOM中添加额外标签
function Component() {

return (

<React.Fragment>

    <h1>Hello world!</h1>

    <h1>Hello there!</h1>

    <h1>Hello there again!</h1>

</React.Fragment>

)

}
key
保证key具有唯一性
DIff算法根据key判断元素时新创建还是被移动的元素，从而减少不必要渲染
虽然key是一个prop，但是接受key的组件并不能读取到key的值，因为key和ref是React保留的两个特殊prop
合理使用Context
无需为每层组件手动添加 Props，通过provider接口在组件树间进行数据传递
原则
Context 中只定义被大多数组件所共用的属性
使用createContext创建一个上下文
设置provider并通过value接口传递state数据
局部组件从value接口中传递的数据对象中获取读写接口
toggle——切换
import { createContext } from 'react';

const LoginContext = createContext();

export default LoginContext;
虚拟列表
合理设计组件
简化Props
简化State
减少组件嵌套
Fiber
React 15 ，渲染时 会递归对比 VDOM，找出需要变动的节点，再同步更新，一气呵成！！此过程中，React会占据浏览器资源，导致用户触发的事件得不到响应，导致 掉帧，用户觉得卡顿！！
将浏览器 渲染 布局 绘制 资源加载 事件响应 脚本执行 看成OS的process，通过一些调度策略合理分配 CPU 资源，提高浏览器 的用户响应速率，兼顾 执行效率
React16起，引入 Fiber 架构
让执行过程 变得 可中断！！
分批延时 操作 DOM，避免一次性操作大量 DOM 节点，用户体验更好
给浏览器一点喘息的机会，对代码进行 编译 优化 及热代码优化
Fiber也称协程或纤程，和线程并不一样，协程本身没有并发或者 并行能力，它只是一种控制流程的让出机制。让出 CPU 的执行权，让 CPU 能在这段时间执行其他的操作。
dangerouslySetInnerHTML
是REact中innerHTML的替代品
<div dangerouslySetInnerHTML={{ __html: newsTexts }} />
React的HTML元素上的一个属性，它可能是危险的，因为我们容易收到XSS(跨站脚本攻击)——从第三方获取数据或用户提交内容时
React会识别HTML标签，然后渲染
HTML元素可能会执行脚本，当JS代码附加到HTML元素上
使用HTML净化工具DOMPurify检测HTML中潜在的恶意部分
