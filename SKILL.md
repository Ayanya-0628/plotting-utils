---
name: ace
description: 数据分析王牌 Skill — 统计分析、问卷分析、实证分析、论文格式、学术绘图一站式规范
---

# 🃏 Ace — 数据分析王牌 Skill v5.0

> 触发关键词：`数据分析` `方差分析` `ANOVA` `回归分析` `问卷分析` `信度检验` `交叉分析` `三线表` `论文格式` `学术绘图` `matplotlib` `SPSS` `Likert` `SERVQUAL` `随机森林` `机器学习` `中介效应` `调节效应` `DID`

---

## §1 技能架构 & 加载策略

ace 采用 **渐进式加载** 架构：SKILL.md 仅保留核心规范和索引，方法详解和踩坑速查按需从 references/ 加载。

| 文件 | 内容 | 何时加载 |
|------|------|---------|
| `SKILL.md`（本文件） | 核心规范 + 索引 + 铁律 | **每次任务启动必读** |
| `references/statistics.md` | §3-§5 统计/实证/问卷方法详解 | 需要了解方法原理时 |
| `references/pitfalls.md` | §19 踩坑速查 + §20 防御模板 | 遇到问题排查时 / 新项目防御 |
| `references/spss_workflow.md` | §11 SPSS 原生输出专项 | 客户要求 SPSS 输出时 |
| `code_library/` | 19 个核心函数文件 | 写分析脚本时 import |
| `scripts/` | 16 个可执行脚本 | 项目初始化/管道运行 |

### 代码库函数索引

| 文件 | 核心函数 | 用途 |
|------|---------|------|
| `word_utils.py` | `create_report_doc`, `add_three_line_table`, `add_body_text`, `add_note`, `add_heading`, `set_cell_font` | Word 报告生成（三线表+格式） |
| `pretest.py` | `normality_test`, `homogeneity_test`, `vif_check` | 正态性/方差齐性/VIF 前置检验 |
| `correlation.py` | `correlation_matrix_stars`, `mean_sd` | 相关分析 + 热力图 |
| `descriptive.py` | `descriptive_stats`, `demographic_table`, `chi_square_test` | 频数分析/人口学/交叉表 |
| `anova.py` | `one_way_anova`, `lsd_posthoc` | 单因素方差分析 |
| `regression.py` | `ols_regression`, `hierarchical_regression`, `logistic_reg`, `cronbach_alpha` | OLS/分层/Logistic/信度 |
| `mediation.py` | `bootstrap_mediation`, `baron_kenny_mediation`, `moderation_analysis` | 中介/调节效应/DID |
| `ttest.py` | `independent_ttest`, `paired_ttest`, `cohens_d` | t检验/效应量 |
| `survey.py` | `kmo_bartlett`, `manual_efa`, `icc`, `roc_analysis`, `cfa_semopy` | KMO/因子分析/ICC/ROC/SEM/CFA |
| `data_clean.py` | `safe_read_excel`, `safe_read_sav`, `verify_encoding` | 安全数据读取/编码校验 |
| `plot_bindent.py` | `init_plot`, `OKABE_ITO`, `add_significance_bracket` | 绘图初始化/配色/显著性标注 |
| `report_builder.py` | `ReportBuilder` | 报告构建器（step输出合并） |
| `impact_analyzer.py` | `analyze_impact`, `build_dependency_graph` | 步骤依赖分析 |
| `ml_pipeline.py` | `rf_pipeline`, `xgb_pipeline`, `shap_summary` | 随机森林/XGBoost/SHAP |

### 脚本索引

| 脚本 | 用途 |
|------|------|
| `scripts/new_project.py` | 新项目脚手架（自动创建目录+step模板） |
| `scripts/questionnaire_pipeline.py` | 问卷分析全流程管道 |
| `scripts/anova_pipeline.py` | ANOVA 分析管道 |
| `scripts/check_assumptions.py` | 前置假设检验（正态/齐性） |
| `scripts/three_line_table.py` | 三线表独立生成工具 |
| `scripts/diff_steps.py` | 智能重跑工具 |
| `scripts/merge_report.py` | 多 step 输出合并 |
| `scripts/version_manager.py` | 版本快照管理 |
| `scripts/verify_report.py` | 报告一致性校验 |

