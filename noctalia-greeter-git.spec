%global debug_package %{nil}

%global commit      603ba85bb759c0d03ecc1e189402f93835eba68d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261121

Name:           noctalia-greeter-git
Version:        %{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        A minimal login greeter for greetd that matches the look and feel of Noctalia Shell
Summary(zh_CN): 与 Noctalia Shell 视觉风格一致的 greetd 极简登录界面
License:        MIT AND (Apache-2.0 OR MIT)
URL:            https://github.com/noctalia-dev/noctalia-greeter
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?fedora} && 0%{?fedora} < 44
ExclusiveArch:  none
%else
ExclusiveArch:  x86_64 aarch64
%endif

# Shares every installed path with the release package.
Conflicts:      noctalia-greeter

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  stb_image_resize2-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20
BuildRequires:  pkgconfig(xkbcommon)

Requires:       dbus-daemon
Requires:       greetd

Recommends:     accountsservice
Recommends:     polkit

%description
Noctalia Greeter is the screen you see before your desktop session starts.
It lets you pick a user, enter your password, choose a Wayland session, and pick
a color scheme - with the same visual language as Noctalia Shell.
Noctalia Greeter 是进入桌面会话前的登录界面，可选择用户、输入密码、选择
Wayland 会话与配色方案，视觉风格与 Noctalia Shell 保持一致。

%prep
%autosetup -n noctalia-greeter-%{commit}

%build
# Upstream sets 'c_args=-Wno-error=switch' in default_options, which drops the
# distro C flags; force PIE so C objects link into the PIE binaries RPM expects.
%meson \
  -Db_pie=true \
  -Dnative_optimizations=false
%meson_build

%install
%meson_install
# Upstream's tmpfiles rule hardcodes the "greeter" session user; Fedora's greetd
# uses "greetd", so omit the rule and let the state helper create the directory:
#   GREETER_USER=greetd %{_bindir}/noctalia-greeter-apply-appearance --setup-system
rm -f %{buildroot}%{_prefix}/lib/tmpfiles.d/noctalia-greeter.conf

%check
%{buildroot}%{_bindir}/noctalia-greeter --version

%files
%license LICENSE
%license third_party/wuffs/LICENSE-APACHE third_party/wuffs/LICENSE-MIT
%doc README.md
%{_bindir}/noctalia-greeter
%{_bindir}/noctalia-greeter-apply-appearance
%{_bindir}/noctalia-greeter-compositor
%{_bindir}/noctalia-greeter-print-greetd-config
%{_bindir}/noctalia-greeter-session
%{_bindir}/noctalia-greeter-xsession
%{_datadir}/noctalia-greeter/
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy

%changelog
* Wed Nov 18 2026 Weng <khoocw97@gmail.com> - 20261116git.b8f95e0-1
- Initial package (git snapshot)
