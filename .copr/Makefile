srpm:
	@test -n "$(spec)" || (echo "error: 'spec' variable is empty" >&2; exit 1)
	@test -n "$(outdir)" || (echo "error: 'outdir' variable is empty" >&2; exit 1)
	@command -v spectool >/dev/null 2>&1 || dnf install -y rpmdevtools
	@rpm --showrc 2>/dev/null | grep -q '_userunitdir' || dnf install -y systemd-rpm-macros
	@mkdir -p "$(outdir)"
	@set -e; \
	tmpd=$$(mktemp -d); mkdir -p "$$tmpd/SOURCES" "$$tmpd/SRPMS" "$$tmpd/BUILD"; \
	spectool -g --directory "$$tmpd/SOURCES" "$(spec)"; \
	rpmbuild -bs --define "_topdir $$tmpd" --define "_sourcedir $$tmpd/SOURCES" --define "_srcrpmdir $(outdir)" "$(spec)"; \
	rm -rf "$$tmpd"

.PHONY: srpm
