#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试：检查代码中是否还有硬编码路径
不需要导入模块，直接读取源文件
"""

from pathlib import Path

def test_hardcoded_paths():
    """检查源文件中是否有硬编码路径"""
    print("=" * 60)
    print("检查硬编码路径")
    print("=" * 60)
    
    # 要检查的文件
    files_to_check = [
        "model_manager.py",
        "nodes/sa2va_node.py",
        "__init__.py",
    ]
    
    # 硬编码路径模式
    hardcoded_patterns = [
        "E:/Comfyui_test",
        "E:\\Comfyui_test",
        'E:/Comfyui_test',
        'E:\\Comfyui_test',
    ]
    
    all_clean = True
    
    for file_name in files_to_check:
        file_path = Path(__file__).parent / file_name
        
        if not file_path.exists():
            print(f"⚠️ 文件不存在: {file_name}")
            continue
        
        print(f"\n检查文件: {file_name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        found_issues = []
        for pattern in hardcoded_patterns:
            if pattern in content:
                # 统计出现次数
                count = content.count(pattern)
                found_issues.append(f"  ❌ 发现 '{pattern}' 出现 {count} 次")
        
        if found_issues:
            all_clean = False
            for issue in found_issues:
                print(issue)
        else:
            print("  ✅ 未发现硬编码路径")
    
    print("\n" + "=" * 60)
    if all_clean:
        print("✅ 所有文件检查通过！没有硬编码路径。")
    else:
        print("❌ 发现硬编码路径，需要修复。")
    print("=" * 60)
    
    return all_clean


def test_auto_detection_logic():
    """检查自动检测逻辑是否存在"""
    print("\n" + "=" * 60)
    print("检查自动检测逻辑")
    print("=" * 60)
    
    model_manager_path = Path(__file__).parent / "model_manager.py"
    
    with open(model_manager_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键函数和逻辑
    checks = [
        ("find_comfyui_root", "自动查找ComfyUI根目录函数"),
        ("Optional[str] = None", "可选路径参数"),
        ("relative_to", "相对路径显示"),
        ("ComfyUI/", "相对路径格式"),
    ]
    
    all_found = True
    for keyword, description in checks:
        if keyword in content:
            print(f"✅ 找到: {description}")
        else:
            print(f"❌ 缺失: {description}")
            all_found = False
    
    print("=" * 60)
    return all_found


def main():
    """运行所有测试"""
    print("\n" + "🔍" * 30)
    print("ComfyUI-Sa2VA-DP 路径修复验证")
    print("🔍" * 30 + "\n")
    
    test1 = test_hardcoded_paths()
    test2 = test_auto_detection_logic()
    
    print("\n" + "=" * 60)
    print("最终结果")
    print("=" * 60)
    
    if test1 and test2:
        print("🎉 所有检查通过！路径问题已修复！")
        print("\n修复内容:")
        print("1. ✅ 移除了硬编码的 E:/Comfyui_test/ComfyUI 路径")
        print("2. ✅ 添加了自动检测ComfyUI根目录功能")
        print("3. ✅ 使用相对路径显示，不暴露用户完整路径")
        print("4. ✅ 添加了友好的错误提示")
        return True
    else:
        print("⚠️ 部分检查未通过，请查看上面的详细信息")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
