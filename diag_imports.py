import sys, os, traceback

# 模拟 PyInstaller 环境
sys.path.insert(0, r"toolbox\dist\Xeliz_box\_internal")
sys.path.insert(0, r"toolbox\dist\Xeliz_box")

print("=== Import Chain Test ===")
print(f"Python: {sys.executable}")
print(f"sys.path[0]: {sys.path[0]}")
print()

try:
    print("1. import tools...")
    import tools
    print(f"   OK: {tools.__file__}")
except Exception as e:
    print(f"   FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. from tools import get_all_tools...")
    from tools import get_all_tools
    print("   OK")
except Exception as e:
    print(f"   FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("3. get_all_tools()...")
    tools_list = get_all_tools()
    print(f"   OK: {len(tools_list)} tools returned!")
    for t in tools_list[:3]:
        print(f"      - {t.name}: {t.description}")
    if len(tools_list) > 3:
        print(f"      ... and {len(tools_list)-3} more")
except Exception as e:
    print(f"   FAILED: {e}")
    traceback.print_exc()
