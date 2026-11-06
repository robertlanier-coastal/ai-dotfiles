# Run Workflows Locally: Reference

Details for [SKILL.md](SKILL.md). Read the section you need.

## Contents

- [Install a container engine](#install-a-container-engine)
  - [Podman on a Mac (no admin)](#podman-on-a-mac-no-admin)
  - [Podman on Windows](#podman-on-windows)
  - [Docker Desktop](#docker-desktop)
- [Point act at Podman](#point-act-at-podman)
- [Events, inputs and artifacts](#events-inputs-and-artifacts)
- [Troubleshooting](#troubleshooting)

## Install a container engine

act runs each job in a container, so it needs an engine that speaks the Docker
Engine API (the interface Docker's tools use). Podman and Docker Desktop both do.

| | Podman | Docker Desktop |
|---|---|---|
| Admin to install | Mac: no. Windows: WSL2 must already be on (admin, one time). | Yes, on Mac and Windows |
| License | Free (Apache 2.0) | Free for small companies; paid at large companies |
| act setting | `DOCKER_HOST` and `--container-daemon-socket -` | None: act finds Docker's socket |

### Podman on a Mac (no admin)

Podman on a Mac runs Linux in a small virtual machine (the "podman machine").
The client and two helper programs all live in your home folder.

1. **Podman client.** Download `podman-remote-release-darwin_arm64.zip` from
   [Podman releases](https://github.com/containers/podman/releases). Extract it, then
   copy `podman` and `podman-mac-helper` from `podman-<version>/usr/bin/` to
   `~/.local/bin`.
2. **Helpers.** Make the folder: `mkdir -p ~/.local/libexec/podman`. Then download:
   - `gvproxy-darwin` from [gvisor-tap-vsock releases](https://github.com/containers/gvisor-tap-vsock/releases);
     save it as `~/.local/libexec/podman/gvproxy`.
   - `vfkit` from [vfkit releases](https://github.com/crc-org/vfkit/releases);
     save it as `~/.local/libexec/podman/vfkit`.
3. **Make them runnable** and clear the download block:

   ```bash
   chmod +x ~/.local/bin/podman ~/.local/bin/podman-mac-helper ~/.local/libexec/podman/*
   xattr -d com.apple.quarantine ~/.local/bin/podman* ~/.local/libexec/podman/* 2>/dev/null
   ```

4. **Tell Podman where the helpers are.** Create `~/.config/containers/containers.conf`
   (replace `<you>` with your user name):

   ```toml
   [engine]
   helper_binaries_dir = ["/Users/<you>/.local/libexec/podman"]

   [machine]
   provider = "applehv"
   ```

5. **Create and start the machine** (the first start downloads a Linux image):

   ```bash
   podman machine init
   podman machine start
   podman info --format '{{.Host.Arch}}'   # check: prints arm64
   ```

### Podman on Windows

Not tested on Windows yet. The steps follow the Podman release files.

1. Podman on Windows runs Linux in WSL2 (Windows Subsystem for Linux). Turning
   WSL2 on needs admin once. On a managed laptop, ask IT. Check with `wsl --status`.
2. Download `podman-remote-release-windows_amd64.zip` from
   [Podman releases](https://github.com/containers/podman/releases). Extract it, and copy
   `podman.exe`, `gvproxy.exe` and `win-sshproxy.exe` from `podman-<version>\usr\bin\`
   to `%USERPROFILE%\.local\bin` (already on your PATH if you set up act).
3. Create and start the machine: `podman machine init`, then `podman machine start`.

### Docker Desktop

1. Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/).
   The installer needs admin. On a managed laptop, request it from IT.
2. Start Docker Desktop. Check with `docker info`.
3. Nothing else: act finds Docker's socket by itself. Leave out
   `--container-daemon-socket -` if you like; it is harmless either way.

## Point act at Podman

act looks for the engine in `DOCKER_HOST`. Set it in your shell profile so every
new terminal has it.

**Mac (zsh):** the machine's socket path is shown by Podman itself:

```bash
podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}'
```

It is usually under `$TMPDIR`, so this line in `~/.zshrc` works across restarts:

```bash
export DOCKER_HOST="unix://${TMPDIR}podman/podman-machine-default-api.sock"
```

**Windows (not tested):** Podman serves a named pipe. Find it with
`podman machine inspect --format '{{.ConnectionInfo.PodmanPipe.Path}}'`, then set
`DOCKER_HOST` to `npipe://` followed by that path in your user environment variables.

**Also add** `--container-daemon-socket -` to your `actrc`. Without it, act tries to
mount the Podman socket into the job container and fails.

Check the setup: `act -l` lists jobs, and a small job runs, for example
`act pull_request -j lint -n`.

## Events, inputs and artifacts

**Event payload.** A workflow that reads the event (for example
`github.event.pull_request.number`) gets empty values unless you give a payload:

```bash
cat > /tmp/pr.json <<'EOF'
{ "pull_request": { "number": 123, "head": { "ref": "my-branch" }, "base": { "ref": "main" } } }
EOF
act pull_request -e /tmp/pr.json -j lint
```

**Manual-run inputs** (`workflow_dispatch`):

```bash
act workflow_dispatch -W .github/workflows/deploy.yml --input full=true
```

**Variables** (`vars.NAME`) and **secrets** (`secrets.NAME`):

```bash
act -j deploy --var MY_VAR=value -s API_KEY="$API_KEY"
act -j deploy --var-file .vars --secret-file .secrets   # files must be git-ignored
```

**Artifacts.** `actions/upload-artifact` needs a local store:

```bash
act -j build --artifact-server-path /tmp/act-artifacts
```

**Graph.** `act -g` draws the jobs and their `needs:` order, which helps when a job
is skipped unexpectedly.

## Troubleshooting

| Message | Cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Engine not running, or `DOCKER_HOST` not set | Start Podman (`podman machine start`) or Docker Desktop. Check `echo $DOCKER_HOST`. |
| Error mounting `docker.sock` or the Podman socket | act mounts the engine socket into the job container | Add `--container-daemon-socket -` |
| `Unable to resolve v10: reference not found` | The action has no such tag (some publish only exact tags) | Use an exact tag, for example `@v10.3.3` |
| `Expected format {org}/{repo}[/path]@ref` | `uses: $/...` self-repository syntax | Use `./...` until act supports `$/` |
| `uv: command not found` (or another tool) in a later step | An earlier setup step failed | Scroll up to the first `Failure -` step |
| A job is skipped | Its `if:` uses outputs from a job that did not run, or the trigger does not match | Run with `-j` so `needs:` jobs run first; check the event (`pull_request` vs `push`) |
| Sign-in or token error | OIDC (`id-token: write`) is not available locally | Expected. Test that job on the pull request run. |
| macOS says the program "cannot be opened" | Download quarantine | `xattr -d com.apple.quarantine <file>` |
| Image pull is slow or fails | First run downloads about 1.7 GB | Wait, or pull ahead: `podman pull catthehacker/ubuntu:act-24.04` |
