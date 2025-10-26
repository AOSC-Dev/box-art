#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_transparent_background_svg.py
---------------------------------
一个小型命令行工具，用于将 SVG 文件中接近白色的矩形 (rect) 元素设置为透明背景。
白色像素会完全透明，距离白色“越远”，则越不透明。

使用方式:
    python make_transparent_background_svg.py input.svg output.svg [--threshold THRESHOLD]

示例:
    python make_transparent_background_svg.py image.svg image_transparent.svg
    python make_transparent_background_svg.py image.svg output.svg --threshold 200

参数说明:
    input.svg      输入的 SVG 文件
    output.svg     处理后输出的 SVG 文件
    --threshold    (可选) 白色阈值，范围 0~255，默认 180。
                   越低 → 处理更多浅色；越高 → 仅处理接近白色的像素。

备注：
    这个程序脚本经由 GPT-5 优化调整过。
"""

import xml.etree.ElementTree as ET
import math
import re
import sys
import os
import argparse


def hex_to_rgb(color_str: str):
    """将颜色字符串转为 RGB 三元组"""
    if not color_str:
        return None
    color_str = color_str.strip().lower()

    # 3位十六进制：#fff
    if re.match(r"^#([0-9a-f]{3})$", color_str):
        color_str = "#" + "".join([ch * 2 for ch in color_str[1:]])

    # 6位十六进制：#ffffff
    if re.match(r"^#([0-9a-f]{6})$", color_str):
        return tuple(int(color_str[i : i + 2], 16) for i in (1, 3, 5))

    # rgb(...) 表示法
    if color_str.startswith("rgb(") and color_str.endswith(")"):
        nums = color_str[4:-1].split(",")
        return tuple(int(x.strip()) for x in nums)

    return None


def color_distance_to_white(rgb):
    """计算颜色与白色 (255,255,255) 的欧几里得距离"""
    if rgb is None:
        return None
    r, g, b = rgb
    return math.sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)


def opacity_from_distance(distance, max_distance=255 * math.sqrt(3)):
    """根据颜色距离计算透明度：白色=0.0，黑色≈1.0"""
    if distance is None:
        return None
    norm = min(1.0, distance / max_distance)
    return round(norm, 3)


def adjust_rect_opacity(svg_path, output_path, threshold=180):
    """将接近白色的 rect 元素透明化"""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    changes = 0
    for rect in root.findall(".//svg:rect", ns):
        fill_color = rect.get("fill")
        rgb = hex_to_rgb(fill_color)
        if rgb is None:
            continue

        distance = color_distance_to_white(rgb)

        # 仅处理亮色区域
        if (max(rgb) > threshold) and ((max(rgb) - min(rgb)) < 80):
            opacity = opacity_from_distance(distance)
            rect.set("fill-opacity", str(opacity))
            changes += 1
            
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ 已处理文件: {svg_path}")
    print(f"📄 输出文件: {output_path}")
    print(f"🔹 修改的 rect 元素数量: {changes}")
    print(f"🔧 使用的亮度阈值: {threshold}")


def main():
    parser = argparse.ArgumentParser(
        description="将 SVG 中接近白色的矩形制作成透明背景的实用工具"
    )
    parser.add_argument("input_file", help="输入的 SVG 文件路径")
    parser.add_argument("output_file", help="输出的 SVG 文件路径")
    parser.add_argument(
        "--threshold",
        type=int,
        default=180,
        help="白色亮度阈值 (0-255)，默认 180，值越低则处理更多浅灰色",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"❌ 错误: 找不到文件 '{args.input_file}'")
        sys.exit(1)

    adjust_rect_opacity(args.input_file, args.output_file, threshold=args.threshold)


if __name__ == "__main__":
    main()
