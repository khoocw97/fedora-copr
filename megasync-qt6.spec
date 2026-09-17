%global debug_package %{nil}

%global commit      76c343ed96cba55d1b3a1b34cc691d19b39668f8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260903
# SDK submodule pinned by upstream at this commit (see src/MEGASync/control/Version.h VER_SDK_ID)
%global sdk_commit  8775533fe50255723c45ab8abf4e14285a592d51
%global sdk_short   %(c=%{sdk_commit}; echo ${c:0:7})

Name:           megasync-qt6
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        MEGA Desktop App - sync and backup client (Qt6)
Summary(zh_CN): MEGA 桌面客户端 - 同步与备份（Qt6）
License:        MEGA Limited Code Licence
URL:            https://github.com/meganz/MEGAsync
Source0:        https://github.com/meganz/MEGAsync/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/meganz/sdk/archive/%{sdk_commit}.tar.gz#/sdk-%{sdk_short}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.18
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconf
# Qt6: private Qt fully replaced. qtx11extras was Qt5-only; Qt6 drops WinExtras/MacExtras on Linux.
BuildRequires:  qt6-qtbase-devel >= 6.5
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel
# System deps when VCPKG_ROOT is empty (see CMakeLists.txt: "Using system dependencies").
BuildRequires:  openssl-devel
BuildRequires:  cryptopp-devel
BuildRequires:  libsodium-devel
BuildRequires:  curl-devel
BuildRequires:  sqlite-devel
BuildRequires:  pkgconfig(libicu-i18n)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  freeimage-devel
BuildRequires:  ffmpeg-free-devel
BuildRequires:  libmediainfo-devel

Requires:       hicolor-icon-theme
Requires:       qt6-qtbase >= 6.5
Requires:       qt6-qtsvg
Requires:       qt6-qtdeclarative

Recommends:     xdg-desktop-portal
Suggests:       nautilus-megasync
Suggests:       dolphin-megasync
Suggests:       nemo-megasync
Suggests:       thunar-megasync

Provides:       megasync = %{version}-%{release}
Conflicts:      megasync

# Upstream installs to /opt/megasync/lib with RPATH; silence Fedora check.
%if 0%{?fedora} && 0%{?fedora} >= 35
%define __brp_check_rpaths %{nil}
%endif

%description
MEGAsync is the MEGA desktop client for Linux, Windows and macOS.
This variant builds against system Qt6, fully replacing the vendored
qt-mega 5.15 (contrib/build_qt). It syncs selected folders and backs
up data to MEGA with a Qt-based GUI and shell integrations.
MEGAsync 是 MEGA 桌面客户端，此 Qt6 变体完全替换私有的 qt-mega
5.15，使用系统 Qt6 构建，提供文件夹同步、备份与文件管理器集成。

%prep
%autosetup -n MEGAsync-%{commit}
# GitHub archive does not contain submodules - inject SDK.
rm -rf src/MEGASync/mega
mkdir -p src/MEGASync/mega
tar -xzf %{SOURCE1} --strip-components=1 -C src/MEGASync/mega
# Offline build: upstream downloads .clang-format at configure time.
if [ ! -f .clang-format ]; then
  touch .clang-format
  sed -i '/include(get_clang_format)/d; /get_clang_format()/d' CMakeLists.txt || true
fi
# Guard empty vcpkg install dir (no VCPKG_ROOT).
sed -i 's|install(DIRECTORY "${vcpkg_lib_folder}"|if(EXISTS "${VCPKG_INSTALLED_DIR}")\n  install(DIRECTORY "${vcpkg_lib_folder}"|' src/MEGASync/CMakeLists.txt
sed -i '/PATTERN "pkgconfig" EXCLUDE/{n; s/.*/&\nendif()/}' src/MEGASync/CMakeLists.txt || true
# --- Qt5 -> Qt6 minimal port ---
# Upstream is Qt5-only (find_package(Qt5 ...), Qt5::*, qt5_create_translation).
# This is the smallest patch that lets cmake configure with Qt6; remaining
# API mismatches (QRegExp, Qt::MidButton renames, WinExtras/MacExtras) will
# surface as compile errors and need iterative fixes.
sed -i 's/find_package(Qt5/find_package(Qt6/g' src/MEGASync/CMakeLists.txt
sed -i 's/Qt5::/Qt6::/g' src/MEGASync/CMakeLists.txt
sed -i 's/Qt5_VERSION/Qt6_VERSION/g; s/Qt5_DIR/Qt6_DIR/g' src/MEGASync/CMakeLists.txt
sed -i 's/qt5_create_translation/qt6_create_translation/g' src/MEGASync/CMakeLists.txt
# Qt6 removed WinExtras/MacExtras; drop those find_package lines on Linux build.
sed -i '/find_package(Qt6 REQUIRED COMPONENTS WinExtras)/d' src/MEGASync/CMakeLists.txt || true
sed -i '/find_package(Qt6 REQUIRED COMPONENTS MacExtras/d' src/MEGASync/CMakeLists.txt || true
# Embed build id from Release (mirrors upstream megasync.spec).
mega_build_id=$(echo %{release} | sed "s/\.[^.]*$//" | sed "s/[^.]*\\.//" | sed "s/[^0-9]//g")
sed -i -E "s/VER_BUILD_ID([[:space:]]+)([0-9]*)/VER_BUILD_ID\\1${mega_build_id}/g" src/MEGASync/control/Version.h

%build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DENABLE_DESKTOP_UPDATE_GEN=OFF \
  -DENABLE_DESKTOP_APP_TESTS=OFF \
  -DENABLE_DESIGN_TOKENS_IMPORTER=OFF \
  -DENABLE_DESKTOP_UPDATER=OFF \
  -DUSE_BREAKPAD=OFF
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}/opt/megasync/lib
desktop-file-validate %{buildroot}%{_datadir}/applications/megasync.desktop || true
mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d
echo "fs.inotify.max_user_watches = 524288" > %{buildroot}%{_sysconfdir}/sysctl.d/99-megasync-inotify-limit.conf
mkdir -p %{buildroot}%{_docdir}/%{name}
if command -v lsb_release >/dev/null 2>&1; then
  lsb_release -ds > %{buildroot}%{_docdir}/%{name}/distro 2>/dev/null || true
  lsb_release -rs > %{buildroot}%{_docdir}/%{name}/version 2>/dev/null || true
fi
# Rename binary/desktop to avoid conflict when -qt6 package installed alongside test.
# Keep Provides/Conflicts for clean upgrade path.

%check
test -x %{buildroot}%{_bindir}/megasync
desktop-file-validate %{buildroot}%{_datadir}/applications/megasync.desktop || true

%files
%license LICENCE.md
%doc README.md README.linux.md
%{_bindir}/megasync
%{_datadir}/applications/megasync.desktop
%{_datadir}/icons/hicolor/*/apps/mega.png
%config(noreplace) %{_sysconfdir}/sysctl.d/99-megasync-inotify-limit.conf
%{_docdir}/%{name}/
%dir /opt/megasync
%dir /opt/megasync/lib
/opt/megasync/lib/

%changelog
* Wed Sep 17 2026 Weng <khoocw97@gmail.com> - 20260903git.76c343e-1
- Qt6 variant: system Qt6, drop vendored qt-mega, minimal Qt5->Qt6 sed
