@echo off
chcp 65001 >nul
echo ================================================
echo          Xeliz_box 安装程序
echo ================================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [错误] 需要管理员权限！
    echo 请右键点击 install.bat，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 设置安装目录
set INSTALL_DIR=C:\Program Files\Xeliz_box

:: 创建安装目录
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: 复制文件
echo [1/4] 复制文件到 %INSTALL_DIR%...
xcopy /E /I /Y "Xeliz_box\*" "%INSTALL_DIR%\"

:: 创建桌面快捷方式
echo [2/4] 创建桌面快捷方式...
set DESKTOP=%PUBLIC%\Desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo sLinkFile = "%DESKTOP%\Xeliz_box.lnk" >> "%TEMP%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\Xeliz_box.exe" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"
cscript /nologo "%TEMP%\shortcut.vbs"
del "%TEMP%\shortcut.vbs"

:: 创建开始菜单快捷方式
echo [3/4] 创建开始菜单快捷方式...
set STARTMENU=%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo sLinkFile = "%STARTMENU%\Xeliz_box.lnk" >> "%TEMP%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\Xeliz_box.exe" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"
cscript /nologo "%TEMP%\shortcut.vbs"
del "%TEMP%\shortcut.vbs"

:: 创建卸载脚本
echo [4/4] 创建卸载脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ================================================
echo echo          Xeliz_box 卸载程序
echo echo ================================================
echo echo.
echo net session ^>nul 2^>^&1
echo if %%%%errorLevel%%%% NEQ 0 ^(
echo     echo [错误] 需要管理员权限！
echo     echo 请右键点击 uninstall.bat，选择"以管理员身份运行"
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo 正在卸载 Xeliz_box...
echo del "%DESKTOP%\Xeliz_box.lnk" /f /q ^>nul 2^>^&1
echo del "%STARTMENU%\Xeliz_box.lnk" /f /q ^>nul 2^>^&1
echo rmdir /S /Q "%INSTALL_DIR%"
echo echo 卸载完成！
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

echo.
echo ================================================
echo  安装完成！
echo ================================================
echo.
echo 安装位置: %INSTALL_DIR%
echo 卸载方法: 运行 %INSTALL_DIR%\uninstall.bat
echo.
pause