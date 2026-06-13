#!/usr/bin/env python3
import sys, os, traceback

if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
    _internal_dir = os.path.join(_base_dir, '_internal')
    if os.path.isdir(_internal_dir) and _internal_dir not in sys.path:
        sys.path.insert(0, _internal_dir)
        sys.path.insert(0, _base_dir)

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)

log_lines = []
log_lines.append(f"sys.executable = {sys.executable}")
log_lines.append(f"frozen = {getattr(sys, 'frozen', False)}")
log_lines.append(f"sys.path[0] = {sys.path[0]}")
log_lines.append(f"")

# Test import tools
try:
    import tools
    log_lines.append(f"✅ import tools OK: {tools.__file__}")
except Exception as e:
    log_lines.append(f"❌ import tools FAIL: {e}")
    traceback.print_exc()
    log_lines.append(traceback.format_exc())

# Test get_all_tools
try:
    from tools import get_all_tools
    all_tools = get_all_tools()
    log_lines.append(f"✅ get_all_tools() -> {len(all_tools)} tools")
    
    # Show first 5 tool names
    for i, t in enumerate(all_tools[:5]):
        log_lines.append(f"  [{i}] name={t.name!r} icon={t.icon!r} desc={t.description!r} tags={t.tags}")
    if len(all_tools) > 5:
        log_lines.append(f"  ... +{len(all_tools)-5} more")
except Exception as e:
    log_lines.append(f"❌ get_all_tools() FAIL: {e}")
    traceback.print_exc()
    log_lines.append(traceback.format_exc())

# Now try to create the main window and check load_tools
try:
    from ui.main_window import Xeliz_boxWindow
    window = Xeliz_boxWindow()
    log_lines.append(f"")
    log_lines.append(f"✅ Xeliz_boxWindow created")
    log_lines.append(f"  window.tools count = {len(window.tools)}")
    log_lines.append(f"  tool_list count (after load_tools) = {window.tool_list.count()}")
except Exception as e:
    log_lines.append(f"❌ Xeliz_boxWindow FAIL: {e}")
    traceback.print_exc()
    log_lines.append(traceback.format_exc())

window.show()

# Show debug dialog
msg = "\n".join(log_lines)
QMessageBox.information(None, "Debug Info", msg)

sys.exit(app.exec())
