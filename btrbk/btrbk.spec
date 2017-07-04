Name:           btrbk
Version:        0.25.0
Release:        1%{?dist}
Summary:        Tool for creating snapshots and remote backups of btrfs subvolumes

License:        GPLv3
URL:            https://digint.ch/btrbk/
Source0:        https://github.com/digint/%{name}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  systemd

Requires:       perl btrfs-progs
Requires:       openssh-clients

%{?perl_default_filter}


%description
Tool for creating snapshots and remote backups of btrfs subvolumes


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
* Tue Jul  4 2017 Mike Goodwin <xenithorb@fedoraproject.org> - 0.25.0-1
- Initial packaging