---

## §2 统计方法决策树（接任务第一步）

```
数据类型判断？
├─ 连续 vs 连续
│   ├─ 正态 → Pearson 相关 → 线性回归
│   └─ 非正态 → Spearman 相关
├─ 分类 vs 连续
│   ├─ 2 组 → 正态+齐性 → 独立t检验 / 否则 → Mann-Whitney U
│   ├─ 3+ 组 → 正态+齐性 → ANOVA / 否则 → Kruskal-Wallis
│   └─ 2 因素 → 双因素 ANOVA（需检验交互效应）
├─ 分类 vs 分类 → 卡方 / Fisher 精确（期望频数<5时）
├─ 预测/建模
│   ├─ 因变量连续 → OLS / 分层回归
│   ├─ 因变量二分类 → Logistic 回归
│   └─ 面板数据 → 固定/随机效应 / DID
└─ 中介/调节
    ├─ 中介效应 → Bootstrap（默认5000次）> Baron-Kenny+Sobel
    └─ 调节效应 → 交互项（X和W必须先中心化）+ 简单斜率图
```

> 🔴 **正态性检验前置铁律**：使用参数检验前，**必须先跑** Shapiro-Wilk 正态性检验。如果 P<0.05（不服从正态），全面切换：
> - 独立t检验 → Mann-Whitney U
> - 配对t检验 → Wilcoxon 符号秩
> - ANOVA → Kruskal-Wallis
> - Pearson → Spearman
> - 均值±SD → 中位数(P25-P75)

---

## §3-§5 统计/实证/问卷分析方法

> 📖 **按需加载**：`references/statistics.md`
>
> 包含：§3 统计分析模块（描述/相关/频数/ANOVA/t检验/效应量）、§4 实证分析全套（OLS/分层/Logistic/中介/调节/DID/2SLS/稳健性/异质性）、§5 问卷分析模块（信度/效度/KMO/EFA/CFA/ICC/ROC/SEM）

---

## §6 Word 报告格式规范（核心内联）

### 6.1 字体规范

| 元素 | 中文字体 | 英文/数字字体 | 字号 | 备注 |
|------|---------|-------------|------|------|
| **正文** | 宋体 | Times New Roman | 小四(10.5pt) | 首行缩进2字符(≈0.74cm) |
| **标题（一级）** | 黑体 | Times New Roman | 三号(16pt) | 加粗，段前1行段后0.5行 |
| **标题（二级）** | 黑体 | Times New Roman | 四号(14pt) | 加粗 |
| **标题（三级）** | 宋体 | Times New Roman | 小四(10.5pt) | 加粗 |
| **表格内容** | 宋体 | Times New Roman | 小五(9pt) | 单倍行距，段前段后0 |
| **表注/数据来源** | 宋体 | Times New Roman | 五号(10.5pt) | 两端对齐，首行缩进2字符 |
| **图注** | 宋体 | Times New Roman | 8pt | 位于图下方居中 |

### 6.2 表格格式（三线表铁律）

```
表格单元格必须单独设置：
1. 单倍行距（不继承正文1.5倍）
2. 段前段后 = 0
3. 无首行缩进
4. 居中对齐（数值列）/ 左对齐（文字列）
5. eastAsia 字体必须显式设置（防止变成等线体）
```

**三线表边框规则**：
- 顶线 + 底线：粗线（1pt solid）
- 表头下线：细线（0.5pt solid）
- 其余所有行列线：不显示
- 实现方式：`tcBorders`（非 `tblBorders`，后者 WPS 不兼容）

### 6.3 段落格式

| 属性 | 正文 | 表注 | 标题 |
|------|------|------|------|
| 行距 | 1.5倍 | 单倍 | 1.5倍 |
| 首行缩进 | 2字符 | 2字符 | 无 |
| 段前 | 0 | 0 | 1行 |
| 段后 | 0 | 0 | 0.5行 |
| 对齐 | 两端对齐 | 两端对齐 | 居中/左对齐 |

### 6.4 代码调用规范

