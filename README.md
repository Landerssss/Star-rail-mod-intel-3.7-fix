# Star-rail-mod-intel-3.7-fix 🔧
> **星穹铁道 Intel 显卡 Mod 问题综合修复方案**

在 Intel 显卡（集显/独显）环境下使用 Mod 时出现的人物黑屏、模型爆炸、贴图丢失（半身/透明）等问题。整合了手动配置文件修复与 Python 哈希自动修正脚本。

---

## (Patch Notes)

下载文件后在 MOD 文件下运行：

```bash
cd “你的MOD路径”
python intel_compatibility.py
```



---

## 说明 (Patch Notes)

> 下方内容为转载：[HSR v3.7 Intel显卡补丁说明]

在 3.7 版本中，米哈游在更新后一天紧急发布了一次补丁，修复了 Intel 显卡 GPU 上姿势渲染的变化问题。同时还撤销了在 3.2 版本中针对 Intel 硬件引入的计算着色器修改。

本仓库提供的脚本在 v3.2 之前使用的绘制哈希基础上新增了一个额外部分，同时加入了新的角色绘制哈希。

**以下是我的补充说明：如果模组修复后仍然无法正常运行：**
很可能是 `.ini` 文件中缺少以下一行判定代码（建议参考其他正常运行的 Mod）：
```ini
DRAW_TYPE == 1
注：某些 Intel GPU 版本可能还会有其他问题，但目前尚未得到确认。

第一步：确保加载器核心正确  
如果你使用了旧版的 3.6.exe 或其他过期的“修复工具”，可能会有一些错误

打开 XXMI 或 JASM。

找到 SRMI 安装选项。

点击 Reinstall (重新安装) 或 Update，确保核心文件（d3d11.dll）是最新版本。

不要 再运行旧版的 exe 修复工具。

第二步：全局配置修复 
请手动修改 d3dx.ini 配置文件。

打开 SRMI 文件夹下的 d3dx.ini。

使用记事本或代码编辑器，修改/确认以下参数（如果没有请手动添加）：

在 [Rendering] 区域下添加：

Ini, TOML

; 强制纹理拷贝，修复 Intel 显卡贴图透明/缺失的核心指令
copymips = 1
在 [Device] 区域下添加/修改：

Ini, TOML

; 强制 CPU 访问，修复模型爆炸/乱码
force_cpu_access = 1

; 修正分辨率识别错误，防止衣服错位
get_resolution_from = depth_stencil

; 解决闪屏问题 (绝对不能设为 1)
rasterizer_disable_scissor = 0
在 [Rendering] 区域修改（可选，优化防丢图）：

Ini, TOML

; 开启显存追踪，防止加载一半丢失
track_texture_updates = 1

