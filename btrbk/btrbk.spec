Name:           btrbk
Version:        0.25.0
Release:        2%{?dist}
Summary:        Tool for creating snapshots and remote backups of btrfs subvolumes
License:        GPLv3
URL:            https://digint.ch/btrbk/
Source0:        https://digint.ch/download/%{name}/releases/%{name}-%{version}.tar.xz
#Source0:        https://github.com/digint/%%{name}/archive/v%%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd
Requires:       perl btrfs-progs

%if 0%{?rhel} <= 7
Requires:       openssh-clients pv
%else
Recommends:     openssh-clients pv
%endif

%{?perl_default_filter}


%description
‎Backup tool for btrfs subvolumes, using a configuration file, allows
‎creation of backups from multiple sources to multiple destinations,
‎with ssh and flexible retention policy support (hourly, daily,
‎weekly, monthly)


%prep
%autosetup


%build


%install
make DESTDIR=%{buildroot} \
    install-bin \
    install-systemd \
    install-share

install -Dm644 doc/btrbk.1 "%{buildroot}%{_mandir}/man1/btrbk.1"
install -Dm644 doc/ssh_filter_btrbk.1 "%{buildroot}%{_mandir}/man1/ssh_filter_btrbk.1"
install -Dm644 doc/btrbk.conf.5 "%{buildroot}%{_mandir}/man5/btrbk.conf.5"

rm -rf doc/*.{1,5}
mv %{buildroot}%{_sysconfdir}/btrbk/btrbk.conf{.example,}


%files
%doc doc/* README.md ChangeLog
%config(noreplace) %{_sysconfdir}/btrbk
%license COPYING
%{_sbindir}/btrbk
%{_unitdir}/btrbk.*
%{_datadir}/btrbk
%{_mandir}/man1/btrbk.1*
%{_mandir}/man1/ssh_filter_btrbk.1*
%{_mandir}/man5/btrbk.conf.5*


%changelog
* Wed Jul  5 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-2
- Added a more verbose description per the developer
- Changed Source0 to the official source tarball
- Include pv as a weak dependency, as well as openssh-clients
- Add if statement because <= RHEL7 doesn't have Recommends:

* Tue Jul  4 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-1
- Initial packaging
