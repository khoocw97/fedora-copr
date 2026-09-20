%global debug_package %{nil}

Name:           bibata-cursor-themes
Version:        2.0.7
Release:        1%{?dist}
Summary:        OpenSource, compact and material designed cursor set
Summary(zh_CN): 开源、紧凑、Material 风格的光标主题
License:        GPL-3.0-only
URL:            https://github.com/ful1e5/Bibata_Cursor
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/bitmaps.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-pip

%description
Bibata is an open source, compact and material designed cursor set,
hand-designed by Abdulkaiz Khatri. This package ships the 6 normal
variants (Modern/Original × Amber/Classic/Ice); right-hand variants are
not built.
Bibata 是由 Abdulkaiz Khatri 手绘的开源、紧凑、Material 风格光标集，本包
仅打包 6 个常规变体（Modern/Original × Amber/Classic/Ice），不含 Right-hand
变体。

%prep
%autosetup -c
%autosetup -T -D -a 1
mv bitmaps Bibata_Cursor-%{version}

%build
export PATH="/builddir/.local/bin:%{_builddir}/.local/bin:$PATH"
pip install --quiet --no-warn-script-location clickgen

cd Bibata_Cursor-%{version}

declare -A variants
variants["Bibata-Modern-Amber"]="Yellowish and rounded edge Bibata cursors"
variants["Bibata-Modern-Classic"]="Black and rounded edge Bibata cursors"
variants["Bibata-Modern-Ice"]="White and rounded edge Bibata cursors"
variants["Bibata-Original-Amber"]="Yellowish and sharp edge Bibata cursors"
variants["Bibata-Original-Classic"]="Black and sharp edge Bibata cursors"
variants["Bibata-Original-Ice"]="White and sharp edge Bibata cursors"

for key in "${!variants[@]}"; do
  ctgen configs/normal/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "${variants[$key]}"
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons
for theme in Bibata_Cursor-%{version}/themes/*; do
  mv "$theme" %{buildroot}%{_datadir}/icons/
  chmod 0755 %{buildroot}%{_datadir}/icons/$(basename "$theme")
done

%files
%license Bibata_Cursor-%{version}/LICENSE
%doc Bibata_Cursor-%{version}/README.md
%{_datadir}/icons/Bibata-*

%changelog
* Mon Sep 21 2026 Weng <khoocw97@gmail.com>
- Initial package (6 normal variants only, right-hand excluded)
