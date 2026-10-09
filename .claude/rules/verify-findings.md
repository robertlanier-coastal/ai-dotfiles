# Verify Findings Before Reporting

Before reporting any findings — code review issues, bugs, static analysis results, security
vulnerabilities, configuration problems, or any other defects — verify each one is real and
not a false positive.

## Required verification steps

1. **Confirm the symptom exists**: read the relevant code, config, or file directly. Do not
   report based on pattern-matching alone.
2. **Trace the execution path**: confirm the problematic code is actually reachable and not
   guarded by a condition that prevents the issue.
3. **Check external facts**: if the finding depends on a package name, API behavior, platform
   quirk, or tool version, verify it — search the web, read docs, or run a command.
4. **Test the counter-case**: actively try to disprove the finding. If you can construct a
   scenario where the code is correct, the finding may be a false positive.

## When verification is not possible

If you cannot verify a finding (no container runtime, no network access, docs unavailable),
say so explicitly alongside the finding. Do not report it as confirmed. Use language like
"unverified — could not check X" rather than stating it as fact.

## Reporting

Only report findings that survived verification. Label each as:
- **Confirmed**: verified through code inspection, execution trace, or external source.
- **Plausible**: logic suggests an issue but full verification was not possible — state what
  was checked and what remains uncertain.

Do not report findings labeled as false positives.
