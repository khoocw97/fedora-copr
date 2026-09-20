# fedora-copr — Agent Notes

> 个人 COPR 打包约定与排坑记录，同步于 `khoocw97/software`。

## 1. 项目与构建流

- **仓库**: `khoocw97/fedora-copr`，每个 `*.spec` 对应 COPR 一个 Package，`Source` 直链上游（GitHub/Codeberg）。
- **SRPM**: 走 `.copr/Makefile` 通用 `srpm` target：`spectool -g --directory $tmpd/SOURCES <spec>` → `rpmbuild -bs`。COPR 不用 `rpkg`/`dist-git`。
- **批量本地**: 顶层 `Makefile` 的 `SPECS := ...` 仅用于 `make srpm` 本地验证。
- **COPR 顺序**: `scenefx` 必须先单独构建成功，`mangowm` 才能解析 `pkgconfig(scenefx-0.5)`。其它包无此依赖。

## 2. 网络

- COPR 构建期默认 `enable_net: False`（mock `--resolv-conf=off`），`cargo build`/`zig fetch`/`pip install` 会 DNS 失败。
- 已在 COPR 项目 Settings 打开 **Enable internet access during builds**（项目级，对自动/手动构建均生效）。`vm-curator` / `ly` / `bibata` 依赖它。
- 不想开网的替代：`cargo vendor` / `zig vendor` 打进 SRPM + `--offline`，代价是 SRPM 变大。

## 3. check-upstream

- `.github/workflows/check-upstream.yml` 每天 `00:00 Asia/Shanghai = 16:00 UTC` (`cron: '0 16 * * *'`)。
- `bump()` 已支持双 forge：`bump github <org/repo> <spec>` 走 `api.github.com` + `GH_TOKEN`，`bump codeberg <org/repo> <spec>` 走 `codeberg.org/api/v1/...` 免 token。
- 当前跟踪（commit 快照）：
  - `github noctalia-dev/umbriel`, `noctalia-dev/xdg-desktop-portal-umbriel`, `mroboff/vm-curator`, `mangowm/mango`, `wlrfx/scenefx`
  - `codeberg fairyglade/ly`
- 固定版本不跟踪：`bibata-cursor-themes` (tag `v2.0.7`), `lxgw-fonts` (自定 `1.0`), `maple-mono-fonts` (`7.9`)。

## 4. Spec 模板（以 `umbriel.spec` 为准）

```spec
%global debug_package %{nil}
%global commit <sha>
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate YYYYMMDD
Name: foo
Version: %{commitdate}git.%{shortcommit}
License: SPDX
URL: https://...
Source0: %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch: x86_64 aarch64   # 仅限编译型；noarch 包不用
BuildRequires: ...
%autosetup -n %{name}-%{commit}  # Codeberg 归档是 %{name}/，则 -n %{name}
%meson / %build ...
%check  # 轻量可执行检查
%files  # %license / %doc 明确
```

- 纯二进制字体/光标：`BuildArch: noarch`，`Version` 固定 tag，无 `commit`。
- Codeberg 归档顶层是 `ly/` 而非 `ly-<sha>`，注意 `%autosetup -n`。

## 5. 已验证的上游依赖

- **umbriel**: `wlroots-0.20 >=0.20.1`（F44 `wlroots 0.20.2` 满足），`wayland-protocols >=1.47` 等。
- **mangowm**: 需 `xcb-randr`（上游 `meson.build` 显式依赖，参考 spec 漏了）；删 `Requires: vulkan-loader`（由 `wlroots` 自动带）；`Recommends: xdg-desktop-portal-wlr`。
- **scenefx**: 纯 `meson`，`egl/gbm/glesv2/lcms2/libdrm>=2.4.129/pixman>=0.43` 等 F44 均有。
- **ly**: `zig >=0.16.0`（F44 有 0.16.0），`pam-devel + pkgconfig(xcb) + glibc-devel + kernel-headers`（`translate-c` 解析系统头）。
- **vm-curator**: `cargo + gcc + pkgconfig(libudev)`，`cargo build --locked --release` 需联网。

## 6. 常见排坑

| 现象 | 根因 | 修法 |
|------|------|------|
| `ctgen: command not found` (bibata) | `pip` 装到 `/builddir/.local/bin`，spec 只加了 `%{_builddir}/.local/bin` | `export PATH="/builddir/.local/bin:%{_builddir}/.local/bin:$PATH"` + `pip install --no-warn-script-location` |
| `File not found: .../BUILDROOT/.../OFL.txt` (lxgw) | `%license %{SOURCE3}` 在 `%files` 会被当 BUILDROOT 相对路径 | `%prep` 先 `cp %{SOURCE3} ./OFL.txt`，`%files` 用 `%license OFL.txt` |
| `install: cannot stat 'MapleMono-NF-CN/*.ttf'` (maple) | zip 解压后文件在当前目录根下，非子目录 | `%install` 改 `install -m 0644 *.ttf ...`，`%license LICENSE.txt` 同理 |
| `bogus date in %changelog` | 星期与日期不匹配（`Sun Sep 21 2026` 实际是 Monday） | 用 `date -d YYYY-MM-DD +%A` 校验，改为 `Mon Sep 21 2026` |
| `scenefx` 找不到 | Fedora 官方无 `scenefx-0.5`，需同 COPR 自建 | 先单独构建 `scenefx.spec`，再建 `mangowm` |

## 7. 当前 Spec 清单

| Spec | 上游 | 版本策略 | 备注 |
|------|------|----------|------|
| `umbriel.spec` | `noctalia-dev/umbriel` | commit 快照 |  |
| `xdg-desktop-portal-umbriel.spec` | 同上 | commit 快照 |  |
| `vm-curator.spec` | `mroboff/vm-curator` | `20260811git.cdcf2ac` | 需联网 |
| `mangowm.spec` | `mangowm/mango` | `d4b1e49` | 依赖自建 scenefx |
| `scenefx.spec` | `wlrfx/scenefx` | `3606f3d` | 被 mangowm 依赖 |
| `ly.spec` | `codeberg:fairyglade/ly` | `60be7ad` | zig 0.16 |
| `bibata-cursor-themes.spec` | `ful1e5/Bibata_Cursor` | `2.0.7` tag | 6 变体，删 Right |
| `lxgw-fonts.spec` | `lxgw/*` | `1.0` 自定 (Bright v5.528 + Neo v1.305) | 7z，需 p7zip |
| `maple-mono-fonts.spec` | `subframe7536/maple-font` | `7.9` tag | NF-CN zip |

## 8. 待办 / 约定

- 新包默认 `Summary(zh_CN)` 双语，`%global debug_package %{nil}`，`%check` 跑 `--version`/`--help`。
- 固定版本包不加入 `check-upstream` bump，手动改 `Version` + `Source`。
- 新增字体/光标类 `BuildArch: noarch`，不需要 `ExclusiveArch`。
