%global debug_package %{nil}

%global commit      3372b413f0e2eaafc6d2bf26051790df0770df9b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260919

Name:           umbriel
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        A Wayland compositor built on wlroots
Summary(zh_CN): 基于 wlroots 的 Wayland 合成器
License:        MIT
URL:            https://github.com/noctalia-dev/umbriel
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libinput) >= 1.23
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-server) >= 1.24
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.1
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(jemalloc)

Requires:     xwayland-satellite
Requires:     xdg-desktop-portal-umbriel

%description
Umbriel is a Wayland compositor designed for daily use, with scrolling,
dwindle, and master layouts, per-output workspaces, window rules, blur,
shadows, and fluid animations. It is built in C++23 on wlroots and
umbrielfx (its own hard fork of SceneFX), and pairs with Noctalia as its
desktop shell.
Umbriel 是一个为日常使用设计的 Wayland 合成器，具有 scrolling /
dwindle / master 布局、逐输出工作区、窗口规则、模糊、阴影和流畅动画。

%prep
%autosetup -n %{name}-%{commit}
sed -i -e "s/fallback: 'unknown'/fallback: '%{shortcommit}'/" \
       -e "s/set('VCS_TAG', 'unknown')/set('VCS_TAG', '%{shortcommit}')/" meson.build

%build
%meson -Dtests=disabled
%meson_build

%install
%meson_install
sed -i 's|^Exec=start-umbriel|Exec=%{_bindir}/start-umbriel|' \
  %{buildroot}%{_datadir}/wayland-sessions/umbriel.desktop
install -Dpm 0644 umbrielfx/LICENSE \
  %{buildroot}%{_licensedir}/%{name}/umbrielfx/LICENSE

%check
%{buildroot}%{_bindir}/%{name} --version
test -x %{buildroot}%{_bindir}/start-umbriel

%post
%systemd_user_post umbriel.service umbriel-session.target umbriel-shutdown.target

%preun
%systemd_user_preun umbriel.service umbriel-session.target umbriel-shutdown.target

%postun
%systemd_user_postun umbriel.service umbriel-session.target umbriel-shutdown.target

%files
%license LICENSE
%doc README.md PACKAGING.md
%{_licensedir}/%{name}/umbrielfx/LICENSE
%{_bindir}/umbriel
%{_bindir}/start-umbriel
%config(noreplace) %{_datadir}/umbriel/config.toml
%{_datadir}/umbriel/shaders/
%{_datadir}/wayland-sessions/umbriel.desktop
%{_userunitdir}/umbriel.service
%{_userunitdir}/umbriel-session.target
%{_userunitdir}/umbriel-shutdown.target

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