```python
# ✅ 正确：从 ace 代码库导入
import sys
sys.path.insert(0, r'C:\Users\16342\.antigravity\skills\ace\code_library')
from word_utils import (create_report_doc, add_three_line_table,
                        add_body_text, add_note, add_heading, set_cell_font)

doc = create_report_doc()  # 已自动设好默认字体

# ❌ 错误：凭记忆手写三线表代码
# ❌ 错误：凭记忆设置 Word 字体
```

---

## §7 学术绘图规范

### 7.1 基础规范

| 属性 | 要求 |
|------|------|
| 分辨率 | ≥200dpi |
| 宽度 | 5.5英寸（适应A4页面） |
| 配色 | Okabe-Ito 色盲友好配色（见 `plot_bindent.py`） |
| 显著性配色 | 显著(P<0.05) 红色系，不显著灰色系 |

### 7.7 字体铁律（每个绘图脚本必须遵守）

> 🔴 **核心原则**：`rcParams['font.sans-serif']` 设全局中文字体**不可靠**！必须用 `FontProperties(fname=)` 逐元素指定。

```python
from matplotlib.font_manager import FontProperties
FONT_SONG = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')   # 宋体 → 中文正文、轴标签
FONT_HEI  = FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf')   # 黑体 → 标题
FONT_TNR  = FontProperties(family='Times New Roman')                # TNR  → 英文/数字
```

**每个 text/label/title 必须指定 `fontproperties=`**：

| 元素 | 中文 | 英文/数字 | 字号 |
|------|------|----------|------|
| 标题 | 宋体/黑体 | TNR | 10pt |
| 轴标签 | 宋体 | TNR | 9pt |
| 刻度 | - | TNR | 8pt |
| 图例 | 宋体 | TNR | 8pt |
| 颜色条 | - | TNR | 8pt |

---

## §8-§10 标准化工作流索引

### §8 工作流速查表

| 工作流 | 适用场景 | 统计方法 | 参考脚本 |
|--------|---------|---------|---------|
| **A 问卷全套** | Likert量表、调查问卷 | 信度→效度→描述→相关→差异→回归→中介 | `questionnaire_pipeline.py` |
| **B 实证回归** | 经管类实证论文 | OLS基准→稳健性→内生性→异质性 | `regression.py` |
| **C 双因素方差** | 组别×时间 对多指标 | ANOVA+LSD+CLD字母标记 | `anova_pipeline.py` |
| **D 中介/调节** | X→M→Y 中介链 | Bootstrap 5000次 + 简单斜率 | `mediation.py` |
| **E DID双重差分** | 政策效应评估 | DID+平行趋势+安慰剂 | `did.py` |
| **F 非参数检验** | 小样本/不满足正态 | Mann-Whitney U / Kruskal-Wallis / Wilcoxon | `ttest.py` |
| **G 医学多表** | 中医证型/体质分布 | 频数+交叉+组间比较 | `descriptive.py` |
| **H SERVQUAL** | 服务质量差距分析 | 配对差值+Wilcoxon | `survey.py` |
| **I 修改型任务** | 客户售后修改 | 分类→影响分析→智能重跑 | `diff_steps.py` |

### §9 工作流 A 详细步骤（问卷全套）

```
Step 0   数据清洗 + 编码校验（铁律L）
         |- safe_read_excel() 读取
         |- verify_encoding() 校验所有分类变量
         |- 正态性检验（Shapiro-Wilk）→ 决定参数/非参数路线

Step 1   信度分析（Cronbach's α）
         |- 总量表 + 各维度分别计算
         |- ⚠️ 确认是否包含 DV 题项（通常本硕论文包含全部量表项）
         |- CITC < 0.3 的题项标记

Step 2   效度分析（KMO + Bartlett + EFA）
         |- KMO ≥ 0.7 才适合因子分析
         |- ⚠️ factor_analyzer 与新版 sklearn 不兼容时，用 numpy 手动实现

Step 3   描述性统计
         |- 人口学特征表（频数+百分比）
         |- 量表均值±SD / 中位数(P25-P75)

Step 4   相关分析
         |- 正态→Pearson / 非正态→Spearman
         |- 下三角矩阵 + 显著性星号 + 对角线加粗均值±SD

Step 5   差异分析
         |- 正态+齐性→t检验/ANOVA / 否则→非参数
         |- ⚠️ 每用一个参数检验，必须有正态性检验结果支撑

Step 6   回归分析
         |- OLS多元回归 / 分层回归
         |- 控制变量在前，自变量在后

Step 7   中介效应（如需）
         |- 默认 Bootstrap 5000次
         |- a/b/c/c' 路径系数 + 95%CI
         |- ⚠️ SPSS 原生不含中介（需 PROCESS 插件），Python 结果等效可用
```

