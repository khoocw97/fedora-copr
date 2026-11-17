%global debug_package %{nil}

%global commit      d8755c598078a68d5bde98cf07fd800495eb0a34
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261117

Name:           luciole
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        Native Wayland file manager with fast previews, tabs and split view
Summary(zh_CN): 原生 Wayland 文件管理器，支持快速预览、标签页与分屏视图
License:        MIT
URL:            https://github.com/noctalia-dev/luciole
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.1
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  stb_image_resize2-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.44
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glycin-2) >= 2.0.1
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcurl) >= 7.85
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.9
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(tomlplusplus) >= 3.4
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(xkbcommon)

Requires:       adwaita-icon-theme
Requires:       dconf
Requires:       glib-networking
Requires:       glycin-loaders
Requires:       gsettings-desktop-schemas
Requires:       gvfs
Requires:       gvfs-smb
Requires:       hicolor-icon-theme
Requires:       poppler-utils
Requires:       shared-mime-info
Requires:       (ffmpeg-free or ffmpeg)
Recommends:     7zip
Recommends:     ffmpegthumbnailer
Recommends:     xdg-terminal-exec

%description
Luciole is a native Wayland file manager with grid, list and Miller column
views, tabs, split view and live file previews. It also provides an
xdg-desktop-portal FileChooser backend.
Luciole 是一个原生 Wayland 文件管理器，提供网格 / 列表 / Miller 多列视图、
标签页、分屏和实时文件预览，并可作为 xdg-desktop-portal 的文件选择器后端。

%prep
%autosetup -n %{name}-%{commit}

%build
%meson \
  -Dtests=disabled \
  -Dnative_optimizations=false \
  -Dbuild_revision=%{shortcommit}
%meson_build

%install
%meson_install
install -Dpm 0644 lib/assets/fonts/tabler-icons-license.txt \
  %{buildroot}%{_licensedir}/%{name}/tabler-icons-license.txt

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%license LICENSE
%doc README.md PACKAGING.md
%{_licensedir}/%{name}/tabler-icons-license.txt
%{_bindir}/luciole
%{_datadir}/luciole/
%{_datadir}/applications/dev.noctalia.luciole.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.luciole.svg
%{_datadir}/dbus-1/services/dev.noctalia.luciole.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luciole.service
%{_datadir}/xdg-desktop-portal/portals/luciole.portal
%{_datadir}/bash-completion/completions/luciole
%{_datadir}/zsh/site-functions/_luciole
%{_datadir}/fish/vendor_completions.d/luciole.fish

%changelog
* Wed Nov 18 2026 Weng <khoocw97@gmail.com> - 20261117git.d8755c5-1
- Initial package
