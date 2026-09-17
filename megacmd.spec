%global debug_package %{nil}

%global commit      6505327a5a7a0e94f26f611f83b024aeeb63582c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260828
# SDK submodule pinned by upstream (see sdk mode 160000 in MEGAcmd tree)
%global sdk_commit  8775533fe50255723c45ab8abf4e14285a592d51
%global sdk_short   %(c=%{sdk_commit}; echo ${c:0:7})

Name:           megacmd
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        MEGA Command Line Interactive and Scriptable Application
Summary(zh_CN): MEGA 命令行交互与脚本化客户端
License:        BSD-2-Clause
URL:            https://github.com/meganz/MEGAcmd
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/meganz/sdk/archive/%{sdk_commit}.tar.gz#/sdk-%{sdk_short}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.16
BuildRequires:  pkgconf-pkg-config
BuildRequires:  hicolor-icon-theme
BuildRequires:  fuse-devel
BuildRequires:  readline-devel
BuildRequires:  pcre-devel
# System deps when VCPKG_ROOT is empty (see CMakeLists.txt: "Using system dependencies").
# Upstream CI builds these via vcpkg; list Fedora equivalents. pdfium not in Fedora
# so FULL_REQS is OFF by default (see %build).
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

Requires:       fuse
Requires:       procps-ng

# Upstream installs to /opt/megacmd/lib with RPATH; silence Fedora check.
%if 0%{?fedora} && 0%{?fedora} >= 35
%define __brp_check_rpaths %{nil}
%endif

%description
MEGAcmd provides non-UI access to MEGA services with synchronization,
backup and WebDAV/streaming support. It runs a server (MEGAcmdServer),
an interactive shell (MEGAcmdShell) and non-interactive mega-* clients
(mega-put, mega-get, mega-sync, ...).
MEGAcmd 为 MEGA 提供无界面访问，支持同步、备份与 WebDAV/串流；由
MEGAcmdServer、交互式 shell 与一系列 mega-* 非交互客户端组成。

%prep
%autosetup -n MEGAcmd-%{commit} -a 1
# GitHub archive does not contain submodules - inject SDK.
rm -rf sdk
mkdir -p sdk
tar -xzf %{SOURCE1} --strip-components=1 -C sdk
# Embed build id from Release (mirrors upstream build/templates/megacmd/megacmd.spec).
mega_build_id=$(echo %{release} | cut -d'.' -f1 | sed "s/[^0-9]//g")
sed -i -E "s/(^#define MEGACMD_BUILD_ID )[0-9]*/\1${mega_build_id}/g" src/megacmdversion.h.in

%build
# VCPKG_ROOT defaults to ../vcpkg and auto-clones; force system deps.
# FULL_REQS=OFF avoids requiring pdfium (not in Fedora); keep fuse where available.
%cmake \
  -DVCPKG_ROOT="" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DFULL_REQS=OFF \
  -DENABLE_MEGACMD_TESTS=OFF
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}/opt/megacmd/lib

%check
test -x %{buildroot}%{_bindir}/mega-cmd
test -x %{buildroot}%{_bindir}/mega-cmd-server
test -x %{buildroot}%{_bindir}/mega-exec
%{buildroot}%{_bindir}/mega-exec --help 2>&1 | head -n 5

%files
%license LICENSE
%doc README.md UserGuide.md
%{_bindir}/mega-*
%{_sysconfdir}/bash_completion.d/megacmd_completion.sh
%config(noreplace) %{_sysconfdir}/sysctl.d/99-megacmd-inotify-limit.conf
%dir /opt/megacmd
%dir /opt/megacmd/lib
/opt/megacmd/lib/

%changelog
* Wed Sep 17 2026 Weng <khoocw97@gmail.com> - 20260828git.6505327-1
- Initial package (system deps, VCPKG_ROOT disabled, FULL_REQS=OFF)