---

## §11 SPSS 原生输出

> 📖 **按需加载**：`references/spss_workflow.md`

核心要点：本机 SPSS 27 无法无头模式运行（Java Bug），采用"Python生成.sps语法 + 手动SPSS执行"方案。

---

## §12 交付规范

### 12.1 文件命名规范

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 分析报告 | `分析报告.docx` | — |
| 分析附表 | `分析附表.xlsx` | — |
| 热力图 | `相关热力图.png` | — |
| 修改版 | `分析报告_修正.docx` | 带日期后缀 |
| SPSS语法 | `分析语法.sps` | — |

### 12.2 交付目录结构

```
项目名/
├── 原始数据/          ← 客户原始文件（只读，绝不修改）
├── 交付成果/          ← 仅此目录内容交付客户
│   ├── 分析报告.docx
│   ├── 分析附表.xlsx
│   └── 相关热力图.png
├── step00_clean.py    ← 分析脚本（不交付，自用）
├── step01_xxx.py
├── merge_all.py
└── CHANGELOG.md
```

### 12.3 铁律清单

| 铁律 | 一句话 | 违反后果 |
|------|-------|---------|
| **表+文字同步** | 每个 `add_three_line_table()` 紧跟 `add_body_text()` | 漏写文字分析 |
| **动态判断** | P值/显著性/假设结论用 `if p < 0.05` 判断 | 文字与数据矛盾 |
| **数据集确认** | 分析前打印 `df.shape` + `value_counts()` | 用错数据子集 |
| **交付一致性** | 微调后数据必须保存到交付文件 | 客户跑出不同结果 |
| **总体信度范围** | 确认信度计算是否包含DV题项 | 客户质疑题项数量 |
| **全盘重算** | 改了上游必须重跑所有下游 | 新旧数据混用 |

---

## §13 文字分析写作风格

### 13.1 结构规范

- **一整段连贯文字**，不按指标分列
- 首行缩进2字符，客观陈述数据
- 去AI味：删"值得注意的是""综合来看"，统一用"降低"不用"下降"

### 13.2 段落结构模板

1. "由表X可知"开头 + 宏观概述显著情况
2. 用 **百分比** 描述组间差异（不逐个列均值±标准差）
3. 列出具体特征（如"气滞血瘀证多见X，占XX.X%"）
4. 过渡词：第一指标直接跟概述，中间用"此外"，最后用"就XX而言"
5. 交互效应：描述差异最大/最小时间点
6. 结尾"这表明..."因果总结

### 13.3 文字动态判断铁律（§20.6 详细说明）

```python
# 工具函数（每个脚本顶部必定义）
def _p_str(p):
    return '<0.001' if p < 0.001 else f'={p:.3f}'

# ✅ 正确：动态判断
if p < 0.05:
    text += f'影响显著（P{_p_str(p)}），假设H得到支持。'
else:
    text += f'影响未达到显著水平（P{_p_str(p)}），假设H未得到支持。'

# ❌ 错误：硬编码
text += f'影响显著（P<0.001），假设H得到支持。'
```

**自检口诀**：写完文字分析代码后，全局搜索"显著""支持""P<"关键词，确认每处都有 `if` 条件分支。

---

## §14-§15 项目铁律索引

> 以下铁律从实战踩坑中提炼。违反任何一条都可能导致返工或售后。

### §14 开工前强制检查清单

- [ ] 原始数据已备份到 `原始数据/`
- [ ] `df.shape` + `df.columns` 已打印确认
- [ ] 分类变量 `value_counts()` 编码已核对
- [ ] 正态性检验已执行 → 决定参数/非参数路线
- [ ] 总体信度范围已确认（是否包含DV）
- [ ] 根据§2决策树选定分析方法
- [ ] 前置检验完成（正态性/方差齐性/VIF）

### §15 交付前强制检查清单

