%global debug_package %{nil}

%global commit      cdcf2acc2027a4db07e9f65b046d4e3119ee8a08
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260811

Name:           vm-curator
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        A TUI application to manage QEMU VM library
Summary(zh_CN): 管理 QEMU 虚拟机库的 TUI 应用
License:        MIT
URL:            https://github.com/mroboff/vm-curator
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libudev)

Requires:       bash
Requires:       qemu-img
Requires:       qemu-system-x86-core

Recommends:     dnsmasq
Recommends:     edk2-ovmf
Recommends:     passt
Recommends:     swtpm
Recommends:     virt-viewer

%description
vm-curator is a fast and friendly Rust TUI for managing desktop QEMU/KVM
virtual machines, with VM discovery, a creation wizard with 130+
pre-configured OS profiles, snapshot management, USB passthrough, GPU
passthrough, managed virtual networks, and VM import from libvirt and
Quickemu.
vm-curator 是一个用于管理桌面 QEMU/KVM 虚拟机的 Rust TUI 应用，提供虚拟机
发现、带 130+ 预置 OS 配置的创建向导、快照管理、USB 直通、GPU 直通、虚拟
网络管理，并支持从 libvirt 与 Quickemu 导入虚拟机。

%prep
%autosetup -n %{name}-%{commit}

%build
cargo build --locked --release

%install
install -Dpm 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%check
%{buildroot}%{_bindir}/%{name} --version
%{buildroot}%{_bindir}/%{name} --help

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}

%changelog
* Mon Sep 14 2026 Weng <khoocw97@gmail.com>
- Initial package
