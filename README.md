# 机器学习算法课程论文材料

## 内容
- 实验代码/run_experiment.py`：复现实验脚本
- `实验代码/requirements.txt`：关键 Python 依赖
- `实验结果/metrics.json`：汇总指标、配置与混淆矩阵
- `实验结果/raw_predictions.json`：留出测试集真实标签、预测标签和混淆矩阵

## 复现
Python 3.12 环境安装依赖后，在项目根目录执行：

```powershell
python -m pip install -r 实验代码/requirements.txt
python 实验代码/run_experiment.py
```

数据来自 scikit-learn 内置 `load_digits` 数据集。数据划分固定 `random_state=42`，按类别分层；超参数仅在训练集内进行五折分层交叉验证。测试集用于最终评估。

## 结果说明
主要测试结果：标准化 RBF-SVM 与 PCA+RBF-SVM 的准确率均为 98.22%，宏平均 F1 均为 98.21%。PCA 保留 54 个成分和约 99.14% 方差，没有提高测试性能。论文保留这一真实结果，不将负结果描述为性能提升。耗时只供本机参考。
