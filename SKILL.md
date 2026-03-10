---
name: plotting-utils
description: 科研绘图脚本库 + 出版级可视化标准。包含 R/Python 绘图模板、期刊投稿规范、色盲友好配色、多子图排版、图表导出工具。
---

# Plotting Utils - 科研绘图与出版级可视化

## 概述
本 skill 融合了两个核心能力：
1. **常用绘图脚本模板**（R + Python），覆盖极坐标图、柱状图、热力图等
2. **出版级可视化标准**（来自 [AcademicForge/scientific-visualization](https://github.com/HughYau/AcademicForge)），确保图表达到期刊投稿标准

## 目录结构
```
plotting-utils/
├── SKILL.md                    # 本文档
├── README.md                   # 脚本清单与使用说明
├── scripts/
│   ├── R/
│   │   └── polar_bar_chart.R   # 极坐标柱状图（circlize）
│   └── Python/
│       ├── figure_export.py    # 图表导出工具（多格式、期刊规范）
│       └── style_presets.py    # 预设样式（Nature/Science/Cell等）
├── assets/
│   ├── color_palettes.py       # 色盲友好配色方案（Okabe-Ito等）
│   ├── publication.mplstyle    # 通用出版级样式
│   ├── nature.mplstyle         # Nature 期刊样式
│   └── presentation.mplstyle  # 演示/海报样式（大字号）
└── references/
    ├── color_palettes.md       # 配色方案详细指南
    ├── journal_requirements.md # 期刊投稿尺寸/DPI/格式要求
    ├── matplotlib_examples.md  # 10个完整绘图实例
    └── publication_guidelines.md # 出版级图表最佳实践
```

## 触发场景
- 用户提到"画图""plot""绘图模板""极坐标图""circlize"时自动关联
- 用户要求复用之前的绘图代码时，优先从本 skill 查找
- 用户提到"出版级""投稿""期刊图表""colorblind""色盲友好"时触发
- 用户要求"导出PDF""导出高分辨率""300DPI"时触发
- 用户提到"Nature风格""Science格式""期刊规范"时触发

---

## 第一部分：出版级可视化标准

### 核心原则

#### 1. 分辨率与文件格式
- **矢量图**（图表/线图）：优先使用 PDF/EPS/SVG
- **位图**（显微镜照片等）：300-600 DPI，TIFF/PNG
- ❌ **永远不要**用 JPEG 保存科研图表

#### 2. 色盲友好配色
**默认使用 Okabe-Ito 配色方案**（8色，对所有类型色盲均可辨别）：
```python
from assets.color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')
# 或手动指定
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
```

**热力图/连续数据**：
- ✅ 使用感知均匀色图：`viridis`, `plasma`, `cividis`
- ❌ 禁止使用 `jet` 或 `rainbow`

#### 3. 字体规范
- 无衬线字体：Arial, Helvetica, Calibri
- 最小字号（最终印刷尺寸）：
  - 坐标轴标签：7-9 pt
  - 刻度标签：6-8 pt
  - 子图标签：8-12 pt（加粗）

#### 4. 期刊尺寸要求
| 期刊 | 单栏宽度 | 双栏宽度 |
|------|---------|---------|
| Nature | 89 mm | 183 mm |
| Science | 55 mm | 175 mm |
| Cell | 85 mm | 178 mm |

详见 `references/journal_requirements.md`。

#### 5. 统计严谨性
**每张图必须包含**：
- 误差线（标注是 SD、SEM 还是 CI）
- 样本量 n
- 显著性标记（*, **, ***）
- 尽可能展示个体数据点

### 快速使用

```python
# 1. 应用期刊样式
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# 2. 绘图...

# 3. 导出
from figure_export import save_for_journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

### 出版前 Checklist
- [ ] 分辨率 ≥ 300 DPI
- [ ] 正确的文件格式（矢量/TIFF）
- [ ] 尺寸符合期刊规范
- [ ] 所有文字 ≥ 6pt 可读
- [ ] 色盲友好配色
- [ ] 灰度下可辨别
- [ ] 坐标轴标签含单位
- [ ] 有误差线并在图注中说明
- [ ] 子图标签（A, B, C...）一致
- [ ] 无多余装饰（3D效果、渐变等）
- [ ] 字体全文统一
- [ ] 显著性标记清晰

---

## 第二部分：绘图脚本库

### R 脚本

| 文件名 | 用途 | 依赖包 | 说明 |
|--------|------|--------|------|
| `polar_bar_chart.R` | 极坐标柱状图 | circlize, readxl, grid, showtext | circlize 环形柱状图，多品种多分组，PDF 导出 |

### Python 脚本

| 文件名 | 用途 | 依赖 | 说明 |
|--------|------|------|------|
| `figure_export.py` | 图表导出工具 | matplotlib | 多格式导出、期刊规范检查、DPI控制 |
| `style_presets.py` | 预设样式 | matplotlib | Nature/Science/Cell等期刊一键配置 |

## 使用方法

### 调用方式
1. 当用户需要某类图表时，先在 `scripts/` 下查找现成模板
2. 如果找到，复制模板到工作目录并修改参数
3. 如果未找到，根据需求新建，完成后保存到 `scripts/R/` 或 `scripts/Python/`
4. **所有新绘图默认遵循出版级标准**（配色、字号、分辨率）

### 新增脚本规则
- R 脚本放入 `scripts/R/`
- Python 脚本放入 `scripts/Python/`
- 文件名使用英文小写 + 下划线，如 `correlation_heatmap.py`
- 头部必须包含注释：用途、依赖、输入输出、参数说明
- 新增后同步更新本文档脚本清单

### 常见错误避免
1. ❌ 字体太小（印刷尺寸下不可读）
2. ❌ JPEG 格式（产生压缩伪影）
3. ❌ 红绿配色（约8%男性无法区分）
4. ❌ 低分辨率（印刷模糊）
5. ❌ 缺少单位（坐标轴必须标注）
6. ❌ 3D效果（扭曲感知）
7. ❌ 过多装饰（移除多余网格线）
8. ❌ 截断坐标轴（柱状图须从0开始，除非有科学依据）
9. ❌ 不一致的样式（同篇论文不同图用不同字体/颜色）
10. ❌ 缺少误差线

## 致谢
出版级可视化标准部分来自 [HughYau/AcademicForge](https://github.com/HughYau/AcademicForge)，MIT 许可证。

## GitHub 仓库
- 地址：https://github.com/Ayanya-0628/plotting-utils
- 每次新增或修改脚本后自动提交推送
