%global libname btchip
%global srcname %{libname}-python
%global sum Python communication library for Ledger Hardware Wallet products
%global desc %{srcname} is a python API for communicating primarily with the \
Ledger HW.1 hardware bitcoin wallet. This library is also adds compatibility \
to Electrum in order to use the "Nano", "Nano S", and other Ledger-based \
hardware wallets.

Name:     python-%{libname}
Version:  0.1.18
Release:  2%{?dist}
Summary:  %{sum}

License:  ASL 2.0
URL:      https://github.com/LedgerHQ/%{srcname}
Source0:  https://github.com/LedgerHQ/%{srcname}/archive/v%{version}.tar.gz

BuildArch:     noarch
# Tests require these but dont' work without internet
#BuildRequires: libusbx-devel systemd-devel


%description
%{desc}


%package -n python2-%{libname}
Summary: %{sum}
BuildRequires: python2-devel
Requires: python2-hidapi hidapi >= 0.7.99
%{?python_provide:%python_provide python2-%{libname}}

%description -n python2-%{libname}
%{desc}


#%%package -n python3-%%{libname}
#Summary: %%{sum}
#BuildRequires: python3-devel
#Requires: python3-hidapi hidapi >= 0.7.99
#%%{?python_provide:%%python_provide python3-%%{libname}}
#
#%%description -n python3-%%{libname}
#%%{desc}


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
#%%py3_build


%install
%py2_install
#%%py3_install


%check
# Current tests try to contact PyPi and fail on Koji
#%%{__python2} setup.py test
#%%{__python3} setup.py test


%files -n python2-%{libname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*


#%%files -n python3-%%{libname}
#%%license LICENSE
#%%doc README.md
#%%{python3_sitelib}/*


%changelog
* Tue Jan 3 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.18-2
- Improve SPEC for most recent python packaging guidelines

* Sun Jan 1 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.18-1
- Initial packaging of btchip-python for Fedora
