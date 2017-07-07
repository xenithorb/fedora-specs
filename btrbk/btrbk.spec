Name:           btrbk
Version:        0.25.0
Release:        4%{?dist}
Summary:        Tool for creating snapshots and remote backups of btrfs sub-volumes
License:        GPLv3+
URL:            https://digint.ch/btrbk/
Source0:        https://digint.ch/download/%{name}/releases/%{name}-%{version}.tar.xz
#Source0:        https://github.com/digint/%%{name}/archive/v%%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd perl-generators

Requires:       btrfs-progs

%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       openssh-clients pv
%else
Recommends:     openssh-clients pv
%endif


%description
‎Backup tool for btrfs sub-volumes, using a configuration file, allows
‎creation of backups from multiple sources to multiple destinations,
‎with ssh and flexible retention policy support (hourly, daily,
‎weekly, monthly)


%prep
%autosetup


%build
# Until patched upstream, modify Makefile to perserve timestamps during install
# See: https://github.com/digint/btrbk/pull/164/files for upstream PR
sed -i '/install/s/-Dm\([0-9]\{3,4\}\)/-pDm\1/' Makefile


%install
make DESTDIR=%{buildroot} \
    install-bin \
    install-systemd \
    install-share

install -pDm644 doc/btrbk.1 "%{buildroot}%{_mandir}/man1/btrbk.1"
install -pDm644 doc/ssh_filter_btrbk.1 "%{buildroot}%{_mandir}/man1/ssh_filter_btrbk.1"
install -pDm644 doc/btrbk.conf.5 "%{buildroot}%{_mandir}/man5/btrbk.conf.5"

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
* Fri Jul 07 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.25.0-4
- Removed perl from Requires, auto-generated
- Removed %%{?systemd_requires}, for scriptlets only

* Wed Jul  5 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-3
- License was GPLv3+ not GPLv3
- Add perl-generators for BuildRequires
- Add -p to all install commands in Makefile and in spec (with sed)
  - Patch submitted upstream: https://github.com/digint/btrbk/pull/164
- Fix if statement for RHEL detection
- Spelling of subvolumes -> sub-volumes to satisfy rpmlint
- Removed %%{?perl_default_filter} macro, unnecessary

* Wed Jul  5 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-2
- Added a more verbose description per the developer
- Changed Source0 to the official source tarball
- Include pv as a weak dependency, as well as openssh-clients
- Add if statement because <= RHEL7 doesn't have Recommends:

* Tue Jul  4 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-1
- Initial packaging
