%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global _hardened_build 1
%global __requires_exclude (npm)
%global __provides_exclude (npm)
%global project Rocket.Chat.Electron
%global repo %{project}
%global node_ver 6.11.3
%global _optdir /opt

# commit
%global _commit develop
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		rocketchat-desktop
Version:	2.10.0
Release:	100.git%{_shortcommit}%{?dist}
Summary:	Rocket.Chat Native Cross-Platform Desktop Application via Electron
Group:		Applications/Communications
Vendor:		Rocket.Chat Community
License:	MIT
URL:		https://rocket.chat/
Source0:	https://github.com/RocketChat/%{project}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
AutoReq:	0

Obsoletes: rocketchat <= %{version}

BuildRequires: npm
BuildRequires: git-core
BuildRequires: gcc-c++
BuildRequires: node-gyp
BuildRequires: nodejs >= %{node_ver}
BuildRequires: libX11-devel libXScrnSaver-devel

%description
From group messages and video calls all the way to help desk killer features.
Our goal is to become the number one cross-platform open source chat solution


%prep
%setup -q -n %repo-%{_commit}


%build

node-gyp -v; %{__nodejs} -v; npm -v

# Remove deb and rpm targets, only output dir
%{__python} <<-'EOF'
	import json
	with open("package.json", "r+") as file:
	    package = json.load(file)
	    package['build']['linux']['target'] = ["dir"]
	    package['name'] = "%{name}"
	    file.seek(0)
	    json.dump(package, file, indent=4)
	EOF

npm install
npm run release


%install
%{__install} -d %{buildroot}%{_datadir}/applications
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_optdir}/%{name}
%{__install} -Dm644 build/icons/512x512.png \
	%{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%{__cp} -r dist/linux-*unpacked/* %{buildroot}%{_optdir}/%{name}/

%{__cat} <<-'EOF' > %{buildroot}%{_datadir}/applications/%{name}.desktop
	[Desktop Entry]
	Name=Rocket.Chat+
	Comment=Rocket.Chat Native Cross-Platform Desktop Application via Electron.
	Exec=/usr/bin/%{name}
	Terminal=false
	Type=Application
	Icon=%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
	Categories=GNOME;GTK;Network;InstantMessaging
	StartupWMClass=Rocket.Chat+
	EOF

%{__cat} <<-'EOF' > %{buildroot}%{_bindir}/%{name}
	#!/bin/sh
	exec %{_optdir}/%{name}/%{name}
	EOF

%{__chmod} +x %{buildroot}%{_bindir}/%{name}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:


%postun
if [ $1 -eq 0 ]; then
	/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
	/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:


%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:


%files
%defattr(-,root,root,-)
%attr(755,-,-) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_optdir}/%{name}


%changelog
* Wed Oct 4 2017 xenithorb <mike@mgoodwin.net> - 2.9.0-100.gitdevelop
- Bump spec
* Sat May 6 2017 xenithorb <mike@mgoodwin.net> - 2.8.0-102.gitdevelop
- Spec updates
- Use exec instead of env for wrapper
* Wed May 3 2017 xenithorb <mike@mgoodwin.net> - 2.8.0-100.gitdevelop
- Release channel version 2.8.0-develop
* Mon Mar 6 2017 xenithorb <mike@mgoodwin.net> - 2.6.0-100.git70cb0d0
- Development channel ver 2.6.0
- Upgrade node version to 4.7.1
* Fri Dec 23 2016 xenithorb <mike@mgoodwin.net> - 1.3.3-100.git2142556
- Development channel ver 1.3.3
- Upgrade node version to 4.6.2
- Electron version to 1.4.3
* Sat Jun 4 2016 xenithorb <mike@mgoodwin.net> - 1.3.1-0.git3ed2b6d
- Release 1.3.1
- Changed build to do exactly what is done for Ubuntu deb sans building .deb pkg
* Wed Mar 23 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-2.gitf74b825
- Release 1.2.0
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1.gitabb7b81
- Initial package
