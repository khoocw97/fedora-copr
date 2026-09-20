%global debug_package %{nil}

Name:           maple-mono-fonts
Version:        7.9
Release:        1%{?dist}
Summary:        Maple Mono NF CN font
Summary(zh_CN): Maple Mono NF 中文版字体
License:        OFL-1.1
URL:            https://github.com/subframe7536/maple-font
Source0:        https://github.com/subframe7536/maple-font/releases/download/v7.9/MapleMono-NF-CN.zip

BuildArch:      noarch
BuildRequires:  unzip

%description
Maple Mono NF CN v7.9 — prebuilt TTFs with Nerd Font glyphs and
Simplified Chinese support.
Maple Mono NF CN v7.9 预编译字体，含 Nerd Font 图标与简中支持。

%prep
%autosetup -c -T
unzip -q %{SOURCE0} -d .

%build
# no build, prebuilt

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/fonts/maple
install -m 0644 *.ttf %{buildroot}%{_datadir}/fonts/maple/

%files
%license LICENSE.txt
%{_datadir}/fonts/maple/*.ttf

%changelog
* Mon Sep 21 2026 Weng <khoocw97@gmail.com>
- Initial package: v7.9
