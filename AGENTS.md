# AGENTS.md

# Project Development Rules & AI Agent Instructions

## 1. Core Principles

You are an AI development agent working on this project.

You MUST follow these rules at all times. These rules take priority over your own preferences, assumptions, shortcuts, and implementation choices.

The project follows four fundamental principles:

1. **Fedora Standards First** — All RPM packages and SPEC files MUST strictly follow official Fedora packaging standards.
2. **Upstream First, Approval Required** — Before making ANY modification, you MUST investigate and verify the relevant upstream source, explain your findings, and obtain explicit approval from the project owner.
3. **No Automatic Build Verification** — After modifications, package building, RPM building, testing, and validation MUST NOT be performed unless explicitly requested by the project owner.
4. **AGENTS.md Protection** — This file is protected. You MUST NEVER modify, overwrite, delete, rename, move, or replace this file unless explicitly instructed by the project owner.

Never assume that a technically valid solution is automatically an acceptable solution.

The project owner has final authority over all implementation decisions.

---

## 2. AGENTS.md Protection Policy

**AGENTS.md is a protected file.**

You MUST NOT modify this file without explicit authorization from the project owner.

This restriction includes:

- Changing existing instructions.
- Adding new instructions.
- Removing existing instructions.
- Reorganizing or rewriting sections.
- Modifying formatting or Markdown structure.
- Automatically updating instructions.
- Applying suggestions that modify this file.
- Modifying this file as part of automated cleanup or refactoring.
- Replacing the file with another version.
- Deleting or renaming the file.

Even if you believe an instruction is incorrect, outdated, contradictory, or could be improved, you MUST NOT modify AGENTS.md independently.

### 2.1 When Changes Are Necessary

If changes to AGENTS.md appear necessary:

1. Explain why the change is necessary.
2. Describe the exact proposed changes.
3. Identify the affected sections.
4. Present the proposed content.
5. Wait for explicit authorization from the project owner.

Only an explicit request from the project owner to modify AGENTS.md grants permission to do so.

General approval to modify the project does NOT authorize modifications to AGENTS.md.

**This protection rule takes precedence over all other project instructions, automated workflows, and agent preferences.**

Without explicit authorization, AGENTS.md MUST remain untouched.

---

## 3. Fedora RPM Packaging Standards

### 3.1 Mandatory Fedora Compliance

All RPM packaging MUST follow the official Fedora Packaging Guidelines.

Official references:

- Fedora Packaging Guidelines: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- Fedora Packaging Review Guidelines: https://fedoraproject.org/wiki/Packaging:ReviewGuidelines
- Fedora Naming Guidelines: https://fedoraproject.org/wiki/Packaging:NamingGuidelines
- Fedora Licensing Guidelines: https://fedoraproject.org/wiki/Packaging:LicensingGuidelines
- Fedora RPM SPEC Style Guide: https://fedoraproject.org/wiki/SpecStyleGuide
- Fedora RPM Macros: https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/

The official Fedora documentation is the primary authority.

If different sources conflict, follow the current official Fedora guidelines.

Do not rely on outdated documentation when newer official guidelines are available.

Always consider the target Fedora release when determining applicable packaging requirements.

### 3.2 SPEC File Requirements

Every SPEC file MUST follow Fedora conventions.

Mandatory requirements:

- Use standard Fedora RPM SPEC syntax.
- Use Fedora-supported RPM macros.
- Follow Fedora package naming conventions.
- Use correct `Name`, `Version`, `Release`, `Summary`, `License`, and `URL` fields.
- Use appropriate `Source` and `Patch` declarations.
- Declare all necessary build dependencies using `BuildRequires`.
- Declare runtime dependencies using appropriate dependency tags.
- Follow Fedora conventions for `%prep`, `%build`, `%install`, `%check`, and `%files`.
- Use appropriate Fedora macros instead of unnecessary hardcoded filesystem paths.
- Use `%license` for upstream-provided license files.
- Use `%doc` for appropriate documentation.
- Follow Fedora conventions for subpackages and dependency relationships.
- Follow Fedora scriptlet and file ownership requirements.
- Preserve upstream source integrity.
- Ensure the SPEC file is readable, maintainable, and understandable.

Follow the applicable Fedora guidelines for the target Fedora release.

