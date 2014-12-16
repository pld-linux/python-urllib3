#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
#
%define 	module	urllib3
Summary:	HTTP library with thread-safe connection pooling, file post, and more
Summary(pl.UTF-8):	Biblioteka HTTP z bezpieczną wątkowo pulą połączeń, wysyłaniem plików itd.
Name:		python-%{module}
Version:	1.10
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/u/urllib3/%{module}-%{version}.tar.gz
# Source0-md5:	9badc8f09ea2d3c36cbb5071bfe52ebd
URL:		http://urllib3.readthedocs.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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
Requires:	python3-modules >= 1:3.2

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

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%{__python} setup.py build -b py2
%endif

%if %{with python3}
%{__python3} setup.py build -b py3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build -b py2 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build -b py3 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

# dummyserver is a part of unitstests
%{__rm} -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/dummyserver \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/dummyserver

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-urllib3
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
