Name:       gitea
# renovate: datasource=github-releases depName=go-gitea/gitea
Version:    1.13.1
Release:    itix1
Summary:    Git with a cup of tea, painless self-hosted git service
License:    MIT
Source0:    https://github.com/go-gitea/%{name}/releases/download/v%{version}/%{name}-%{version}-linux-amd64.xz
ExclusiveArch: x86_64
Source1:    gitea.service
Requires(pre): shadow-utils
Requires: postgresql-server
BuildRequires: systemd

%description

The goal of this project is to make the easiest, fastest, and most painless
way of setting up a self-hosted Git service. Using Go, this can be done with
an independent binary distribution across all platforms which Go supports,
including Linux, macOS, and Windows on x86, amd64, ARM and PowerPC
architectures.

# Since we don't recompile from source, disable the build_id checking
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global debug_package %{nil}

%prep
%setup -q -c -T
xz -dc %{S:0} > gitea
cp %{S:1} %{name}.service

%build

%install
install -d %{buildroot}/opt/%{name}/etc/
install -d %{buildroot}/srv/%{name}/custom
install -d %{buildroot}/srv/%{name}/git
install -D gitea %{buildroot}/opt/%{name}/bin/gitea
install -D -m 0644 %{name}.service %{buildroot}/%{_unitdir}/%{name}.service

%files
%defattr(0644, root, root, 0755)
%dir /opt/%{name}/bin
%dir /opt/%{name}/etc
%dir /srv/%{name}
%dir /srv/%{name}/custom
%dir /srv/%{name}/git
%attr(0755, root, root) /opt/%{name}/bin/gitea
%{_unitdir}/%{name}.service

%pre
getent group itix-svc >/dev/null || groupadd -r itix-svc
getent passwd git >/dev/null || useradd -r -g itix-svc \
  -d /srv/%{name} -s /sbin/nologin -c "Git with a cup of tea" \
  git

exit 0

%changelog
* Mon Feb 22 2021 Nicolas MASSE <nicolas.masse@itix.fr> - 1.13.1-itix1
- First release
