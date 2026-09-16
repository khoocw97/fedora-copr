%global debug_package %{nil}

%global commit      d4b1e49fcbfd14e62acec4e9a0d895230f25da8f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260916

Name:           mangowm
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        Practical and powerful Wayland compositor based on dwl
Summary(zh_CN): 基于 dwl 的实用强大的 Wayland 合成器
License:        GPL-3.0-or-later AND MIT
URL:            https://github.com/mangowm/mango
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-randr)
# protocols/meson.build consumes staging XMLs (cursor-shape, ext-workspace,
# ext-image-capture, ...) and resolves them via pkgconfig pkgdatadir, so a
# recent protocols package is required.
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wayland-client)
# Protocol codegen uses find_program('wayland-scanner'); keep it explicit.
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput) >= 1.27.1
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libcjson)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
# Provided by the scenefx package in this COPR (not in Fedora repos).
BuildRequires:  pkgconfig(scenefx-0.5) >= 0.5.0

Requires:       xorg-x11-server-Xwayland

Recommends:     xdg-desktop-portal >= 1.18
Recommends:     xdg-desktop-portal-gtk
Recommends:     xdg-desktop-portal-wlr

Provides:       wayland-compositor

%description
MangoWM is a practical and powerful Wayland compositor based on dwl,
keeping the lightweight, fast-build philosophy while adding day-to-day
usability: external configuration with hot-reload, scratchpad, IPC via
mmsg, and window effects (blur, shadow, corner radius, opacity) through
scenefx.
MangoWM 是一个基于 dwl 的实用强大的 Wayland 合成器，保持轻量快速的同时
提供日常可用的功能：支持热重载的外部配置、暂存区、经由 mmsg 的 IPC，
以及经由 scenefx 的窗口特效（模糊、阴影、圆角、透明）。

%prep
%autosetup -n mango-%{commit}

%build
%meson
%meson_build

%install
%meson_install

%check
%{buildroot}%{_bindir}/mango -v
test -x %{buildroot}%{_bindir}/mmsg

%files
%license LICENSE
%doc README.md
%{_bindir}/mango
%{_bindir}/mmsg
%{_mandir}/man1/mmsg.1*
%config(noreplace) %{_sysconfdir}/mango/config.conf
%{_datadir}/wayland-sessions/mango.desktop
%config(noreplace) %{_datadir}/xdg-desktop-portal/mango-portals.conf
%{_userunitdir}/mango-session.target

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
