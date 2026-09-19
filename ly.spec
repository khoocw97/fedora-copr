%global debug_package %{nil}

%global commit      60be7ada9e6e84371c89c03303b133d0bebf7c0b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260908

Name:           ly
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        A lightweight TUI display manager
Summary(zh_CN): 轻量 TUI 显示管理器
License:        WTFPL AND MIT
URL:            https://codeberg.org/fairyglade/ly
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  zig >= 0.16.0
BuildRequires:  systemd-rpm-macros
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(xcb)
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers

%description
Ly is a lightweight TUI (ncurses-like) display manager for Linux, with
X11 and Wayland session support, PAM authentication, Lua-based
configuration, and 25 interface languages.
Ly 是一个轻量 TUI 显示管理器，支持 X11 与 Wayland 会话、PAM 认证、
Lua 配置文件，带 25 种界面语言。

%prep
%autosetup -n %{name}

%build
zig build -Doptimize=ReleaseSafe

%install
zig build installexe -Doptimize=ReleaseSafe \
  -Ddest_directory=%{buildroot} \
  -Dinit_system=systemd

%check
%{buildroot}%{_bindir}/ly --version
%{buildroot}%{_bindir}/ly --help

%files
%license license.md
%doc readme.md
%{_bindir}/ly
%config(noreplace) %{_sysconfdir}/ly/config.lua
%config(noreplace) %{_sysconfdir}/ly/config.lua.example
%config(noreplace) %{_sysconfdir}/ly/setup.sh
%config(noreplace) %{_sysconfdir}/ly/startup.sh
%config(noreplace) %{_sysconfdir}/ly/example.dur
%config(noreplace) %{_sysconfdir}/ly/example.lua
%{_sysconfdir}/ly/custom-sessions/README
%{_sysconfdir}/ly/lang/
%config(noreplace) %{_sysconfdir}/pam.d/ly
%config(noreplace) %{_sysconfdir}/pam.d/ly-autologin
%{_unitdir}/ly@.service
%{_unitdir}/ly-kmsconvt@.service

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
