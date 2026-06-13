# 项目改名总结：ToolBox → Xeliz_box

**时间**：2026-06-13 15:34 CST
**操作**：批量替换 + 文件重命名

## 已修改的内容

### 1. 源码内容替换（ToolBox → Xeliz_box）
- `main.py`
- `ui/main_window.py`
- `utils/config.py`
- `tools/office_tools.py`
- `main_debug.py`
- `main_debug2.py`
- `diag_imports.py`
- `build.ps1`
- `ToolBox.spec`
- `README.md`
- `install.bat`（GBK 编码）
- `.idea/misc.xml`
- `.idea/workspace.xml`
- `.idea/modules.xml`
- `.idea/inspectionProfiles/profiles_settings.xml`
- `.idea/inspectionProfiles/Project_Default.xml`

### 2. 文件/目录重命名
| 旧名称 | 新名称 |
|--------|--------|
| `dist/ToolBox/` | `dist/Xeliz_box/` |
| `build/ToolBox/` | `build/Xeliz_box/` |
| `toolbox.iml` | `Xeliz_box.iml` |
| `ToolBox.spec` | `Xeliz_box.spec` |
| `install.bat` | `Xeliz_box_install.bat` |
| `ToolBox_Setup.zip` | `Xeliz_box_Setup.zip` |
| `ToolBox_Dependencies.zip` | `Xeliz_box_Dependencies.zip` |

### 3. 打包输出内部文件名更新
- `dist/Xeliz_box/ToolBox.exe` → `dist/Xeliz_box/Xeliz_box.exe`
- `build/Xeliz_box/` 下所有 `ToolBox.*` 文件 → `Xeliz_box.*`
- `Xeliz_box_Setup.zip` 内部：`ToolBox/` → `Xeliz_box/`，`install.bat` → `Xeliz_box_install.bat`

### 4. build/ 目录 TOC 文件内容更新
- `Analysis-00.toc`, `COLLECT-00.toc`, `EXE-00.toc`, `PKG-00.toc`, `PYZ-00.toc`
- 内部路径引用全部从 `ToolBox` 更新为 `Xeliz_box`

## 最终文件状态
- ✅ `Xeliz_box_Setup.zip` (119.7 MB)
- ✅ `Xeliz_box_Dependencies.zip` (262 MB)
- ✅ `dist/Xeliz_box/Xeliz_box.exe` (7.6 MB)
- ✅ `Xeliz_box.spec` / `Xeliz_box_install.bat`

## 待办
- [ ] 源码目录改名（`toolbox/` → `xeliz_box/`）- 可选，当前代码兼容
- [ ] 重新 PyInstaller 打包验证
