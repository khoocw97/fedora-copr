%global debug_package %{nil}

%global commit      6b5e084779706096a8da5161f946b982bac2abeb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261118

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
BuildRequires:  stb_image_resize2-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libei-1.0) >= 1.3
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  pkgconfig(xkbcommon)

Requires:       xdg-desktop-portal
Recommends:     xdg-desktop-portal-gtk

%description
An xdg-desktop-portal backend for the Umbriel compositor, implementing
the ScreenCast and Screenshot interfaces, plus umbriel-share-picker, a
noctalia-ui source chooser with live screen/window thumbnails.
Umbriel 合成器的 xdg-desktop-portal 后端，实现 ScreenCast 与 Screenshot
接口，并附带 noctalia-ui 分享选择器 umbriel-share-picker。

%prep
%autosetup -n %{name}-%{commit}

%build
%meson -Dpicker=true
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
%config %{_datadir}/xdg-desktop-portal/umbriel-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.umbriel.service
%{_datadir}/xdg-desktop-portal-umbriel/assets/fonts/noctalia-tabler.ttf
%{_datadir}/xdg-desktop-portal-umbriel/assets/fonts/tabler.json
%license %{_datadir}/xdg-desktop-portal-umbriel/assets/fonts/tabler-icons-license.txt
%{_userunitdir}/xdg-desktop-portal-umbriel.service

%changelog
* Wed Nov 18 2026 Weng <khoocw97@gmail.com>
- Bump to 6b5e084 (noctalia-ui lib update)
- Replace GTK4 picker with noctalia-ui: -Dpicker is now a boolean option
- Sync BuildRequires with lib/meson.build (pango/harfbuzz/glib/egl/stb, drop gtk4)
- Install picker font assets
* Tue Nov 17 2026 Weng <khoocw97@gmail.com>
- prefers Luciole FileChooser with gtk fallback, %config instead of %config(noreplace)
- Recommends: xdg-desktop-portal-gtk (fallback for unimplemented interfaces)
* Wed Oct 28 2026 Weng <khoocw97@gmail.com>
- Add BuildRequires pkgconfig(libei-1.0) >= 1.3 (upstream 707b548 new dependency)
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
