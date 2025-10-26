# 🧩 make_transparent_background_svg

一个 Python 实用工具，用于将 **SVG 文件中接近白色填充的矩形（ `<rect>` ）区域设置为透明填充**。纯白色将完全透明，颜色越深则越不透明。  
适合处理由 [Dithering Studio](ditheringstudio.com) 生成的“像素块” `.svg` 矢量文件。

---

## ✨ 功能特性

- ✅ 自动分析每个 `<rect>` 元素的填充颜色 (`fill`)
- 🎨 根据与白色的距离动态计算透明度
- ⚙️ 支持命令行参数指定输入/输出文件
- 🔧 提供可调节的亮度阈值（`--threshold`）

---

## 📦 系统要求

- `Python 3.7` 或更高版本
- 无需额外安装任何依赖

---

## 🚀 使用方法
下载或复制 `make_transparent_background_svg.py` 文件即可直接使用。


### 命令

```bash  
python make_transparent_background_svg.py <输入文件> <输出文件>  
```

### 示例
```bash
python make_transparent_background_svg.py input.svg output.svg
```

### 调整亮度阈值
默认亮度阈值为 `180`，只有高于这个阈值的填充色才会被修改为透明填充。  
可通过 `--threshold` 参数调整对“接近白色”的判定标准。
```bash
python make_transparent_background_svg.py input.svg output.svg --threshold 200
```

---
## 📄 输出示例

```text
✅ 已处理文件: input.svg
📄 输出文件: output.svg
🔹 修改的 rect 元素数量: 142
🔧 使用的亮度阈值: 190
```

输出文件将保留所有原始 SVG 结构，仅添加或修改了 `fill-opacity` 属性。

---