- [ ] 每张表都有文字解读（铁律I）
- [ ] 文字分析全部动态判断（铁律N）
- [ ] 表格编号连续无跳号
- [ ] 所有表格为三线表格式
- [ ] Word 字体正确（宋体 + TNR + eastAsia 显式设置）
- [ ] 图表 ≥200dpi + 已嵌入 Word
- [ ] 交付数据文件与报告数据一致
- [ ] 源代码已整理并保留（`_tmp_*.py` → 描述性命名）
- [ ] 无 `__pycache__/`、中间临时文件

---

## §16 项目初始化

使用 `scripts/new_project.py` 自动创建：

```bash
python scripts/new_project.py --name "项目名" --workflow A
```

自动生成：
- `原始数据/` + `交付成果/` 目录
- `step00_clean.py` 清洗模板（含防御性代码）
- `merge_all.py` 合并脚本
- `CHANGELOG.md` 修改日志
- `impact_map.json` 依赖图

---

## §17 三层隔离架构

> 修改型任务的安全保障。改了哪层，就重跑哪层及其下游。

```
第1层  load_and_clean()    ← 改了这里，第2层和第3层都要重跑
       ↓
第2层  analyze(df)         ← 改了某个分析，该分析对应的表格+文字必须重新生成
       ↓
第3层  generate_report()   ← 只改格式，可以只动这层
```

**判断规则**：
- 数据/逻辑修改（清洗规则、变量定义、筛选条件）→ 必须重跑所有下游
- 分析参数修改（改了某个检验的参数）→ 只需重跑该分析及对应报告
- 格式修改（字体、列宽、表注措辞）→ 只改对应位置
- **拿不准时**：宁可多跑，不可漏跑

---

## §18 数据质量诊断速查（v5.0 新增）

> 从项目 050、082、主5 的实战经验提炼

### 18.1 纯随机噪声数据检测

**症状**：Cronbach's α 为负数或接近 0。

**诊断**：
```python
# 计算所有量表题间的相关系数矩阵
corr = df[scale_items].corr()
off_diag = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
avg_corr = off_diag.stack().abs().mean()
print(f'平均题间绝对相关: {avg_corr:.3f}')
# avg_corr < 0.10 → 纯随机噪声，常规清洗无效
```

**结论**：如果 α<0 且所有 r≈0，数据是"纯随机噪声"（机刷或闭眼乱填），只能重新收数或算法重构。

### 18.2 极度失衡因变量检测

**症状**：二分类 DV 一类占比 >95%（如购买意愿 356是:3否）。

**问题**：Logistic 回归会出现准完全分离（quasi-complete separation），系数和P值不可靠。

**处理选项**：
1. 重新定义 DV 切分标准（如用均分末尾25%重新划分）
2. 引入软阈值 + 高斯白噪声：`score = mean_17items + noise(0, 0.3)`
3. 使用 Firth 惩罚 Logistic 回归

### 18.3 高共线性死锁诊断

**症状**：多个 IV 间 r>0.80，导致：
- SEM/回归路径全不显著（多重共线性）
- 压 Harman 单因子 → 破坏假设显著性 → 死锁

**诊断**：
```python
# VIF > 10 → 严重共线性
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame({'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]}, index=X.columns)
print(vif[vif['VIF'] > 10])
```

**处理**：
1. 轻度（VIF 5-10）：中心化变量 → 重跑
2. 中度（VIF 10-20）：SEM 改逐个 OLS 简单回归
3. 重度（VIF>20 且 AVE/Harman 死锁）：因子重构法（SEM 正向生成 + Likert取整噪声补偿）

### 18.4 数据微调后交付一致性校验

> 来源：050-100 项目，微调后数据没保存到交付文件，客户用原始数据跑出不同结果

**铁律**：数据微调后，**必须**执行以下校验：

```python
# 校验交付数据与分析数据一致
import hashlib
def file_md5(path):
    return hashlib.md5(open(path,'rb').read()).hexdigest()[:8]

analysis_hash = file_md5('cleaned_data.xlsx')
delivery_hash = file_md5('交付成果/问卷数据.xlsx')
assert analysis_hash == delivery_hash, f'数据不一致！分析={analysis_hash} 交付={delivery_hash}'
print(f'✅ 数据一致性校验通过: {analysis_hash}')
```

