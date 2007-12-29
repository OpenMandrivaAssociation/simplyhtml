%define gcj_support 1
%define section free

Name:           simplyhtml
Version:        0.12.2
Release:        %mkrel 0.0.3
Epoch:          0
Summary:        Application and a java component for rich text processing
License:        GPL
Group:          Development/Java
URL:            http://simplyhtml.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/simplyhtml/shtml_0_12_2_beta1.zip
Requires:       gnu-regexp
Requires:       javahelp2
BuildRequires:  ant
BuildRequires:  gnu-regexp
BuildRequires:  javahelp2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
SimplyHTML is an application and a java component for rich text
processing. It stores documents as HTML files in combination with
Cascading Style Sheets (CSS). SimplyHTML is not intended to be used
as an editor for web pages.

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java

%description javadoc
Javadoc documentation for %{name}.

%prep
%setup -q -n dist
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

%{_bindir}/find . -type f -name '*.htm' | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%{__perl} -pi -e 's/^Class-Path:.*\n//;' \
              -e 's/^Created-By:.*\n//;' \
  src/MANIFEST.MF

cd lib
%{__ln_s} $(build-classpath gnu-regexp) gnu-regexp-1.1.4.jar
%{__ln_s} $(build-classpath javahelp2) jhall.jar
cd ..

%build
export CLASSPATH=
export OPT_JAR_LIST=:
cd src
%{ant}
cd ..

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}

%{__cp} -a dist/lib/SimplyHTML.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/SimplyHTML-%{version}.jar
%{__ln_s} SimplyHTML-%{version}.jar %{buildroot}%{_javadir}/SimplyHTML.jar

%{__cp} -a dist/lib/SimplyHTMLHelp.jar %{buildroot}%{_javadir}/%{name}-help-%{version}.jar
%{__ln_s} %{name}-help-%{version}.jar %{buildroot}%{_javadir}/%{name}-help.jar
%{__ln_s} %{name}-help-%{version}.jar %{buildroot}%{_javadir}/SimplyHTMLHelp-%{version}.jar
%{__ln_s} SimplyHTMLHelp-%{version}.jar %{buildroot}%{_javadir}/SimplyHTMLHelp.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc doc/*
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
