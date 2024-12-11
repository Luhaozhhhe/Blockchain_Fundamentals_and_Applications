# 第六次实验报告 文件说明

**本次实验提交的代码如下所示，重点修改部分已经加粗标注。**

==***注意！本组提交时，为了保持文件的整齐，所以调整了部分文件的位置，所以可能会与报告中的文件路径对不上，特此说明。***==

- artifacts
  - **proof_factor.json：了解circom部分生成的proof代码**
  - **proof_spend.json：赎回部分生成的proof代码**
  - **verification_key_factor.json：了解circom部分生成的verification代码**
  - **verification_key_spend.json：赎回部分生成的verification代码**
  - **writeup.md：了解circom部分所填写的三个问题**
- circuits
  - **example：下面存放了了解circom部分生成的文件**
    - circuit.json
    - input.json
    - proof.json
    - proving_key.json
    - public.json
    - verification_key.json
    - witness.json
  - example.circom：未改动
  - mimc.circom：未改动
  - **spend.circom：编写了IfThenElse函数、SelectiveSwitch函数和Spend函数**
- src
  - **compute_spend_inputs.js：编写了computeInput函数**
  - input.json：生成的输入脚本，没啥用
  - mimc.js：未改动
  - sparse_merkle_tree.js：未改动
  - transcript_gen.zsh：未改动
- test
  - circuits
    - **spend10：存储了赎回部分生成的文件**
      - circuit.json
      - input.json
      - proof.json
      - proving_key.json
      - public.json
      - verification_key.json
      - witness.json
    - 后面9个文件均没有改动，不再列举
  - compute_spend_inputs：未改动，下面有八个文件，不一一列举了
  - compute_spend_inputs.js：未改动
  - if_then_else.js：未改动
  - mimc.js：未改动
  - selective_switch.js：未改动
  - sparse_merkle_tree.js：未改动
  - spend.js：未改动
  - util.js：未改动
- Makefile：编译项目
- package.json：没啥用
- package-lock.json：没啥用