### 3.3 Forbidden Packaging Practices

Unless explicitly permitted by Fedora guidelines, DO NOT:

- Copy Debian packaging instructions into RPM SPEC files.
- Use Arch Linux PKGBUILD conventions.
- Use openSUSE-specific RPM macros that are unavailable in Fedora.
- Introduce distribution-specific macros from other distributions.
- Hardcode paths when appropriate Fedora RPM macros exist.
- Invent dependencies without verifying their actual requirements.
- Guess license identifiers.
- Blindly copy SPEC files from COPR, third-party repositories, or other distributions.
- Introduce unnecessary scriptlets.
- Add unnecessary patches to work around problems without investigating upstream.
- Add unnecessary dependencies merely to simplify packaging.
- Ignore Fedora package review requirements.

A SPEC file that successfully builds is NOT necessarily Fedora-compliant.

Correctness and Fedora compliance are both mandatory.

### 3.4 SPEC File Research Requirements

Before proposing a new SPEC file or modifying an existing one, investigate:

1. Upstream source and release version.
2. Actual project license and license files.
3. Build system and build dependencies.
4. Runtime dependencies.
5. Installation paths.
6. Binary, library, configuration, and documentation locations.
7. Required patches and their upstream status.
8. Fedora packaging guidelines applicable to the package.
9. Architecture support.
10. RPM macros and scriptlet requirements.

Do not assume dependencies, installation paths, or build procedures.

Base packaging decisions on actual upstream source and official Fedora documentation.

### 3.5 Packaging Tool Policy

The following tools may be relevant when the owner explicitly requests packaging verification:

- `rpmlint`
- `rpmbuild`
- `mock`
- `rpmdevtools`

Their execution is NOT automatic.

See Section 8 for build and verification restrictions.

---

## 4. Upstream Verification Is Mandatory

### 4.1 Verify Before Every Modification

Before modifying ANY project file, you MUST investigate the relevant upstream project.

This applies to:

- RPM SPEC files.
- Build scripts.
- Installation scripts.
- Configuration files.
- Systemd services and overrides.
- Patches.
- Package dependencies.
- Build configurations.
- Kernel and system configurations.
- Desktop environment configurations.
- CI/CD workflows.
- Repository metadata.
- Documentation describing implementation behavior.

You MUST NOT skip upstream verification because:

- The modification looks trivial.
- The solution seems obvious.
- You have seen a similar implementation elsewhere.
- You already know how the software works.
- The requested change appears to be a simple bug fix.
- The modification only involves one or two lines.

### 4.2 Upstream Investigation Priority

Use the following investigation order:

1. Official upstream GitHub/GitLab repository.
2. Official upstream documentation.
3. Upstream source code.
4. Upstream release notes and changelogs.
5. Upstream issues and discussions.
6. Upstream pull requests and commits.
7. Official Fedora documentation, when RPM packaging is involved.

Third-party implementations may be used as supplementary references, but MUST NOT replace upstream verification.

### 4.3 What Must Be Verified

Before proposing a modification, establish:

- What the current upstream implementation actually does.
- Whether the proposed feature or fix already exists upstream.
- Whether the issue is already fixed in a newer release.
- Whether there is an upstream issue or pull request discussing it.
- Whether the proposed solution follows upstream recommendations.
- Whether the proposed change introduces compatibility or maintenance problems.
- Whether a downstream modification is actually necessary.

If upstream information cannot be verified, explicitly report that limitation.

DO NOT fabricate upstream behavior, issue numbers, commits, or recommendations.

### 4.4 No Unverified Implementation

Never propose an implementation as an established fact when it is only a hypothesis.

Clearly distinguish between:

- Verified upstream behavior.
- Official documentation requirements.
- Existing project implementation.
- Technical inference.
- Unverified hypotheses.
- Proposed modifications.

If evidence is insufficient, investigate further or explain what remains unknown.

---

## 5. Strict Approval Gate — No Changes Without Permission

This is a mandatory authorization policy.

**You MUST NOT modify any project file without explicit approval from the project owner.**

### 5.1 Actions That Require Approval

The following actions are prohibited until approval:

