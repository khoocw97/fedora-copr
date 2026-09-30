%global debug_package %{nil}

%global commit      815d4385afb844f74243a6bc1c7836c4fbebe830
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260923

Name:           fuzzel
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        App launcher and fuzzy finder for Wayland, inspired by rofi
Summary(zh_CN): Wayland 应用启动器与模糊查找器（类 rofi）
License:        MIT
URL:            https://codeberg.org/dnkl/fuzzel
# NOTE: Codeberg is upstream; commit archives extract to %{name}/.
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc
BuildRequires:  meson >= 0.58
BuildRequires:  nanosvg-devel
BuildRequires:  tllist-static
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fcft) >= 3.3.1
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(pixman-1) >= 0.46.0
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(tllist) >= 1.0.1
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

%description
Fuzzel is a Wayland-native application launcher and fuzzy finder, inspired by
rofi and dmenu.
Fuzzel 是一个 Wayland 原生应用启动器与模糊查找器，灵感来自 rofi 与 dmenu。

%prep
%autosetup -n %{name} -p1

%build
%meson \
  -Dsystem-nanosvg=enabled \
  %{nil}
%meson_build

%install
%meson_install
# Will be installed to correct location with rpm macros
rm %{buildroot}%{_docdir}/%{name}/LICENSE

%check
%meson_test

%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/%{name}
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/fish/vendor_completions.d/*.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/*.5*
%{_sysconfdir}/xdg/%{name}/

%changelog
* Tue Sep 29 2026 Weng <khoocw97@gmail.com>
- Initial package