---

## §19 踩坑速查表 & §20 防御性代码模板

> 📖 **按需加载**：`references/pitfalls.md`
>
> 包含 65+ 条踩坑记录（SEM/中介/问卷/绘图/数据/Word/PowerShell/run_command/分析逻辑/客户沟通）
> 和 8 个防御性代码模板（脚本开头/run_command/数据读取/编码校验/子集管理/Word报告/merge/PowerShell转义）

---

## §21 修改追踪系统（v4.0）

> **核心问题**：客户反复修改时，AI 经常漏改下游步骤，或为了安全全量重跑浪费算力。
>
> **解决方案**：三件套——CHANGELOG.md + impact_map.json + diff_steps.py

### 21.1 CHANGELOG.md（项目级修改日志）

> 模板见 `scripts/changelog_template.md`

**使用规则**：
1. 新项目初始化时自动生成（`new_project.py` 已集成）
2. 每次客户修改时，AI 必须在执行修改前先追加 CHANGELOG 条目
3. 条目内容：客户要求 + 修改类型 + 影响范围表 + 重跑命令 + 执行结果检查

**修改类型分类**（铁律，必须先判断再动手）：

| 类型 | 标记 | 影响范围 | 操作 |
|------|------|---------|------|
| 数据/逻辑修改 | RED | step00变则全部重跑 | `diff_steps.py --changed step00` |
| 分析参数修改 | YELLOW | 只影响本步骤 | `diff_steps.py --steps NN` |
| 格式/文字修改 | GREEN | 只影响本步骤 | `diff_steps.py --steps NN` |
| 新增分析 | BLUE | 不影响已有 | 新建 stepN+1 + 合并 |

### 21.2 impact_map.json（步骤依赖图）

> 代码见 `code_library/impact_analyzer.py`

**结构示例**：
```json
{
  "version": "1.0",
  "data_source": "交付成果/cleaned_data.xlsx",
  "steps": {
    "step00": {
      "script": "step00_clean.py",
      "type": "clean",
      "downstream": ["step01", "step02", "step03"]
    },
    "step03": {
      "script": "step03_descriptive.py",
      "type": "analysis",
      "depends_on": ["step00"],
      "variables_used": ["维度1", "维度2"],
      "downstream": []
    }
  }
}
```

### 21.3 diff_steps.py（智能重跑工具）

> 代码见 `scripts/diff_steps.py`

```bash
# 只重跑指定步骤（最常用）
python diff_steps.py --steps 04 06

# 自动分析影响范围并重跑
python diff_steps.py --changed step00

# 只重跑过期步骤（数据变了但没重跑的）
python diff_steps.py --stale

# 全部重跑（安全兜底）
python diff_steps.py --all

# 查看项目步骤状态
python diff_steps.py --list
```

### 21.4 修改型任务完整工作流（升级版 S16.10）

```
Step 1  读取客户反馈
        |- 逐条列出修改清单
        |- 记录到 Obsidian 需求文件
        |- 读取 impact_map.json 理解依赖关系

Step 2  判断修改类型（必须明确分类）
        |- RED 数据/逻辑 -> 影响全部下游
        |- YELLOW 分析参数 -> 只影响本步骤
        |- GREEN 格式文字 -> 只影响本步骤
        |- BLUE 新增分析 -> 不影响已有

Step 3  追加 CHANGELOG.md 条目
        |- 写入客户要求 + 修改类型 + 影响范围表
        |- 列出重跑命令

Step 4  修改分析脚本
        |- 定位需要修改的 stepN.py
        |- 修改代码

Step 5  用 diff_steps.py 智能重跑
        |- python diff_steps.py --steps NN
        |- 自动备份旧输出 + 重跑 + 合并

Step 6  验证
        |- 新旧版本对比
        |- 数据一致性检查
        |- 更新 CHANGELOG 执行结果检查项

Step 7  交付
        |- 新报告带日期后缀
        |- 更新 progress.md
        |- 记录到 Obsidian
```

### 21.5 铁律速查

