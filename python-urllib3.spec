# TODO: use system six, [backports.]ssl_match_hostname
#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# test target (uses network etc., few failures)

%define		module		urllib3
Summary:	HTTP library with thread-safe connection pooling, file post, and more
Summary(pl.UTF-8):	Biblioteka HTTP z bezpieczną wątkowo pulą połączeń, wysyłaniem plików itd.
Name:		python-%{module}
Version:	1.25.9
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/urllib3/
Source0:	https://files.pythonhosted.org/packages/source/u/urllib3/%{module}-%{version}.tar.gz
# Source0-md5:	dbf9b868b90880b24b1ac278094e912e
Patch0:		%{name}-mock.patch
Patch1:		%{name}-httplib.patch
URL:		http://urllib3.readthedocs.org/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%if %{with tests}
BuildRequires:	python-PySocks >= 1.5.6
BuildRequires:	python-PySocks < 2.0
BuildRequires:	python-cryptography >= 2.8
# TODO
#BuildRequires:	python-gcp_devrel-py-tools >= 0.0.15
BuildRequires:	python-mock >= 3.0.5
BuildRequires:	python-pytest
BuildRequires:	python-tornado >= 5.1.1
BuildRequires:	python-trustme >= 0.5.3
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.5.6
BuildRequires:	python3-PySocks < 2.0
BuildRequires:	python3-cryptography >= 2.8
#BuildRequires:	python3-gcp_devrel-py-tools >= 0.0.15
BuildRequires:	python3-pytest
BuildRequires:	python3-tornado >= 6.0.3
BuildRequires:	python3-trustme >= 0.5.3
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 HTTP module with connection pooling and file POST abilities.
Features are:
- Re-use the same socket connection for multiple requests (with
  optional client-side certificate verification).
- File posting (encode_multipart_formdata).
- Built-in redirection and retries (optional).
- Supports gzip and deflate decoding.
- Thread-safe and sanity-safe.

%description -l pl.UTF-8
Moduł HTTP dla Pythona 2 z pulą połączeń i możliwością wysyłania
plików metodą POST. Możliwości:
- używanie tego samego połączenia dla wielu żądań (z opcjonalną
  weryfikacją certyfikatu po stronie klienta)
- wysyłanie plików (encode_multipart_formdata)
- wbudowane przekierowania i ponawianie prób (opcjonalne)
- obsługa kodowań gzip i deflate
- bezpieczeństwo względem wątków.

%package -n python3-urllib3
Summary:	HTTP library with thread-safe connection pooling, file post, and more
Summary(pl.UTF-8):	Biblioteka HTTP z bezpieczną wątkowo pulą połączeń, wysyłaniem plików itd.
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-urllib3
Python 3 HTTP module with connection pooling and file POST abilities.
Features are:
- Re-use the same socket connection for multiple requests (with
  optional client-side certificate verification).
- File posting (encode_multipart_formdata).
- Built-in redirection and retries (optional).
- Supports gzip and deflate decoding.
- Thread-safe and sanity-safe.

%description -n python3-urllib3 -l pl.UTF-8
Moduł HTTP dla Pythona 3 z pulą połączeń i możliwością wysyłania
plików metodą POST. Możliwości:
- używanie tego samego połączenia dla wielu żądań (z opcjonalną
  weryfikacją certyfikatu po stronie klienta)
- wysyłanie plików (encode_multipart_formdata)
- wbudowane przekierowania i ponawianie prób (opcjonalne)
- obsługa kodowań gzip i deflate
- bezpieczeństwo względem wątków.

%package apidocs
Summary:	API documentation for Python urllib3 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona urllib3
Group:		Documentation

%description apidocs
API documentation for Python urllib3 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona urllib3.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests_py2}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest test
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3 \
	SPHINXOPTS=
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-urllib3
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,reference,*.html,*.js}
%endif
