%define debug_package %{nil}

Summary:	A Linux clone of the old DOS game WarLords
Name:		freelords
Version:	0.0.4
Release:	3
License:	GPLv2+
Group:		Games/Strategy
Url:		https://sourceforge.net/p/freelords/wiki/Home
Source0:	https://sourceforge.net/projects/freelords/files/Java%20Freelords/%{version}/freelords-%{version}_src.zip
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	ant
BuildRequires:	xalan-j2
BuildRequires:	xerces-j2
BuildRequires:	xml-commons-jaxp-1.3-apis
Requires:	java
BuildArch:	noarch

%description
FreeLords is a turn-based strategy game similar to Warlords.
It can be played with friends on one computer or via a network.

%files
%{_gamesbindir}/*
%{_datadir}/games/%{name}
%{_datadir}/applications/%{name}.desktop

#----------------------------------------------------------------------------

%prep
%setup -qc

%build
ant build

%install
ant deploy

# No need to support M$ crap
rm -f deploy/*.bat

mkdir -p %{buildroot}%{_datadir}/games/%{name}
cp -a deploy/* %{buildroot}%{_datadir}/games/%{name}

mkdir -p %{buildroot}%{_gamesbindir}
for i in client server; do
	cat >%{buildroot}%{_gamesbindir}/%{name}-$i <<EOF
#!/bin/sh
cd %{_datadir}/games/%{name}
exec ./$i.sh "$@"
EOF
done
chmod 0755 %{buildroot}%{_gamesbindir}/*

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=FreeLords
Name[ru]=FreeLords
Comment=A Linux clone of the old DOS game WarLords
Comment[ru]=Клон игры WarLords
Exec=%{_gamesbindir}/%{name}-client
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;StrategyGame;
EOF
