import sys, os, traceback

# PyInstaller 运行时的 sys.path
sys.path.insert(0, os.path.dirname(sys.executable))

print("=== PyInstaller Runtime Diagnostics ===")
print(f"exe dir: {os.path.dirname(sys.executable)}")
print(f"sys.path: {sys.path[:5]}")
print()

# 检查 _internal 目录结构
internal = os.path.dirname(sys.executable)
for root, dirs, files in os.walk(internal):
    level = root.replace(internal, "").count(os.sep)
    if level <= 2:
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)
        for file in files[:10]:
            print(f"{subindent}{file}")
        if len(files) > 10:
            print(f"{subindent}... +{len(files)-10} more")
