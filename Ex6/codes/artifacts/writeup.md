Name: [陆皓喆，张泽睿]

## Question 1

In the following code-snippet from `Num2Bits`, it looks like `sum_of_bits`
might be a sum of products of signals, making the subsequent constraint not
rank-1. Explain why `sum_of_bits` is actually a _linear combination_ of
signals.

```
        sum_of_bits += (2 ** i) * bits[i];
```

## Answer 1

此处的`bits[i]`表示的是我们输入的二进制的第i位，前面的因数`(2 ** i)`表示的是2的i次方。
这一行代码的目的是，将每一位上的二进制数都乘上对应的权重，然后最后将这些值都加起来，最终我们可以得到二进制数的十进制表示。
实际上，我们的`bits[i]`被定义为一个信号，但是我们的`(2 ** i)`并不是一个信号，他只是一个常数，对于线性组合来说，它是常数和信号的乘积之和，而这里的`(2 ** i) * bits[i]`就是常数`(2 ** i)`和信号`bits[i]`的乘积。
因此，`sum_of_bits`是输入位的线性组合，而不是信号的乘积。

## Question 2

Explain, in your own words, the meaning of the `<==` operator.

## Answer 2

`<==`这个符号实际上是`<--`和`===`这两个运算符的结合。首先，它分配了一个值给信号，然后`===`说明了我们在分配的过程中派生的合同成立。
这是一种快捷方式，允许我们在使用两个运算符的时候替换成单独的一个运算符。

举个例子，在`example.circom`中，语句`binaryDecomposition.in <== in`就使用了该语句，意思是将输入信号in的值赋给子电路 `binaryDecomposition`的输入信号，并同时约束`binaryDecomposition.in`等于`in`。



## Question 3

Suppose you're reading a `circom` program and you see the following:

```
    signal input a;
    signal input b;
    signal input c;
    (a & 1) * b === c;
```

Explain why this is invalid.

## Answer 3

我们的a、b和c都是电路信号，第四行代码对信号a做了位运算。而在`circom`中，信号的赋值与约束操作是分开进行的，我们不能直接在赋值语句中使用位运算。

所以，我们应该对其进行修改，才能使用。具体的修改方法：
首先，通过 `a <== (a & 1) * b` 语句来完成我们的位运算，并且将结果乘上b。接着再使用约束语句 `c === a` 来完成我们的赋值操作。
