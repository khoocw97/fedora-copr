%global debug_package %{nil}

Name:           lxgw-fonts
Version:        1.0
Release:        1%{?dist}
Summary:        LXGW Font Series (Bright GB/TC) and NeoXiHeiPlus fonts
Summary(zh_CN): 霞鹜系列字体（Bright 简繁 + 新晰黑 Plus）
License:        OFL-1.1 AND IPA
URL:            https://github.com/lxgw
# LxgwBright v5.528 (2026-03-23), LxgwNeoXiHei v1.305 (2026-08-20)
Source0:        https://github.com/lxgw/LxgwBright/releases/download/v5.528/LXGWBrightGB.7z
Source1:        https://github.com/lxgw/LxgwBright/releases/download/v5.528/LXGWBrightTC.7z
Source2:        https://github.com/lxgw/LxgwNeoXiHei/releases/download/v1.305/LXGWNeoXiHeiPlus.ttf
Source3:        https://raw.githubusercontent.com/lxgw/LxgwBright/main/OFL.txt
Source4:        https://raw.githubusercontent.com/lxgw/LxgwNeoXiHei/main/LICENSE.md

BuildArch:      noarch
BuildRequires:  p7zip
BuildRequires:  p7zip-plugins

%description
LXGW font bundle: Bright GB/TC v5.528, NeoXiHeiPlus v1.305.
霞鹜字体合集：Bright 简繁 v5.528，新晰黑 Plus v1.305。
%{_datadir}/fonts/lxgw。

%prep
# nothing to patch, sources are binary archives

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
%license %{SOURCE3}
%license %{SOURCE4}
%{_datadir}/fonts/lxgw/*.ttf

%changelog
* Sun Sep 21 2026 Weng <khoocw97@gmail.com>
- Initial package: LxgwBright v5.528 (GB/TC) + LxgwNeoXiHeiPlus v1.305
