#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片优化脚本 v2 - 安全版
从原始图片创建优化版本，保留原始文件
"""

from PIL import Image
import os
import shutil

os.chdir(r'e:\Code\Jiaxiaoshe-together\images')

# 定义目标尺寸 - 使用 1200x675 (16:9 比例，适合web)
target_width = 1200
target_height = 675
target_ratio = target_width / target_height

print("=" * 80)
print("图片优化工具 v2 - 安全版（保留原始文件）")
print("=" * 80)

# 首先检查是否有备份文件夹
backup_dir = 'backup_original'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# 处理 1-7 号图片
for i in range(1, 8):
    filename = f'{i}.jpg'
    backup_filename = os.path.join(backup_dir, filename)
    
    if not os.path.exists(filename):
        print(f'⚠ {filename} 不存在')
        continue
    
    # 检查文件大小，如果为 0 则报错
    file_size = os.path.getsize(filename)
    if file_size == 0:
        print(f'✗ {filename} 为空文件（0 字节）- 需要重新上传')
        continue
    
    try:
        # 备份原始文件
        if not os.path.exists(backup_filename):
            shutil.copy2(filename, backup_filename)
            print(f'  → 已备份: {filename} -> {backup_dir}/{filename}')
        
        # 打开并处理图片
        img = Image.open(filename)
        img_ratio = img.width / img.height
        old_size = file_size / (1024*1024)
        
        print(f'\n📷 处理 {filename}...')
        print(f'  原始信息: {img.width}x{img.height}, {img.mode} 模式, {old_size:.2f}MB')
        
        # 计算裁剪尺寸 - 中心裁剪
        if img_ratio > target_ratio:
            # 图片太宽，裁剪宽度
            new_width = int(img.height * target_ratio)
            new_height = img.height
            left = (img.width - new_width) // 2
            top = 0
            crop_type = "宽度过宽"
        else:
            # 图片太高，裁剪高度
            new_width = img.width
            new_height = int(img.width / target_ratio)
            left = 0
            top = (img.height - new_height) // 2
            crop_type = "高度过高"
        
        print(f'  裁剪原因: {crop_type}（原宽高比: {img_ratio:.3f}, 目标: {target_ratio:.3f}）')
        print(f'  裁剪范围: ({left}, {top}) to ({left + new_width}, {top + new_height})')
        
        # 执行中心裁剪
        img_cropped = img.crop((left, top, left + new_width, top + new_height))
        print(f'  ✓ 裁剪完成: {new_width}x{new_height}')
        
        # 调整大小到目标分辨率
        img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        print(f'  ✓ 缩放完成: {target_width}x{target_height}')
        
        # 处理色彩模式
        if img_resized.mode == 'RGBA':
            print(f'  - 转换模式: RGBA -> RGB (白色背景)')
            background = Image.new('RGB', img_resized.size, (255, 255, 255))
            background.paste(img_resized, mask=img_resized.split()[3])
            img_resized = background
        elif img_resized.mode != 'RGB':
            print(f'  - 转换模式: {img_resized.mode} -> RGB')
            img_resized = img_resized.convert('RGB')
        
        # 保存（暂时用临时名称）
        temp_filename = f'{filename}.tmp'
        img_resized.save(temp_filename, 'JPEG', quality=85, optimize=True)
        print(f'  ✓ 保存临时文件: {temp_filename}')
        
        # 替换原文件
        os.replace(temp_filename, filename)
        new_size = os.path.getsize(filename) / (1024*1024)
        size_change = ((new_size - old_size) / old_size) * 100
        
        print(f'✅ {filename} 完成: {old_size:.2f}MB -> {new_size:.2f}MB ({size_change:+.1f}%)')
        
    except Exception as e:
        print(f'❌ {filename} 处理失败: {str(e)}')
        print(f'   提示: 请检查文件是否损坏或重新上传')

# 删除多余的 8.jpg
if os.path.exists('8.jpg'):
    backup_8 = os.path.join(backup_dir, '8.jpg')
    if not os.path.exists(backup_8):
        shutil.copy2('8.jpg', backup_8)
    os.remove('8.jpg')
    print(f'\n✓ 8.jpg 已删除并备份（多余图片）')

print("\n" + "=" * 80)
print("✅ 处理流程完成！")
print(f"💾 原始图片已备份到: {backup_dir}/")
print("=" * 80)
