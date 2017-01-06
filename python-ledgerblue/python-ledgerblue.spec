%global pipname ledgerblue
%global srcname blue-loader-python
%global sum Python communication library for next-generation Ledger Hardware Wallet products
%global desc This package contains Python tools to communicate with Ledger \
Blue and Nano S and manage applications life cycle (see also python2-btchip)

Name:     python-%{pipname}
Version:  0.1.8
Release:  0%{?dist}
Summary:  %{sum}
License:  ASL 2.0
URL:      https://github.com/LedgerHQ/%{srcname}
Source0:  https://github.com/LedgerHQ/%{srcname}/archive/%{version}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel systemd-devel libusb-devel
# Tests require these but don't work without internet
#BuildRequires: libusbx-devel systemd-devel


%description
%{desc}


%package -n python2-%{pipname}
Summary: %{sum}
Requires: hidapi >= 0.7.99
Requires: python2-crypto python2-future python2-pillow
%{?python_provide:%python_provide python2-%{pipname}}

%description -n python2-%{pipname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build


%install
%py2_install


%check
# Current tests try to contact PyPi and fail on Koji
#%%{__python2} setup.py test


%files -n python2-%{pipname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*


%changelog
* Fri Jan 6 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.1.8-0
- Initial packaging for Fedora
