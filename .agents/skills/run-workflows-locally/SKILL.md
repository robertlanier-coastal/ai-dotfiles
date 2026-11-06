---
name: run-workflows-locally
description: >
  Runs GitHub Actions workflows on the user's machine with nektos/act (Docker or
  Podman) to test a CI change before it is pushed. Use whenever the user wants to
  test, try, check, debug or dry-run a workflow, job or composite action locally,
  asks "does this workflow work", "run the PR checks", "test the CI", mentions act,
  or has just edited a file in .github/workflows/ or .github/actions/ and needs proof
  it runs, even if they do not say "act".
---

# Run Workflows Locally

Quick reference: test GitHub Actions workflows on your machine with
[nektos/act](https://github.com/nektos/act) before you push.

## Mission

Run a workflow job locally to catch errors in minutes, not after a push. act reads
the files in `.github/workflows/`, starts a container that acts like a GitHub
runner (a short-lived machine that runs the job), and runs each step in it.

## Core capabilities

- **Run one job or a whole workflow:** `-j <job-id>` or `-W <workflow file>`.
- **Simulate the trigger:** `pull_request`, `push`, `workflow_dispatch` and other
  events. The default event is `push`.
- **Run jobs it depends on:** with `-j`, act also runs the jobs listed in that job's
  `needs:`, so their outputs reach the job.
- **Use local and composite actions:** `uses: ./.github/actions/<name>` works.
- **Pass secrets and variables:** `-s NAME`, `--var NAME=value`, or files.
- **Check without running:** `-n` (dry run) checks the workflow and the plan. A dry
  run creates no job outputs, so a job whose `if:` reads `needs.<job>.outputs` is
  skipped without a message. Run for real to test those jobs.

## Quick start

```bash
# List workflows and jobs (the job ID is what -j needs)
act -l

# Run one job, triggered as a pull request
act pull_request -W .github/workflows/ci.yml -j lint

# Dry run: check the workflow and what would run, start nothing
act pull_request -W .github/workflows/ci.yml -j lint -n

# Map a runner label act does not know (for example ubuntu-slim) for this run
act pull_request -j changes -P ubuntu-slim=catthehacker/ubuntu:act-24.04

# Pass a secret from your environment, never typed into the command
act pull_request -j deploy -s GITHUB_TOKEN="$(gh auth token)"

# Keep the output short: show only step and job results
act pull_request -j lint 2>&1 | grep -E "Success - |Failure - |Job (succeeded|failed)"
```

## Prerequisites

No admin rights are needed for act. Pick one container engine: **Podman** installs
without admin on a Mac. **Docker Desktop** needs admin to install, and a paid
license at large companies, so on a managed laptop ask IT for it.

**act (Mac):**

1. Download `act_Darwin_arm64.tar.gz` (Apple silicon) or `act_Darwin_x86_64.tar.gz`
   (Intel) from [act releases](https://github.com/nektos/act/releases).
2. Double-click it to extract `act`, then copy it to `~/.local/bin`.
3. Run `chmod +x ~/.local/bin/act`. If macOS blocks it, run
   `xattr -d com.apple.quarantine ~/.local/bin/act`.
4. Check: `act --version`.

**act (Windows):**

1. Download `act_Windows_x86_64.zip` from [act releases](https://github.com/nektos/act/releases).
2. Extract it and copy `act.exe` to `%USERPROFILE%\.local\bin`.
3. Add that folder to your user PATH: Start menu, "Edit environment variables for
   your account", Path, New.
4. Check in a new terminal: `act --version`.

**Container engine:** Podman (no admin on a Mac) or Docker Desktop. Steps are in
[REFERENCE.md](REFERENCE.md#install-a-container-engine).

## Common patterns

### Test before you push

```bash
# 1. The workflow file is valid and the plan looks right (see the dry-run note above)
act pull_request -W .github/workflows/ci.yml -j lint -n
# 2. The job passes
act pull_request -W .github/workflows/ci.yml -j lint
# 3. Push only after it passes
git push
```

act copies your working folder into the container, so **uncommitted edits are
tested too**. Git commands inside the job (for example `git diff HEAD^1 HEAD`)
still see your last commit.

### Debug a failing job

```bash
act pull_request -j lint -v                 # verbose: every command and its output
act pull_request -j lint -r                 # keep the container after success
act pull_request -j lint 2>&1 | tee /tmp/act.log   # save the full log
grep -iE "error|not found|failure" /tmp/act.log     # find the first error
```

### Matrix jobs

```bash
act -j build                                # every matrix combination
act -j build --matrix os:ubuntu-24.04       # one combination
```

### Jobs that sign in to the cloud

Steps that use OIDC (`permissions: id-token: write`, for example a cloud CLI that
signs in with GitHub's token) cannot run in act: there is no GitHub token service
locally. Run the jobs that do not sign in (lint, parse, security checks), and test
the sign-in jobs on the pull request run.

## Runner images

act maps each `runs-on:` label to a container image. Set the mapping once in your
config (see [Configuration](#configuration)) so act never asks.

| GitHub runner | Image to use with act | Note |
|---|---|---|
| `ubuntu-latest` | `catthehacker/ubuntu:act-24.04` | Matches GitHub's current `ubuntu-latest` (24.04) |
| `ubuntu-24.04` | `catthehacker/ubuntu:act-24.04` | |
| `ubuntu-22.04` | `catthehacker/ubuntu:act-22.04` | |
| `ubuntu-slim` | `catthehacker/ubuntu:act-24.04` | Not in act's defaults. Map it with `-P`. |

The `act-*` images are about 1.7 GB. The `full-*` images are much larger and are
only needed when a job uses tools the `act-*` image lacks.

## Pass/fail criteria

**Pass:** every step shows `Success -`, and the last line is `Job succeeded`.

**Fail:**

- A step shows `Failure -`, or the last line is `Job failed`.
- An error before any step runs (for example `Expected format {org}/{repo}[/path]@ref`)
  means act could not read the workflow or resolve an action.
- A sign-in or token error in an OIDC step is a local limit, not a workflow bug.

## Configuration

act reads `actrc` files, one option per line and no comments, in this order: the
XDG one (`~/.config/act/actrc`), then `~/.actrc`, then `.actrc` in the folder you
run act from. Command-line options come last.

```text
-P ubuntu-latest=catthehacker/ubuntu:act-24.04
-P ubuntu-24.04=catthehacker/ubuntu:act-24.04
-P ubuntu-slim=catthehacker/ubuntu:act-24.04
--container-architecture linux/arm64
--container-daemon-socket -
```

- `--container-architecture linux/arm64`: on Apple silicon, use native images.
- `--container-daemon-socket -`: do not mount the engine socket into the job
  container. Needed with Podman; harmless with Docker.

Secrets and variables, if a job needs them, go in files outside git (add them to
`.gitignore` first): `--secret-file .secrets`, `--var-file .vars`, `--env-file .env`.

## Limitations

- **OIDC sign-in** (`id-token: write`) does not work locally.
- **`uses: $/...`** (GitHub's self-repository syntax) is rejected by act 0.2.97 and
  older: `Expected format {org}/{repo}[/path]@ref`. Use `./...` until act supports it
  ([nektos/act#6189](https://github.com/nektos/act/issues/6189)).
- **Version tags must exist:** act clones each action at its tag. An action that
  publishes only exact tags (for example `v10.3.3`, no `v10`) fails on a major tag.
- **Dry runs (`-n`) skip jobs gated on `needs` outputs**, because no outputs exist.
- **Runner labels act does not know** (for example `ubuntu-slim`) need a `-P` mapping.
- **GitHub-only features** (caches shared across runs, the job summary page,
  annotations on the pull request) do not appear locally. Annotation lines
  (`::error ...`) are still printed in the log.

## Performance target

- **First run:** pulling the 1.7 GB image takes a few minutes.
- **Later runs:** the container starts in seconds.
- **Example:** a lint job with SQL lint and Python checks took about 75 s; a
  job-setup step with uv took about 5 s.

## Need more detail?

Read [REFERENCE.md](REFERENCE.md) for:

- Installing Podman or Docker Desktop without admin (Mac and Windows)
- Pointing act at Podman (`DOCKER_HOST`)
- Events with a payload (`-e event.json`), inputs and artifacts
- Troubleshooting common errors