- Creating files.
- Editing existing files.
- Deleting files.
- Renaming or moving files.
- Modifying SPEC files.
- Adding, removing, or changing patches.
- Changing package dependencies.
- Modifying build scripts.
- Changing system configurations.
- Modifying systemd units or overrides.
- Changing repository configurations.
- Running automated formatters that modify files.
- Applying patches.
- Committing changes.
- Pushing changes.
- Executing scripts that modify the project or system.

Do not interpret a request to investigate, analyze, explain, or diagnose as permission to modify files.

**Exception:** AGENTS.md has its own stricter protection policy in Section 2. General project approval does not authorize modifying it.

### 5.2 Required Workflow

Every modification MUST follow this sequence.

#### Phase 1 — Investigation

- Inspect the existing project files.
- Identify the affected components.
- Investigate upstream behavior.
- Verify official documentation.
- Identify the actual problem.
- Determine whether a modification is necessary.

No project modifications are allowed.

#### Phase 2 — Report Findings

Present your findings to the project owner.

The report MUST include:

1. Problem description.
2. Current implementation.
3. Upstream implementation or official recommendation.
4. Evidence and source links.
5. Root cause.
6. Proposed solution.
7. Exact files that would be modified.
8. Expected changes.
9. Potential side effects and risks.
10. Implementation approach.

If multiple solutions exist, explain their differences and recommend one.

#### Phase 3 — Wait for Approval

Stop and wait for explicit approval.

Do not proceed automatically.

Examples of valid approval:

- "批准"
- "可以执行"
- "按这个方案修改"
- "Proceed with this implementation"

Silence, previous approval for another task, and general discussion do NOT constitute approval.

#### Phase 4 — Execute

Only after approval:

- Implement the approved changes.
- Modify only the approved files.
- Follow the approved implementation plan.
- Do not introduce unrelated changes.
- Do not silently expand the scope.

If new problems or additional modifications become necessary, STOP and request further approval.

---

## 6. Approval Scope and Change Control

Approval is limited to the specific modification plan presented to the owner.

For example:

If approval was granted to modify `package.spec`, this does NOT authorize modifications to:

- `build.sh`
- `install.sh`
- `systemd/*.service`
- Other SPEC files
- Repository configuration
- Unrelated documentation

Additional changes require additional approval.

If the implementation differs from the approved plan, stop and explain why.

Never use an approved task as permission to perform unrelated cleanup, refactoring, optimization, or formatting.

Approval to modify files does NOT automatically authorize building, testing, packaging, or installing the result.

These operations have a separate authorization requirement described in Section 8.

AGENTS.md remains protected regardless of the scope of an approved task.

---

## 7. Research and Diagnostic Operations

The following operations are generally allowed without modification approval, provided they do not change project or system state:

- Reading project files.
- Inspecting directory structures.
- Reading upstream source code.
- Browsing official documentation.
- Checking Git history.
- Inspecting existing RPM metadata.
- Querying package dependencies.
- Checking package versions.
- Reviewing logs.
- Running read-only diagnostic commands.
- Analyzing existing build failures.
- Reviewing existing build artifacts.

When uncertain whether a command modifies state, do not execute it.

Explain its potential effects and request permission first.

Do not execute commands that:

- Install or remove packages.
- Change repository configurations.
- Modify system settings.
- Change boot configurations.
- Restart or stop system services.
- Overwrite project files.
- Generate build artifacts.
- Modify the host system.

Unless the owner explicitly authorizes the relevant operation.

---

## 8. Build, Packaging and Testing Policy

### 8.1 Disabled by Default

**All post-modification build, packaging, and testing operations are DISABLED by default.**

After completing an approved modification, you MUST NOT automatically execute:

- RPM builds.
- `rpmbuild`.
- `mock`.
- `rpmlint`.
- Package build pipelines.
- CI/CD workflows.
- Automated test suites.
- Package installation.
- Package removal.
- Runtime testing.
- Integration testing.
- Any other build or validation procedure.

This restriction applies even when:

- The modification is small.
- The SPEC file has been changed.
- The build appears straightforward.
- You believe verification is necessary.
- You want to confirm that the modification works.
- The build is likely to succeed.

Do not initiate build or verification operations without explicit authorization.

### 8.2 Explicit Authorization Required

Build and package verification may only be performed when the project owner explicitly requests it.

Examples:

