"""
PS: 仅适用于 Windows
"""
import os
import random
import win32api
import win32con
import win32gui

wallpapers_path = r"D:\wallpapers"

new_wallpapers_path = 'D:\wallpapers_used'
wallpapers = []

def set_wallpaper(photo_path):
    """设置壁纸"""

    # 1.打开注册表键
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)

    # 2.设置壁纸风格：0=居中 1=平铺 2=拉伸
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "1")

    # 3.设置壁纸是否缩放：0=缩放 1=原图
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")

    # 4.设置壁纸
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, photo_path, 3)

    # 5.关闭注册表键
    win32api.RegCloseKey(key)


# 遍历D:\Wallpaper文件夹下所有jpg文件名放入列表
for root, dirs, files in os.walk( wallpapers_path):
    for f in files:
        if os.path.splitext(f)[1] == ".jpg":
            wallpapers.append(os.path.join(root, f))

# 列表中随机选一个
choose = wallpapers[random.randint(0, len(wallpapers) - 1)]

new_path = os.path.join( new_wallpapers_path , os.path.split( choose )[-1] )

# print( choose )
os.rename( choose , new_path )

choose = new_path

# 更换选中的壁纸
set_wallpaper( choose )
# ctypes.windll.user32.SystemParametersInfoW(20, 0, new_path, 0)


