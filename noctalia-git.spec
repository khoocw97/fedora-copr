%global debug_package %{nil}

%global commit      30254799f51c6bdb06fa21936e36214c93a455b5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261125

Name:           noctalia-git
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        A sleek, customizable desktop shell crafted for Wayland
Summary(zh_CN): 为 Wayland 打造的精致可定制桌面 Shell
License:        Apache-2.0 AND MIT AND BSD-3-Clause AND HPND-sell-variant AND LGPL-2.1-or-later
URL:            https://github.com/noctalia-dev/noctalia
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

# File conflicts with the release package: /usr/bin/noctalia, /usr/share/noctalia,
# the desktop entries and the hicolor icon.
Conflicts:      noctalia

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  stb_image_resize2-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libical)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libqalculate)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libsecret-1) >= 0.20
BuildRequires:  pkgconfig(libsodium) >= 1.0.18
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(md4c)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wireplumber-0.5)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       git-core
Requires:       hicolor-icon-theme
Requires:       pipewire
Requires:       sound-theme-freedesktop

Recommends:     ddcutil
Recommends:     power-profiles-daemon
Recommends:     upower
Recommends:     (oo7-daemon or gnome-keyring or kf6-kwallet)
# dlopen-ed in src/render/core/heif_library.cpp
Recommends:     libheif.so.1()(%{__isa_bits}bit)
Suggests:       oo7-daemon

Provides:       PolicyKit-authentication-agent
# Vendored by default; upstream has an all-or-nothing system_libraries option and
# none of the four are packaged separately in Fedora.
Provides:       bundled(fzy) = 1.1
Provides:       bundled(luau) = 0.742
Provides:       bundled(material-color-utilities) = 1a34bd2
Provides:       bundled(wuffs) = 0.4.0.alpha.9

%description
Noctalia is a native Wayland desktop shell for people who want a polished,
configurable Linux desktop without stitching together a separate bar, launcher,
notification daemon, lock screen, wallpaper tool, and settings UI.
Noctalia 是一个原生 Wayland 桌面 Shell，把状态栏、启动器、通知守护、
锁屏、壁纸与设置界面整合为一体。

%prep
%autosetup -n noctalia-%{commit}

# Give the bundled license files distinct names for %%license.
cp lib/assets/fonts/tabler-icons-license.txt LICENSE.tabler
cp lib/third_party/wuffs/LICENSE-APACHE LICENSE-Apache-2.0.wuffs
cp lib/third_party/wuffs/LICENSE-MIT LICENSE-MIT.wuffs
cp third_party/fzy/LICENSE LICENSE.fzy
cp third_party/luau/LICENSE.txt LICENSE.luau
cp third_party/luau/lua_LICENSE.txt LICENSE.luau_lua
cp third_party/material_color_utilities/LICENSE LICENSE.material-color_utilities

%build
%meson \
  -Dtests=disabled \
  -Dnative_optimizations=false
%meson_build

%install
%meson_install

# Completions are generated from the built binary, there are no install rules.
install -d -m 0755 %{buildroot}%{bash_completions_dir}
%{buildroot}%{_bindir}/noctalia completions bash > %{buildroot}%{bash_completions_dir}/noctalia
install -d -m 0755 %{buildroot}%{fish_completions_dir}
%{buildroot}%{_bindir}/noctalia completions fish > %{buildroot}%{fish_completions_dir}/noctalia.fish
install -d -m 0755 %{buildroot}%{zsh_completions_dir}
%{buildroot}%{_bindir}/noctalia completions zsh > %{buildroot}%{zsh_completions_dir}/_noctalia

%check
%{buildroot}%{_bindir}/noctalia --version

%files
%license LICENSE LICENSE.tabler LICENSE-Apache-2.0.wuffs LICENSE-MIT.wuffs
%license LICENSE.fzy LICENSE.luau LICENSE.luau_lua LICENSE.material-color_utilities
%doc README.md
%{_bindir}/noctalia
%{_libexecdir}/noctalia/noctalia-pam-helper
%{_datadir}/applications/dev.noctalia.Noctalia.desktop
%{_datadir}/applications/dev.noctalia.Noctalia.Annotator.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg
%{_datadir}/noctalia/
%{bash_completions_dir}/noctalia
%{fish_completions_dir}/noctalia.fish
%{zsh_completions_dir}/_noctalia

%changelog
* Wed Nov 18 2026 Weng <khoocw97@gmail.com> - 20261118git.f737e2d-1
- Bump to f737e2d (upstream icon color-scheme work, no packaging changes)
* Wed Nov 18 2026 Weng <khoocw97@gmail.com> - 20261117git.4e1dcb6-1
- Initial package (git snapshot)
