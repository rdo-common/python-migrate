%if !(0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global srcname sqlalchemy-migrate

Name: python-migrate
Version: 0.6
Release: 4%{?dist}
Summary: Schema migration tools for SQLAlchemy

Group: Development/Languages
License: MIT
URL: http://code.google.com/p/%{srcname}/
Source0: http://%{srcname}.googlecode.com/files/%{srcname}-%{version}.tar.gz
# Patch to update to new scripttest API submitted upstream
Patch0: migrate-scripttest-update.patch
# Patch to fix a unittest on python-2.7
Patch1: migrate-py27.patch
# Local patch to rename /usr/bin/migrate to sqlalchemy-migrate
Patch100: python-migrate-sqlalchemy-migrate.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-sqlalchemy
BuildRequires: python-setuptools-devel
BuildRequires: python-nose
BuildRequires: python-sphinx
BuildRequires: python-decorator

# for testsuite
BuildRequires: python-scripttest
BuildRequires: python-tempita

Requires: python-sqlalchemy
Requires: python-setuptools
Requires: python-decorator

%if 0%{?rhel} && 0%{?rhel} < 6
BuildRequires: python-sqlite2
Requires:      python-sqlite2
%endif


%description
Schema migration tools for SQLAlchemy designed to support an agile approach
to database design and make it easier to keep development and production
databases in sync as schema changes are required.  It allows you to manage 
atabase change sets and database repository versioning.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .test
%patch1 -p1 -b .py27
%patch100 -p0 -b .rename

# use real unittest in python 2.7 and up
sed -i "s/import unittest2/import unittest as unittest2/g" \
    migrate/tests/fixture/__init__.py \
    migrate/tests/fixture/base.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%check
# Need to set PATH for two reasons:
# 1) Path isn't being cleared by mock so we have /root/bin/ in the PATH
# 2) Need to be able to find the newly installed migrate binaries
PATH=/bin:/usr/bin:%{buildroot}%{_bindir}
export PATH

PYTHONPATH=`pwd`
export PYTHONPATH
echo 'sqlite:///__tmp__' > test_db.cfg
nosetests

%files
%defattr(-,root,root,-)
%doc README TODO docs/
%{_bindir}/*
%{python_sitelib}/*

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-3
- Fix SQLAlchemy Requires -- need >= 0.5, not 0.6
* Sun Aug 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-2
- Update to unittests to work with newer scripttest API

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6-1
- update to new version
- testsuite doesn't work right now

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Martin Bacovsky <mbacovsk@redhat.com> - 0.5.4-1
- Update to new bugfix release 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> 0.5.3-2
- Add python-migrate-py2.4-import.patch, which makes the use
  of __import__ work on Python 2.4
- Add python-sqlite2 to the build requirements on FC6 and below

* Thu Apr 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.3-1
- Update to new bugfix release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.1.2-2
- Add BR on python-sphinx

* Wed Feb 11 2009 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.1.2-1
- Update to 0.5.1.2 release with official support for SA-0.5
- Remove patches merged upstream

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
