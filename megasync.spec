%global debug_package %{nil}

%global commit      76c343ed96cba55d1b3a1b34cc691d19b39668f8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260903
# SDK submodule pinned by upstream at this commit (see src/MEGASync/control/Version.h VER_SDK_ID)
%global sdk_commit  8775533fe50255723c45ab8abf4e14285a592d51
%global sdk_short   %(c=%{sdk_commit}; echo ${c:0:7})

Name:           megasync
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        MEGA Desktop App - sync and backup client
Summary(zh_CN): MEGA 桌面客户端 - 同步与备份
License:        MEGA Limited Code Licence
URL:            https://github.com/meganz/MEGAsync
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
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
BuildRequires:  qt5-qtbase-devel >= 5.15
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtdeclarative-devel
# System deps used when VCPKG_ROOT is empty (see CMakeLists.txt: "Using system dependencies").
# Upstream CI builds these via vcpkg; keep them optional where Fedora coverage is thin.
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
Requires:       qt5-qtbase >= 5.15
Requires:       qt5-qtsvg
Requires:       qt5-qtdeclarative
Requires:       qqc2-desktop-style

Recommends:     xdg-desktop-portal
Suggests:       nautilus-megasync
Suggests:       dolphin-megasync
Suggests:       nemo-megasync
Suggests:       thunar-megasync

# Upstream installs to /opt/megasync/lib with RPATH; silence Fedora check.
%if 0%{?fedora} && 0%{?fedora} >= 35
%define __brp_check_rpaths %{nil}
%endif

%description
MEGAsync is the MEGA desktop client for Linux, Windows and macOS.
It syncs selected folders and backs up data to MEGA with a Qt-based
GUI, shell integrations and background transfers.
MEGAsync 是 MEGA 的桌面客户端，支持 Linux / Windows / macOS，提供
文件夹同步、备份、Qt 图形界面、文件管理器集成与后台传输。

%prep
%autosetup -n MEGAsync-%{commit} -a 1
# GitHub archive does not contain submodules - inject SDK.
rm -rf src/MEGASync/mega
mkdir -p src/MEGASync/mega
tar -xzf %{SOURCE1} --strip-components=1 -C src/MEGASync/mega
# Offline build: upstream downloads .clang-format at configure time.
# Pre-create it to avoid file(DOWNLOAD) fatal error.
if [ ! -f .clang-format ]; then
  touch .clang-format
  sed -i '/include(get_clang_format)/d; /get_clang_format()/d' CMakeLists.txt || true
fi
# Guard empty vcpkg install dir (no VCPKG_ROOT) - otherwise
# install(DIRECTORY "${VCPKG_INSTALLED_DIR}/...") warns on missing dir.
sed -i 's|install(DIRECTORY "${vcpkg_lib_folder}"|if(EXISTS "${VCPKG_INSTALLED_DIR}")\n  install(DIRECTORY "${vcpkg_lib_folder}"|' src/MEGASync/CMakeLists.txt
sed -i '/PATTERN "pkgconfig" EXCLUDE/{n; s/.*/&\nendif()/}' src/MEGASync/CMakeLists.txt || true
# Embed build id from Release (mirrors upstream megasync.spec).
mega_build_id=$(echo %{release} | sed "s/\\.[^.]*$//" | sed "s/[^.]*\\.//" | sed "s/[^0-9]//g")
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
# Custom libdir (desktopapp_configuration.cmake: opt/megasync/lib, gfxworker optional)
%dir /opt/megasync
%dir /opt/megasync/lib
/opt/megasync/lib/

%changelog
* Wed Sep 17 2026 Weng <khoocw97@gmail.com> - 20260903git.76c343e-1
- Initial package (Qt5 system build, no vendored Qt)
