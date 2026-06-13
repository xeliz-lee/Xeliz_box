#!/usr/bin/env python3
import sys, os, traceback

if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
    _internal_dir = os.path.join(_base_dir, '_internal')
    if os.path.isdir(_internal_dir):
        sys.path.insert(0, _internal_dir)
        sys.path.insert(0, _base_dir)

log = []
log.append(f"=== PyInstaller Runtime Diagnostics ===")
log.append(f"exe: {sys.executable}")
log.append(f"frozen: {getattr(sys, 'frozen', False)}")
log.append(f"")

# Test 1: tools.base
try:
    from tools.base import Tool
    log.append(f"[PASS] from tools.base import Tool")
except Exception as e:
    log.append(f"[FAIL] tools.base: {e}")

# Test 2: import tools
try:
    import tools
    log.append(f"[PASS] import tools -> {tools.__file__}")
except Exception as e:
    log.append(f"[FAIL] import tools: {e}")

# Test 3: get_all_tools()
try:
    from tools import get_all_tools
    all_tools = get_all_tools()
    log.append(f"[PASS] get_all_tools() -> {len(all_tools)} tools")
    for t in all_tools[:5]:
        log.append(f"  - {t.name} ({t.category})")
    if len(all_tools) > 5:
        log.append(f"  ... and {len(all_tools)-5} more")
except Exception as e:
    log.append(f"[FAIL] get_all_tools(): {e}")
    traceback.print_exc(file=sys.stdout)
    log.append(traceback.format_exc())

# Write to file
with open(os.path.join(os.path.dirname(sys.executable), "debug_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("\n".join(log))
