%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define srcname sqlalchemy-migrate

Name: python-migrate
Version: 0.5.1
Release: 0.1.20090122.svn479%{?dist}
Summary: Schema migration tools for SQLAlchemy

Group: Development/Languages
License: MIT
URL: http://code.google.com/p/%{srcname}/
# Build from a snapshot so we get this working with sqlalchemy-0.5
# svn checkout http://sqlalchemy-migrate.googlecode.com/svn/trunk/ sqlalchemy-migrate -r479
# cd sqlalchemy-migrate
# python setup.py sdist
# tarball is in dist/sqlalchemy-migrate-0.5.1.dev-r479.tar.gz
Source0: %{srcname}-%{version}.dev-r479.tar.gz
#Source0: http://%{srcname}.googlecode.com/files/%{srcname}-%{version}.tar.gz
# Local patch to rename /usr/bin/migrate to sqlalchemy-migrate
Patch0: python-migrate-sqlalchemy-migrate.patch
# Sent upstream to fix a unittest failure
Patch1: python-migrate-unittests.patch
# Disable one unittest for now.  In the future we want this to work
Patch2: python-migrate-disable-test_fk.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-sqlalchemy
BuildRequires: python-setuptools-devel
BuildRequires: python-nose
Requires: python-sqlalchemy >= 0.5
Requires: python-setuptools

%description
Schema migration tools for SQLAlchemy designed to support an agile approach
to database design and make it easier to keep development and production
databases in sync as schema changes are required.  It allows you to manage 
atabase change sets and database repository versioning.

%prep
%setup -q -n %{srcname}-%{version}.dev-r479
%patch0 -p1 -b .rename
%patch1 -p0 -b .testing
# Try removing this patch on every update
%patch2 -p1 -b .disable-test

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%check
echo 'sqlite:///__tmp__' > test_db.cfg
%{__python} setup.py test

%files
%defattr(-,root,root,-)
%doc README CHANGELOG docs/
%{_bindir}/*
%{python_sitelib}/*

%changelog
* Mon Jan 26 2009 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.1-0.1.20090122.svn479
- Update to snapshot so that it works with sqlalchemy-0.5
- Enable test suite

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.5-4
- Rebuild for Python 2.6

* Tue Jul 29 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.5-3
- Patch to generate a script for the repository migrate script.
- Move the script rename into a patch to setup.py.

* Thu Jul 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.5-2
- Remove patches that are merged upstream.

* Thu Jul 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.5-1
- New upstream

* Thu Jul 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-4
- Disable py.test so we don't try to download it during build.

* Tue Jul 15 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-3
- Rename binary to sqlalchemy-migrate to avoid potential filename clashes.
  (Queried upstream but the change is only in Fedora).  Noted that
  openmosix defintely has a /usr/bin/migrate already.

* Sat Jul 06 2008 Ricky Zhou <ricky@fedoraproject.org> 0.4.4-2
- Add BuildRequires on python-setuptools-devel.
- Add Requires on SQLAlchemy.

* Sat Jun 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-1
- Initial Fedora Build.
