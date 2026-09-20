%global debug_package %{nil}

%global commit      caba5c32e3fcb834bb0461e5c3527573b57cd30b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260919

Name:           scenefx
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        Drop-in wlroots scene API replacement with eye-candy effects
Summary(zh_CN): 带桌面特效的 wlroots scene API 替代实现
License:        MIT
URL:            https://github.com/wlrfx/scenefx
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
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.24.0
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(xkbcommon) >= 1.8.0

%description
SceneFX takes the wlroots scene API and replaces the wlr renderer with
its own fx renderer, capable of rendering surfaces with eye-candy
effects including blur, shadows, and rounded corners. It is required by
Wayland compositors such as MangoWM.
SceneFX 将 wlroots scene API 的 wlr 渲染器替换为自研 fx 渲染器，可渲染
模糊、阴影、圆角等特效。MangoWM 等 Wayland 合成器依赖此库。

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config files for developing against %{name}.

%prep
%autosetup -n %{name}-%{commit}

%build
# -Dexamples=false: tinywl/scene-graph are build-only demos, never installed.
# -Dcolor-management=enabled: keep the lcms2 dependency deterministic instead
# of auto-detect.
%meson -Dexamples=false -Dcolor-management=enabled
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md
%{_libdir}/libscenefx-0.5.so

%files devel
%{_includedir}/scenefx-0.5/
%{_libdir}/pkgconfig/scenefx-0.5.pc

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
