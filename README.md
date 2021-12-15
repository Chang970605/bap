# sppwp and bap

## 2d-sppwp
* 建立线性规划模型，并建立gurobi求解 12.1
* gurobi求解成功，实验了c的数据集，发现求解过程过慢，后面可以直接考虑用算法对比，或者设置实验时间上限 12.2
* 趋势图符合预期，画图时发现有的箱子有重叠，问题出现在一个很大的数上，下一步考虑符合预期w,h同序的箱子，看运行时间 12.5
* 解决为什么不同的偏好位置造成不同的答案，px自身有大于等于0的限制 12.7
* 开始设计启发式算法 12.10
* 编写好三个启发式算法 12.11
* beam_search编写完毕，有一个好处是可以根据alpha的大小得到不同的答案 12.13

## baps
* 写出规划模型，并编写gurobi