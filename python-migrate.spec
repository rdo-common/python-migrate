%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define srcname sqlalchemy-migrate

Name: python-migrate
Version: 0.4.4
Release: 3%{?dist}
Summary: Schema migration tools for SQLAlchemy

Group: Development/Languages
License: MIT
URL: http://code.google.com/p/%{srcname}/
Source0: http://%{srcname}.googlecode.com/files/%{srcname}-%{version}.tar.gz
# Fix a test when migrate is not installed.  Applied upstream.
Patch0: python-migrate-shell-test.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools-devel
Requires: python-sqlalchemy >= 0.3.10

%description
Schema migration tools for SQLAlchemy designed to support an agile approach
to database design and make it easier to keep development and production
databases in sync as schema changes are required.  It allows you to manage 
atabase change sets and database repository versioning.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .env

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
%{__mv} %{buildroot}%{_bindir}/migrate %{buildroot}%{_bindir}/sqlalchemy-migrate

%clean
%{__rm} -rf %{buildroot}

# Check needs py.test in order to run
#%check
#echo 'sqlite:///__tmp__' > test_db.cfg
# setuptools doesn't appear to be compatible with py.test
# %{__python} setup.py test
#%{__python} -c 'from py.test.cmdline import main; main(["test"])'

%files
%defattr(-,root,root,-)
%doc README CHANGELOG docs/
%{_bindir}/sqlalchemy-migrate
%{python_sitelib}/*

%changelog
* Tue Jul 15 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-3
- Rename binary to sqlalchemy-migrate to avoid potential filename clashes.
  (Queried upstream but the change is only in Fedora).  Noted that
  openmosix defintely has a /usr/bin/migrate already.

* Sat Jul 06 2008 Ricky Zhou <ricky@fedoraproject.org> 0.4.4-2
- Add BuildRequires on python-setuptools-devel.
- Add Requires on SQLAlchemy.

* Sat Jun 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-1
- Initial Fedora Build.
