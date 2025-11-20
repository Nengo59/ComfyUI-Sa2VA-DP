#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试路径修复是否成功
验证自动检测ComfyUI根目录功能
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_find_comfyui_root():
    """测试自动查找ComfyUI根目录功能"""
    print("=" * 60)
    print("测试1: 自动查找ComfyUI根目录")
    print("=" * 60)
    
    try:
        from model_manager import find_comfyui_root
        
        root = find_comfyui_root()
        print(f"✅ 成功找到ComfyUI根目录: {root}")
        
        # 验证是否存在models目录
        models_dir = root / "models"
        if models_dir.exists():
            print(f"✅ 验证通过: models目录存在")
        else:
            print(f"❌ 验证失败: models目录不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_manager_init():
    """测试模型管理器初始化（不指定路径）"""
    print("\n" + "=" * 60)
    print("测试2: 模型管理器自动初始化")
    print("=" * 60)
    
    try:
        from model_manager import Sa2VAModelManager
        
        # 不传入路径，测试自动检测
        manager = Sa2VAModelManager()
        
        print(f"✅ 模型管理器初始化成功")
        print(f"   ComfyUI根目录: {manager.comfyui_path}")
        print(f"   模型目录: {manager.models_dir}")
        
        # 验证模型目录是否创建
        if manager.models_dir.exists():
            print(f"✅ 模型目录已创建")
        else:
            print(f"❌ 模型目录创建失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_path_display():
    """测试路径显示（相对路径）"""
    print("\n" + "=" * 60)
    print("测试3: 路径显示格式")
    print("=" * 60)
    
    try:
        from model_manager import Sa2VAModelManager
        
        manager = Sa2VAModelManager()
        
        # 测试获取模型路径
        test_model = "ByteDance/Sa2VA-Qwen3-VL-4B"
        model_path = manager.get_model_path(test_model)
        
        print(f"✅ 获取模型路径成功")
        print(f"   模型名称: {test_model}")
        print(f"   完整路径: {model_path}")
        
        # 尝试获取相对路径
        try:
            rel_path = model_path.relative_to(manager.comfyui_path)
            print(f"✅ 相对路径: ComfyUI/{rel_path}")
            print(f"   (不会暴露用户的完整路径)")
        except ValueError:
            print(f"⚠️ 无法获取相对路径")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_hardcoded_paths():
    """测试是否还有硬编码路径"""
    print("\n" + "=" * 60)
    print("测试4: 检查硬编码路径")
    print("=" * 60)
    
    try:
        import model_manager
        import inspect
        
        # 获取源代码
        source = inspect.getsource(model_manager)
        
        # 检查是否包含硬编码的E盘路径
        hardcoded_patterns = [
            "E:/Comfyui_test",
            "E:\\Comfyui_test",
            'E:/Comfyui_test',
            'E:\\Comfyui_test',
        ]
        
        found_hardcoded = False
        for pattern in hardcoded_patterns:
            if pattern in source:
                print(f"❌ 发现硬编码路径: {pattern}")
                found_hardcoded = True
        
        if not found_hardcoded:
            print(f"✅ 未发现硬编码路径")
            return True
        else:
            print(f"❌ 仍存在硬编码路径，需要修复")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "🔍" * 30)
    print("ComfyUI-Sa2VA-DP 路径修复测试")
    print("🔍" * 30 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(("自动查找ComfyUI根目录", test_find_comfyui_root()))
    results.append(("模型管理器自动初始化", test_model_manager_init()))
    results.append(("路径显示格式", test_path_display()))
    results.append(("检查硬编码路径", test_no_hardcoded_paths()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "-" * 60)
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    print("-" * 60)
    
    if failed == 0:
        print("\n🎉 所有测试通过！路径修复成功！")
        return True
    else:
        print(f"\n⚠️ 有 {failed} 个测试失败，请检查")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
