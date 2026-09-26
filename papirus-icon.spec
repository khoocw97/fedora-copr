%global debug_package %{nil}

Name:           papirus-icon
Version:        20260801
Release:        1%{?dist}
Summary:        Pixel perfect SVG icon theme for Linux
Summary(zh_CN): Linux 下精美还原的 SVG 图标主题
License:        GPL-3.0-only AND CC-BY-SA-4.0 AND LGPL-3.0-or-later
URL:            https://github.com/PapirusDevelopmentTeam/papirus-icon-theme
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
Requires:       hicolor-icon-theme
# same files as Fedora's papirus-icon-theme under different package name,
Conflicts:      papirus-icon-theme

%description
Papirus is a free and open source SVG icon theme for Linux, based on
Paper Icon Set with Hardcode-Tray, KDE colorscheme and Folder Color
support. This package ships the 3 variants Papirus, Papirus-Dark and
Papirus-Light.
Papirus 是基于 Paper Icon Set 的开源 SVG 图标主题，支持 Hardcode-Tray、
KDE 配色与文件夹改色。本包提供 Papirus、Papirus-Dark、Papirus-Light
三个变体。

%prep
%autosetup -n papirus-icon-theme-%{version}

%build
# no build, prebuilt SVG icon theme (upstream `make install` only copies files)

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} PREFIX=/usr

%check
test -f Papirus/index.theme
test -f Papirus-Dark/index.theme
test -f Papirus-Light/index.theme
# no broken symlinks (same idiom as upstream `make test_symlinks`)
find Papirus Papirus-Dark Papirus-Light -xtype l -print -exec false '{}' +

%files
%license LICENSE
%doc AUTHORS README.md CHANGELOG.md
%{_datadir}/icons/Papirus/
%{_datadir}/icons/Papirus-Dark/
%{_datadir}/icons/Papirus-Light/

%changelog
* Sat Sep 26 2026 Weng <khoocw97@gmail.com>
- Initial package: 20260801 tag (Papirus/Papirus-Dark/Papirus-Light)
