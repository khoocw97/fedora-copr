%global debug_package %{nil}

Name:           lxgw-fonts
Version:        1.0
Release:        2%{?dist}
Summary:        LXGW Font Series (Bright GB/TC) and NeoXiHeiPlus fonts
Summary(zh_CN): 霞鹜系列字体（Bright 简繁 + 新晰黑 Plus）
License:        OFL-1.1 AND IPA
URL:            https://github.com/lxgw
# LxgwBright 26.10.22 (2026-10-22), LxgwNeoXiHei v1.309 (2026-11-10)
Source0:        https://github.com/lxgw/LxgwBright/releases/download/26.10.22/LXGWBrightGB.7z
Source1:        https://github.com/lxgw/LxgwBright/releases/download/26.10.22/LXGWBrightTC.7z
Source2:        https://github.com/lxgw/LxgwNeoXiHei/releases/download/v1.309/LXGWNeoXiHeiPlus.ttf
Source3:        https://raw.githubusercontent.com/lxgw/LxgwBright/26.10.22/OFL.txt
Source4:        https://raw.githubusercontent.com/lxgw/LxgwNeoXiHei/v1.309/LICENSE.md

BuildArch:      noarch
BuildRequires:  p7zip
BuildRequires:  p7zip-plugins

%description
LXGW font bundle: Bright GB/TC 26.10.22, NeoXiHeiPlus v1.309.
霞鹜字体合集：Bright 简繁 26.10.22，新晰黑 Plus v1.309。
%{_datadir}/fonts/lxgw。

%prep
cp %{SOURCE3} ./OFL.txt
cp %{SOURCE4} ./LICENSE.md

%build
# no build, prebuilt fonts

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/fonts/lxgw

7z x %{SOURCE0} -o%{_builddir}
7z x %{SOURCE1} -o%{_builddir}
install -m 0644 %{_builddir}/LXGWBrightGB/*.ttf %{buildroot}%{_datadir}/fonts/lxgw/
install -m 0644 %{_builddir}/LXGWBrightTC/*.ttf %{buildroot}%{_datadir}/fonts/lxgw/
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/fonts/lxgw/

%files
%license OFL.txt
%license LICENSE.md
%{_datadir}/fonts/lxgw/*.ttf

%changelog
* Wed Nov 18 2026 Weng <khoocw97@gmail.com> - 1.0-2
- Update LxgwBright to 26.10.22 (GB/TC), LxgwNeoXiHeiPlus to v1.309
* Mon Sep 21 2026 Weng <khoocw97@gmail.com>
- Initial package: LxgwBright v5.528 (GB/TC) + LxgwNeoXiHeiPlus v1.305
