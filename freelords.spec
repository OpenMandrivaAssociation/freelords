%define debug_package %nil

Summary:	A Linux clone of the old DOS game WarLords
Name:		freelords
Version:	0.0.3
Release:	2
License:	GPLv2+
Group:		Games/Strategy
Source0:	http://switch.dl.sourceforge.net/project/freelords/Java%20Freelords/%version/freelords-%{version}_src.tar.gz2
URL:		http://sourceforge.net/projects/freelords/
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	ant
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	xalan-j2 xerces-j2
BuildArch:	noarch

%description
FreeLords is a turn-based strategy game similar to Warlords. 
It can be played with friends on one computer or via a network.

%prep
%setup -q

%build 
ant build

%install
ant deploy

# No need to support M$ crap
rm -f deploy/*.bat

mkdir -p %buildroot%_datadir/games/%name
cp -a deploy/* %buildroot%_datadir/games/%name

mkdir -p %buildroot%_bindir
for i in client server; do
	cat >%buildroot%_bindir/%name-$i <<EOF
#!/bin/sh
cd %_datadir/games/%name
exec $i.sh "$@"
EOF
done
chmod 0755 %buildroot%_bindir/*

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=FreeLords
Comment=A Linux clone of the old DOS game WarLords
Exec=%_bindir/%name-client
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;StrategyGame;
EOF

%files
%defattr(-,root,root)
%_bindir/*
%_datadir/games/%name
%_datadir/applications/*
