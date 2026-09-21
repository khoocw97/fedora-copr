%global debug_package %{nil}

%global commit      add2795134593faafce60e404a0a75df68e9ee0c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260909

Name:           xwayland-satellite
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        Rootless Xwayland integration for Wayland compositors
Summary(zh_CN): 为 Wayland 合成器提供无根 Xwayland 集成
License:        MPL-2.0
URL:            https://github.com/Supreeeme/xwayland-satellite
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  pkgconfig(xcb)

Requires:       xorg-x11-server-Xwayland

%description
xwayland-satellite grants rootless Xwayland integration to any Wayland
compositor implementing xdg_wm_base and viewporter. It proxies X11
clients through a nested Xwayland instance, useful for compositors that
do not want to implement rootless Xwayland themselves.
xwayland-satellite 为任意实现了 xdg_wm_base 与 viewporter 的 Wayland
合成器提供无根 Xwayland 集成，通过嵌套的 Xwayland 实例代理 X11 客户端。

%prep
%autosetup -n %{name}-%{commit}

%build
cargo build --locked --release

%install
install -Dpm 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{name}.man %{buildroot}%{_mandir}/man1/%{name}.1

%check
%{buildroot}%{_bindir}/%{name} --help

%files
%license LICENSE
%doc README.md ARCHITECTURE.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Mon Sep 21 2026 Weng <khoocw97@gmail.com>
- Initial package