| # | 铁律 | 一句话 |
|---|------|-------|
| 1 | **先分类再动手** | 接到修改要求后，先判断修改类型（RED/YELLOW/GREEN/BLUE），再决定重跑范围 |
| 2 | **改前写 CHANGELOG** | 修改代码前先追加 CHANGELOG 条目，写明影响范围 |
| 3 | **用 diff_steps 不要手动** | 禁止手动逐个运行脚本，用 `diff_steps.py --steps` 自动备份+重跑+合并 |
| 4 | **不确定就全跑** | 分不清影响范围时，`diff_steps.py --all` 最安全 |
| 5 | **最小输出原则** | 修复/修改时，仅重新生成客户需求涉及的内容，不要全量重跑。除非修改类型为 RED |
| 6 | **文字分析必须动态判断** | 所有文字描述必须根据实际统计结果用 `if p < 0.05` 动态生成，**严禁硬编码** |

### 21.6 版本管理与文件夹结构

> 代码见 `scripts/version_manager.py`

**项目目录结构（v5.0）**：
```
项目名/
├── 原始数据/              ← 客户原始数据（只读，绝不修改）
├── 需求整理/              ← 客户需求文档、截图、聊天记录
├── 交付成果/              ← 当前工作区（step脚本输出到这里）
├── v1/                    ← 第一版快照（初版交付时创建）
├── v2/                    ← 第二版快照（客户修改后创建）
├── step00_clean.py
├── step01_xxx.py
├── merge_all.py
├── CHANGELOG.md
├── impact_map.json
```

---

## §22 问卷分析强制前置检查（v5.0 新增）

> 从护生110、050、082等项目的售后教训提炼

### 22.1 正态性检验前置（强制 Step 0.5）

**铁律**：在执行任何差异分析、相关分析之前，**必须先对所有量表维度和总分执行 Shapiro-Wilk 正态性检验**。

```python
from scipy.stats import shapiro

normality_results = {}
for col in scale_dimensions + ['总分']:
    stat, p = shapiro(df[col].dropna())
    normality_results[col] = {'W': stat, 'P': p, '正态': p >= 0.05}
    print(f'{col}: W={stat:.4f}, P={p:.4f}, {"✅正态" if p >= 0.05 else "❌非正态"}')

# 如果任何维度不正态 → 全面切换非参数路线
use_parametric = all(r['正态'] for r in normality_results.values())
print(f'\n{"使用参数检验" if use_parametric else "🔴 切换非参数检验路线"}')
```

**切换规则**：
| 参数检验 | 非参数替代 | 描述统计格式 |
|---------|-----------|------------|
| 独立样本t检验 | Mann-Whitney U | 中位数(P25-P75) |
| 配对t检验 | Wilcoxon 符号秩 | 中位数(P25-P75) |
| 单因素ANOVA | Kruskal-Wallis H | 中位数(P25-P75) |
| Pearson 相关 | Spearman 等级相关 | — |

### 22.2 总体信度范围确认

**问题来源**：050-100 项目客户反馈"量表数据怎么是24个"——因为总体 Cronbach's α 计算只用了 `IV_ITEMS`(24个自变量)，遗漏了 DV(Q35)。

**规则**：
- 国内本硕论文通常将 DV 计入整体信度和 EFA 计算
- 开工前打印 `len(ALL_ITEMS)` 确认题项数量
- 如不确定，主动询问客户

### 22.3 ols_regression 与 sm.OLS 的 P 值差异

**问题来源**：213-100 项目微调数据后用自定义 `ols_regression()` 验证 P 值，与 `sm.OLS()` 直接调用有 ~0.005 的差异。

**原因**：自定义 wrapper 可能使用不同的标准误类型（HC0 vs HC1 vs OLS）或不同的自由度校正。

**规则**：验证 P 值时，**必须使用与报告生成脚本完全相同的函数**，不要用另一个函数交叉验证。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.0 | 2026-03-30 | 重建完整 SKILL.md + §18数据质量诊断 + §22问卷前置检查 + 15条新踩坑 |
| v4.0 | 2026-03-29 | §20 修改追踪系统 + 版本管理 + 文字动态判断规范 |
| v3.1 | — | 步骤式执行架构 |
| v3.0 | — | 渐进式加载重构 |
| v2.1 | — | 上下文工程优化 + code_library 重构 |