- "执行打包验证"
- "运行 rpmlint"
- "使用 mock 构建"
- "帮我测试这个 SPEC"
- "Run the RPM build."

Authorization to modify files does NOT imply authorization to build or test them.

### 8.3 After Modification Without Verification

When verification has not been requested:

1. Inspect the final Git diff using read-only operations.
2. Identify all modified files.
3. Summarize the implementation.
4. Explain the intended behavior.
5. Clearly state that no build, packaging, or testing was performed.

Do not claim that the modification works, builds successfully, or passes Fedora packaging review without actual verification.

### 8.4 When Verification Is Requested

When the owner explicitly requests verification:

- Perform only the requested verification.
- Use the appropriate tools for the target Fedora release.
- Report commands that were executed.
- Report actual results.
- Identify failures and warnings.
- Do not silently modify additional files to fix verification failures.

If fixing a newly discovered issue requires further modifications, return to Section 5 and obtain approval.

### 8.5 Mandatory Distinction

This policy applies ONLY to post-modification build, packaging, and testing.

It does NOT waive mandatory upstream investigation BEFORE modifications.

**Upstream verification is always mandatory.**

**Post-modification build verification is optional and requires explicit authorization.**

---

## 9. Technical Accuracy and Communication

### 9.1 Evidence-Based Answers

Never present assumptions as facts.

Distinguish clearly between:

- Verified upstream behavior.
- Official Fedora requirements.
- Existing project implementation.
- Technical inference.
- Proposed changes.
- Unverified hypotheses.

Whenever possible, provide direct links to relevant:

- Source code.
- Official documentation.
- Commits.
- Issues.
- Pull requests.
- Release notes.

### 9.2 Do Not Guess

If information is insufficient:

- State what is unknown.
- Explain what needs verification.
- Investigate before proposing changes.
- Ask the owner when necessary.

Do not invent:

- Configuration options.
- RPM macros.
- Dependencies.
- Command-line arguments.
- Systemd directives.
- Upstream recommendations.
- Test results.

### 9.3 Respect Existing Architecture

Before proposing architectural changes:

- Understand the existing project structure.
- Identify existing conventions.
- Understand the intended build and deployment workflow.
- Avoid introducing unnecessary dependencies.
- Avoid replacing existing mechanisms without evidence.

Prefer minimal, maintainable changes that solve the verified problem.

---

## 10. Mandatory Response Format Before Modifications

Every proposed modification MUST use this format.

### Investigation Results

**Problem:**

Describe the identified problem.

**Current Implementation:**

Explain how the project currently handles it.

**Upstream Verification:**

Describe upstream behavior and provide direct references.

**Root Cause:**

Explain the verified cause or clearly identify any remaining uncertainty.

### Proposed Changes

**Files Affected:**

List every file that would be modified.

**Implementation:**

Explain the exact changes.

**Fedora Compliance:**

Explain which Fedora packaging requirements apply, if relevant.

**Risks:**

Describe possible side effects.

**Implementation Scope:**

Clearly define what will and will not be modified.

### Approval Required

Clearly state:

- No modifications have been made.
- No build or package verification has been performed.
- Explicit approval is required before implementation.
- AGENTS.md will remain untouched.

Then wait for the owner's authorization.

---

## 11. Final Rules — Non-Negotiable

1. Fedora packaging standards are mandatory for RPM SPEC files.
2. Upstream verification is mandatory before every modification.
3. Evidence must be provided before proposing implementation changes.
4. Explicit owner approval is mandatory before modifying files.
5. Approval applies only to the agreed scope.
6. Never silently modify additional files.
7. Never fabricate test results or upstream references.
8. Never assume that a request for analysis authorizes implementation.
9. Never automatically build, package, or test after modifications.
10. Build and package verification require separate explicit authorization.
11. When uncertain, STOP and ASK.
12. AGENTS.md is protected and MUST NOT be modified without explicit owner authorization.
13. General project approval does NOT authorize changes to AGENTS.md.
14. Never weaken, bypass, or remove these instructions independently.

**The project owner has final authority over all implementation decisions.**

Your responsibility is to investigate, explain, propose, and execute only what has been explicitly approved.

**No approval, no modification.**

**No explicit verification request, no build.**

**No explicit AGENTS.md modification request, no changes to AGENTS.md.**
