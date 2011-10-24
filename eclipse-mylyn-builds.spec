%global eclipse_base        %{_libdir}/eclipse
%global install_loc         %{_datadir}/eclipse/dropins
# Taken from update site so we match upstream
#  http://download.eclipse.org/mylyn/archive/3.5.1/v20110422-0200/
%global qualifier           v20110422-0200

Name: eclipse-mylyn-builds
Summary: Eclipse Mylyn Builds
Version: 3.5.1
Group:	Development/Java
Release: 2
License: EPL
URL: http://www.eclipse.org/mylyn/builds/

# bash fetch-eclipse-mylyn-builds.sh
Source0: eclipse-mylyn-builds-R_3_5_1-fetched-src.tar.bz2
Source1: fetch-eclipse-mylyn-builds.sh

# This patches hudson related plug-ins so as to
# - use non-glassfish specific JAXBContextBuilder class
# - use java 6 exec environment
# - remove ecf-based auto-discovery
# See also, Eclipse Bz: 325176.
Patch0: remove-auto-discovery-o.e.m.hudson.ui-remove-glassfish-specific-impl-jaxb.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.6.0
BuildRequires: eclipse-platform >= 0:3.4.0
BuildRequires: eclipse-pde >= 0:3.4.0
BuildRequires: eclipse-mylyn-commons >= 3.5.0
BuildRequires: eclipse-mylyn >= 3.5.0
BuildRequires: eclipse-mylyn-context-team >= 3.5.0
BuildRequires: eclipse-mylyn-versions >= 3.5.0
BuildRequires: eclipse-emf
# Required for RestfulHudsonClient.java. However, this will only
# work with java 1.6 and up, but that's better than not working at all.
BuildRequires: ws-jaxme
# The following is required for javax.xml.stream (apparently openjdk ships it too)
# not sure what's best here.
BuildRequires: xml-commons-apis
Requires: eclipse-mylyn >= 3.5.0
Requires: eclipse-mylyn-commons >= 3.5.0
Requires: eclipse-mylyn-context-team >= 3.5.0
Requires: eclipse-emf
Requires: eclipse-mylyn-versions >= 3.5.0
Requires: xml-commons-apis


%description
Provides a common framework to interact with continuous integration
build providers using Eclipse Mylyn.


# eclipse-mylyn-builds-hudson

%package hudson
Summary: Mylyn Builds Connector: Hudson/Jenkins
Requires: java >= 0:1.6.0
Requires: eclipse-platform >= 0:3.4.0
Requires: eclipse-mylyn-commons >= 3.5.0
Requires: ws-jaxme
Requires: %{name} = %{version}-%{release}
Group: Development/Java

%description hudson
Support for the open source Hudson and Jenkins continuous integration servers.


%prep
%setup -q -n org.eclipse.mylyn.builds
%patch0 -p1


%build
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.builds \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -d "mylyn mylyn-commons mylyn-context-team emf mylyn-versions"
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.hudson \
 -a "-DjavacSource=1.6 -DjavacTarget=1.6 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJavaSE-1.6=%{_jvmdir}/java/jre/lib/rt.jar \
 -d "mylyn-commons"


%install
install -d -m 755 %{buildroot}%{_datadir}/eclipse
install -d -m 755 %{buildroot}%{install_loc}/mylyn-builds
install -d -m 755 %{buildroot}%{install_loc}/mylyn-builds-hudson

unzip -q -o -d %{buildroot}%{install_loc}/mylyn-builds \
 build/rpmBuild/org.eclipse.mylyn.builds.zip
unzip -q -o -d %{buildroot}%{install_loc}/mylyn-builds-hudson \
 build/rpmBuild/org.eclipse.mylyn.hudson.zip


# eclipse-mylyn-builds

%files
%defattr(-,root,root,-)
%{install_loc}/mylyn-builds
%doc org.eclipse.mylyn.builds-feature/epl-v10.html
%doc org.eclipse.mylyn.builds-feature/license.html


# eclipse-mylyn-builds-hudson

%files hudson
%defattr(-,root,root,-)
%{install_loc}/mylyn-builds-hudson
%doc org.eclipse.mylyn.hudson-feature/epl-v10.html
%doc org.eclipse.mylyn.hudson-feature/license.html


