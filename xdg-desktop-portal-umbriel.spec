%global debug_package %{nil}

%global commit      80a74319bb9fef2ab604382026fc61646a8397ef
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260923

Name:           xdg-desktop-portal-umbriel
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        xdg-desktop-portal backend for the Umbriel
Summary(zh_CN): Umbriel 的 xdg-desktop-portal 后端
License:        MIT
URL:            https://github.com/noctalia-dev/xdg-desktop-portal-umbriel
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39

Requires:       xdg-desktop-portal

%description
An xdg-desktop-portal backend for the Umbriel compositor, implementing
the ScreenCast and Screenshot interfaces, plus umbriel-share-picker, a
GTK4 source chooser with live screen/window thumbnails.
Umbriel 合成器的 xdg-desktop-portal 后端，实现 ScreenCast 与 Screenshot
接口，并附带 GTK4 分享选择器 umbriel-share-picker。

%prep
%autosetup -n %{name}-%{commit}

%build
%meson -Dpicker=enabled
%meson_build

%install
%meson_install

%check
test -x %{buildroot}%{_libexecdir}/%{name}
test -x %{buildroot}%{_libexecdir}/umbriel-share-picker

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-umbriel
%{_libexecdir}/umbriel-share-picker
%{_datadir}/xdg-desktop-portal/portals/umbriel.portal
%config(noreplace) %{_datadir}/xdg-desktop-portal/umbriel-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.umbriel.service
%{_userunitdir}/xdg-desktop-portal-umbriel.service

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
