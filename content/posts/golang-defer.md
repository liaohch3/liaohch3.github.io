+++
title = 'Golang defer 关键字的三个细节'
description = '本文介绍 Golang 中使用 defer 关键字容易踩坑的三个细节，帮助你写出更优雅的代码。'
date = 2024-04-25T13:13:41+08:00
draft = false
tags = ["golang", "code"]
+++

这是我第一篇正式的技术博客，灵感来自前段时间某位同事向我请教的问题：为什么 Golang defer 函数没有按预期执行？我觉得这是一个很容易踩坑的点，所以我在网上学习后，写出这篇博客。

## 1. defer 的作用
在 Golang 中，我们常常需要编写一些成对出现的代码，一个前置操作固定搭配一个后置操作，例如
- 上锁后，要解锁
- 打开文件，或发起网络请求后，执行文件/网络句柄的关闭操作
- 执行完一段业务逻辑后，统一打印这段逻辑的业务日志和耗时

通常我们需要在执行完前置操作后，执行一段复杂的业务逻辑，然后再执行后置操作。例如发起打开文件后，解析对文件的内容进行解析，然后再关闭文件句柄，打开和关闭文件两个操作可能中间间隔一段复杂的业务逻辑。 如果将关闭文件、打印日志、解锁操作放在与他们成对出现的前置操作太远的地方，就会导致我们可能在某些执行分支遗漏编写后置语句，导致文件没有正常关闭，锁没有正常释放。

好在，Golang 提供了 defer 关键字，方便你在前置操作完成后，写一个后置操作的代码，等到整段业务逻辑执行完成，再执行 defer 中的操作。 然而，defer 在使用时有一些值得注意的地方，如果用得不好的话，可能会有不符合预期的事情发生。


## 2. 问题现象
我的同事使用 defer 来打印请求的整体日志和整体耗时，他在 debug 的时候发现日志里打印出来的内容都是 0，大概的代码如下

```go
// process 执行某项操作，并记录结果、错误（如果有的话）以及执行时长。
func process() (result string, err error) {
    start := time.Now()
    defer logReq(result, err, start)

    // 调用 doSomething 并将结果赋值给 result 和 err。
    result, err = doSomething()
    if err != nil {
       return "", err
    }

    return result, nil
}

// doSomething 模拟一个需要一些时间来完成的过程。
func doSomething() (string, error) {
    time.Sleep(time.Second) // 模拟执行任务通过休眠一秒。
    return "done", nil      // 返回成功的结果。
}

// logReq 记录 process 函数的执行结果、错误和耗时。
func logReq(result string, err error, start time.Time) {
    log.Printf("result: %s, err: %v, time: %vms", result, err, time.Since(start).Milliseconds())
}

func main() {
    process()   
}
```

这段代码执行的结果我放在下面，我们预期 defer 能在业务逻辑执行完成后，打印出 result 的值，但是实际执行的结果却不是这样。实际上 result 打印出来是一个空字符串，而不是我们预期的 "done"，这是为什么呢？

```
2024/04/25 13:11:50 result: , err: <nil>, time: 1001ms
```


在解答这个问题之前，我们先对 defer 有一个简要的介绍，介绍在使用 Golang defer 关键字时需要注意的三个地方

## 3. defer 的作用

在 Golang 中，`defer` 关键字用于预定一个函数调用，这个函数会在包围它的函数执行完毕（即将返回）之前被调用。`defer` 通常用于执行一些清理工作，例如释放资源、关闭文件、解锁互斥量等。使用 `defer` 可以确保函数退出时，无论因为正常返回还是因为发生错误（如 panic），相关资源都能被正确释放或清理。

```go
func main() {
    // 定义一个匿名函数，并使用 defer 关键字预定它的执行。
    // 这个匿名函数将在 main 函数即将返回之前执行。
    defer func() {
        fmt.Println("这是通过 defer 延迟执行的语句")
    }()

    // 主函数的其他代码
    fmt.Println("主函数中的代码执行")
}
```


在这个例子中，我们在 `main` 函数中使用 `defer` 关键字来延迟执行一个匿名函数，该匿名函数只包含一个打印语句。这个 `defer` 语句确保无论 `main` 函数的执行路径如何，匿名函数都会在 `main` 函数返回之前执行。运行这段代码，你将看到以下输出：

```
主函数中的代码执行
这是通过 defer 延迟执行的语句
```

这个输出清楚地表明，尽管 `defer` 语句在打印 "主函数中的代码执行" 之前声明，但是它延迟的函数实际上是在所有其他语句执行完成后，`main` 函数即将返回前才执行的。

## 4. defer 值得关注的三个细节
### 4.1 defer 执行顺序
当函数中有多个 defer 的时候，每一个 defer 函数的执行顺序是按照 defer 声明顺序的倒序。本质上是一个栈，后进先出。
```go
func process() {
   defer fmt.Println("1")
   defer fmt.Println("2")
   defer fmt.Println("3")
}
```
output:
```text
3
2
1
```
实际开发过程中，使用多个 defer 的场景并不多见，遇到了通常也不会有太大问题

