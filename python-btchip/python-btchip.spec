

%global libname btchip
%global srcname %{libname}-python
%global sum Python communication library for Ledger Hardware Wallet products
%global desc %{srcname} is a python API for communicating primarily with the \
Ledger HW.1 hardware bitcoin wallet. This library also adds compatibility \
to Electrum in order to use the "Nano", "Nano S", and other Ledger-based \
hardware wallets.

Name:     python-%{libname}
Version:  0.1.21
Release:  3%{?dist}
Summary:  %{sum}

License:  ASL 2.0
URL:      https://github.com/LedgerHQ/%{srcname}
Source0:  https://github.com/LedgerHQ/%{srcname}/archive/v%{version}.tar.gz
Source1:  20-hw1.rules

BuildArch:     noarch
# Tests require these but don't work without internet
#BuildRequires: libusbx-devel systemd-devel
BuildRequires: systemd

%description
%{desc}

#------------------------------
# Package: python2-btchip
#------------------------------
%package -n python2-%{libname}
Summary: %{sum}
BuildRequires: python2-devel
Requires: python2-hidapi hidapi >= 0.7.99
Requires: python2-mnemonic python-%{libname}-common
%{?python_provide:%python_provide python2-%{libname}}

%description -n python2-%{libname}
%{desc}
#------------------------------


#------------------------------
# Package: python3-btchip
#------------------------------
%package -n python3-%{libname}
Summary: %{sum}
BuildRequires: python3-devel
Requires: python3-hidapi hidapi >= 0.7.99
Requires: python3-mnemonic python-%{libname}-common
%{?python_provide:%python_provide python3-%{libname}}


%description -n python3-%{libname}
%{desc}
#------------------------------


#------------------------------
# Package: python-btchip-common
#------------------------------
%package -n python-%{libname}-common
Summary: ${sum}

%description -n python-%{libname}-common
%{desc}
#------------------------------


#------------------------------
# Global
#------------------------------
%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install
mkdir -p %{buildroot}%{_udevrulesdir}
install -m644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/20-hw1.rules
#------------------------------


%check
# Current tests try to contact PyPi and fail on Koji
#%%{__python2} setup.py test


%files -n python2-%{libname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python3-%{libname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%files -n python-%{libname}-common
%{_udevrulesdir}/*


%changelog
* Mon Oct 16 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.21-3
- Add python-mnemonic dependency for BIP39 support during dongle setup
- New sub-package: python3-btchip (upstream added py3 support) (#1499686)
- New sub-package: python-btchip-common - current for the btchip udev rules
    - Add udev rules (20-hw1.rules) for automatic device recognition

* Wed Oct 04 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.21-2
- Update to 0.1.21

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 04 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.20-1
- Update to 0.1.20

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 4 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.18-3
- Final finishing touches after package review

* Tue Jan 3 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.18-2
- Improve SPEC for most recent python packaging guidelines

* Sun Jan 1 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.18-1
- Initial packaging of btchip-python for Fedora
