%global srcname sqlalchemy-migrate
%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

Name: python-migrate
Version: 0.11.0
Release: 5%{?dist}
Summary: Schema migration tools for SQLAlchemy

License: MIT
URL: https://github.com/openstack/%{srcname}
Source0: https://pypi.io/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
# Local patch to rename /usr/bin/migrate to sqlalchemy-migrate
Patch100: python-migrate-sqlalchemy-migrate.patch

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-sqlalchemy >= 0.7.8
BuildRequires: python-setuptools
BuildRequires: python-nose
BuildRequires: python-sphinx
BuildRequires: python-decorator
BuildRequires: python-tempita >= 0.4
BuildRequires: python-pbr >= 1.3.0
BuildRequires: python-six >= 1.9.0
BuildRequires: python-sqlparse

# for testsuite
BuildRequires: python-scripttest
BuildRequires: python-testtools

%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires: python-unittest2
%endif

%global _description\
Schema migration tools for SQLAlchemy designed to support an agile approach\
to database design and make it easier to keep development and production\
databases in sync as schema changes are required.  It allows you to manage\
database change sets and database repository versioning.

%description %_description

%package -n python2-migrate
Summary: %summary
Requires: python-sqlalchemy >= 0.7.8
Requires: python-setuptools
Requires: python-decorator
Requires: python-tempita >= 0.4
Requires: python-pbr >= 1.3.0
Requires: python-six >= 1.9.0
Requires: python-sqlparse
%{?python_provide:%python_provide python2-migrate}

%description -n python2-migrate %_description

%if 0%{?with_python3}
%package -n     python3-migrate
Summary: Schema migration tools for SQLAlchemy

BuildRequires: python3-devel
BuildRequires: python3-sqlalchemy >= 0.7.8
BuildRequires: python3-setuptools
BuildRequires: python3-nose
BuildRequires: python3-sphinx
BuildRequires: python3-decorator
BuildRequires: python3-tempita >= 0.4
BuildRequires: python3-pbr >= 1.3.0
BuildRequires: python3-six >= 1.9.0
BuildRequires: python3-sqlparse

%description -n python3-migrate
Schema migration tools for SQLAlchemy designed to support an agile approach
to database design and make it easier to keep development and production
databases in sync as schema changes are required.  It allows you to manage
database change sets and database repository versioning.
%endif

%prep
%setup -q -n %{srcname}-%{version}
%patch100 -p1 -b .rename

# use real unittest in python 2.7 and up
%if 0%{?fedora} || 0%{?rhel} > 6
sed -i "s/import unittest2/import unittest as unittest2/g" \
    migrate/tests/fixture/__init__.py \
    migrate/tests/fixture/base.py
%endif

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
for bin in sqlalchemy-migrate{,-repository}; do
  mv %{buildroot}/%{_bindir}/$bin %{buildroot}/%{_bindir}/python3-$bin
done
%endif
%py2_install

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
for bin in sqlalchemy-migrate{,-repository}; do
    ln -s $bin $bin-2
    ln -s $bin $bin-%{python2_shortver}
done

%if 0%{?with_python3}
for bin in sqlalchemy-migrate{,-repository}; do
    ln -s python3-$bin $bin-3
    ln -s python3-$bin $bin-%{python3_shortver}
done
%endif
popd 

%check
# Need to set PATH for two reasons:
# 1) Path isn't being cleared by mock so we have /root/bin/ in the PATH
# 2) Need to be able to find the newly installed migrate binaries
PATH=/bin:/usr/bin:%{buildroot}%{_bindir}
export PATH

PYTHONPATH=`pwd`
export PYTHONPATH
echo 'sqlite:///__tmp__' > test_db.cfg

# Disable temporarily until tests are adjusted to support testtools >= 0.9.36
#nosetests

%files -n python2-migrate
%doc README.rst doc/
%{_bindir}/sqlalchemy-migrate
%{_bindir}/sqlalchemy-migrate-repository
%{_bindir}/sqlalchemy-migrate-2*
%{_bindir}/sqlalchemy-migrate-repository-2*
%{python2_sitelib}/*
 
%if 0%{?with_python3}
%files -n python3-migrate
%doc README.rst doc/
%{_bindir}/python3-sqlalchemy-migrate
%{_bindir}/python3-sqlalchemy-migrate-repository
%{_bindir}/sqlalchemy-migrate-3*
%{_bindir}/sqlalchemy-migrate-repository-3*
%{python3_sitelib}/*
%endif

%changelog
* Fri Feb 09 2018 Neal Gompa <ngompa@datto.com> - 0.11.0-5
- Add missing pbr dependency for Python 2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11.0-3
- Python 2 binary package renamed to python2-migrate
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr  7 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 0.11.0-1
- Upstream 0.11.0 (required due to pbr bump)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.10.0-1
- Upstream 0.10.0
- Add python3 subpackage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 01 2015 Pádraig Brady <pbrady@redhat.com> - 0.9.6.1
- Latest upstream

* Tue Mar 31 2015 Pádraig Brady <pbrady@redhat.com> - 0.9.5-1
- Latest upstream

* Tue Feb 10 2015 Pádraig Brady <pbrady@redhat.com> - 0.9.4-1
- Latest upstream

* Wed Nov 19 2014 Pádraig Brady <pbrady@redhat.com> - 0.9.2-2
- build: remove cap on testtools for the moment

* Thu Sep 18 2014 Pádraig Brady <pbrady@redhat.com> - 0.9.2-1
- Latest upstream

* Fri Jun 13 2014 Pádraig Brady <pbrady@redhat.com> - 0.9.1-1
- Latest upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 08 2014 Pádraig Brady <pbrady@redhat.com> - 0.9-1
- Latest upstream

* Tue Mar 04 2014 Pádraig Brady <pbrady@redhat.com> - 0.8.5.1
- Latest upstream

* Mon Dec 16 2013 Pádraig Brady <pbrady@redhat.com> - 0.8.2-1
- Latest upstream

* Mon Sep 23 2013 Pádraig Brady <pbrady@redhat.com> - 0.7.2-9
- improve sqlalchemy 0.8 compatibility

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Pádraig Brady <P@draigBrady.com> - 0.7.2-7
- Add compatability for sqlalchemy >= 0.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Pádraig Brady <P@draigBrady.com> - 0.7.2-5
- Fix build on RHEL 7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-2
- Require python-tempita

* Tue Nov 08 2011 Martin Bacovsky <mbacovsk@redhat.com> - 0.7.2-1
- Updated to new version

* Sat Jun 25 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7-1
- Update to new version compatible with SQLAlchemy 0.7.x.

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

* Sun Jul 06 2008 Ricky Zhou <ricky@fedoraproject.org> 0.4.4-2
- Add BuildRequires on python-setuptools-devel.
- Add Requires on SQLAlchemy.

* Sat Jun 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.4-1
- Initial Fedora Build.