### 4.2 defer 函数的执行发生在函数结束的时候，而不是代码块的结束
有时候我们会把代码封在一个代码块里，通常是 if for 等关键字的代码块，此时使用 defer 关键字要格外注意他的执行时机。

代码块结束时 defer 并不会被执行，直到整个函数结束时，defer 才会执行。稍不注意，可能导致 defer 函数实际执行的时间比你预期的要晚一些。

示例如下
```go
func main() {
   done := make(chan bool)

   go func() {
       defer func() {
           fmt.Println("Defer in function scope is being executed.")
           done <- true // 发送信号表示 defer 函数已执行
       }()
    
       {
          // 这是函数内的一个代码块
          defer func() {
             fmt.Println("Defer in code block scope is being executed.")
          }()
          fmt.Println("This is inside the code block.")
       } // 代码块结束
    
       // 注意，虽然代码块已经结束，但是代码块内的 defer 函数还没有被执行。
       // 它会在整个函数即将返回之前执行。
       fmt.Println("This is outside the code block, but still within the function.")

       // 函数的其他操作...
       time.Sleep(2 * time.Second) // 模拟函数执行时间
       }() // 函数结束
    
       // 等待接收来自匿名函数的信号
       <-done
    
       fmt.Println("The go routine has returned, and the main function is about to exit.")
   }
}
```
output:
```text
output:
This is inside the code block.
This is outside the code block, but still within the function.
Defer in code block scope is being executed.
Defer in function scope is being executed.
The go routine has returned, and the main function is about to exit.
```

可以看到，defer 函数不会在代码块结束时执行，而是在函数结束时执行。

### 4.3 defer 的参数求值时机
我们常常看到两种 defer 的使用方式
1. defer 直接接函数调用，例如
```go
defer recover()
```
2. defer 接一个匿名函数，例如
```go
defer func(){
    fmt.Printf("request done, result is xxx")
}()
   ```

两种方法的差异就是我同事所遇到问题的原因，这里暗含着 Golang defer 参数求值时机的问题，defer 的参数是在声明 defer 的时候就计算好的，而不是等到 defer 执行的时候才计算

回到同事向我提问的例子，执行下面的代码，我们会看到什么？
```go
// process 执行某项操作，并记录结果、错误（如果有的话）以及执行时长。
func process() (result string, err error) {
    start := time.Now()
    // 延迟调用 logReq 函数。注意此处的 result 和 err 是在 defer 语句执行时求值的。
    // 这意味着记录到的 result 和 err 将始终是它们的零值（""，nil），
    // 而不是 doSomething 返回的实际值。
    defer logReq(result, err, start)

    // 调用 doSomething 并将结果赋值给 result 和 err。
    result, err = doSomething()
    if err != nil {
       return "", err
    }

    return result, nil
}

// doSomething 模拟一个需要一些时间来完成的过程。
func doSomething() (string, error) {
    time.Sleep(time.Second) // 模拟执行任务通过休眠一秒。
    return "done", nil      // 返回成功的结果。
}

// logReq 记录 process 函数的执行结果、错误和耗时。
func logReq(result string, err error, start time.Time) {
    log.Printf("result: %s, err: %v, time: %vms", result, err, time.Since(start).Milliseconds())
}

func main() {
    process()
}
```
output:
```text
2024/04/25 13:11:50 result: , err: <nil>, time: 1001ms
```
在这段代码中，`defer logReq(result, err, start)` 的参数在 defer 声明的时候就拷贝了一份，此时 result 为空字符串，自然在执行 logReq 时，打印出来的 result 就不是预期的 "done"



而修复这个问题的方法也很简单，只需要使用一个匿名函数把 logReq包起来即可，示例如下
```go
defer func() {
    logReq(result, err, start)
}()

output:
2024/04/25 13:52:15 result: done, err: <nil>, time: 1001ms
```
此时执行代码，就能打印出 result 实际的值啦，这就是 defer 的参数求值实际问题。

## 5. 结尾
综上，本文讨论了 Golang defer 函数的作用，以及使用时需要注意的三个细节。由于本人对 Golang 底层的运行机制尚不了解，本文不涉及 defer 底层的执行机制，感兴趣的朋友可以阅读本文的参考来源。

如果有什么想要讨论的话题，或者对我的内容有不同的意见，欢迎留下你的评论，谢谢！

## 6. 参考
- 关于 Golang 语言 defer 的底层实现机制，我对这块不太熟悉，[这篇文章](https://draveness.me/golang/docs/part2-foundation/ch05-keyword/golang-defer/)写的很好
- [这篇文章](https://tiancaiamao.gitbooks.io/go-internals/content/zh/03.4.html) 提到了一个简便的确认 defer 执行逻辑的方法