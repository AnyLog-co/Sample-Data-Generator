# GitHub Actions Version Update Automation

This repository uses **GitHub Actions** to automatically update the project version (`setup.cfg`) whenever specific branches are updated.

Because some branches (like `ms-dev`) are **protected branches**, normal workflows using `GITHUB_TOKEN` cannot push commits to them.
To solve this, we use a **GitHub App (`anylog-ci-bot`)** to authenticate and push updates.

This document explains:

* Why the GitHub App exists
* How the workflows work
* How to configure new branches to use the same automation

---

# Architecture Overview

Two workflows exist:

```
.github/workflows/
├─ generate_git_id.py
├─ version-update.yml
└─ version-update-ms-dev.yml
```

| File                        | Purpose                                                     |
| --------------------------- | ----------------------------------------------------------- |
| `generate_git_id.py`        | Python script that updates the version inside `setup.cfg`   |
| `version-update.yml`        | Generic workflow for most branches                          |
| `version-update-ms-dev.yml` | Special workflow that can push to protected branch `ms-dev` |

---

# Why a GitHub App Is Required

GitHub protected branches often block pushes from the default GitHub Actions token (`GITHUB_TOKEN`).

Example error:

```
remote: error: GH006: Protected branch update failed
You're not authorized to push to this branch
```

To bypass this restriction securely, we created a **GitHub App**:

```
anylog-ci-bot
```

The workflow generates an **installation token** from the app and uses it for the push.

This allows automation while keeping branch protection enabled.

---

# GitHub App Configuration

The GitHub App must:

### Permissions

```
Repository permissions:
  Contents → Read & Write
```

### Repository Access

Install the app on the organization:

```
AnyLog-co
```

and grant access to:

```
AnyLog-Network
```

---

# Repository Secrets

The workflows require the following secrets.

```
Settings → Secrets → Actions
```

| Secret          | Description                           |
| --------------- | ------------------------------------- |
| `ANYLOG_APP_ID` | GitHub App ID                         |
| `MOSHE_PEM`     | Private key (.pem) for the GitHub App |

Example private key format:

```
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

Never commit this file to the repository.

---

# Protected Branch Configuration

If a branch is protected, the GitHub App must be allowed to push.

Go to:

```
Repository → Settings → Branches
```

Edit the rule for the branch (example: `ms-dev`) and add:

```
anylog-ci-bot (GitHub App)
```

under:

```
Restrict who can push to matching branches
```

---

# Workflow: Standard Branches

File:

```
version-update.yml
```

Triggers on pushes to:

```
main
pre-develop
os-dev
```

These branches allow normal pushes using the default token.

Workflow flow:

```
push
 ↓
checkout repository
 ↓
run generate_git_id.py
 ↓
update setup.cfg
 ↓
commit and push
```

Authentication:

```
GITHUB_TOKEN
```

---

# Workflow: Protected Branch (ms-dev)

File:

```
version-update-ms-dev.yml
```

Trigger:

```
push → ms-dev
```

Because the branch is protected, the workflow:

1. Generates a GitHub App token
2. Checks out the repository using the app token
3. Updates the version
4. Pushes back to `ms-dev`

Important step:

```yaml
- name: Generate GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.ANYLOG_APP_ID }}
    private-key: ${{ secrets.MOSHE_PEM }}
    owner: AnyLog-co
    repositories: AnyLog-Network
```

---

# How to Enable Automation for Another Protected Branch

Example: `release-dev`

### 1. Create a workflow

Copy:

```
version-update-ms-dev.yml
```

Rename:

```
version-update-release-dev.yml
```

Update the trigger:

```yaml
on:
  push:
    branches:
      - release-dev
```

Update the push target:

```yaml
git push origin HEAD:release-dev
```

---

### 2. Allow the GitHub App to push

```
Repo → Settings → Branches
```

Edit the rule for:

```
release-dev
```

Add:

```
anylog-ci-bot
```

---

### 3. Commit the workflow

```
git add .github/workflows/version-update-release-dev.yml
git commit -m "add version automation for release-dev"
git push
```

The automation will now run for the new branch.

---

# Security Notes

• The GitHub App private key **must never be stored in the repository**.
• Always store it in **GitHub Actions Secrets**.
• If the key is ever exposed, rotate it immediately.

---

# Maintenance

If the GitHub App stops working:

1. Verify the app is installed on the organization
2. Verify repository permissions
3. Verify secrets (`ANYLOG_APP_ID`, `MOSHE_PEM`)
4. Verify branch protection allows `anylog-ci-bot`

---

# Summary

| Component      | Purpose                              |
| -------------- | ------------------------------------ |
| GitHub App     | Allows pushing to protected branches |
| Actions Secret | Stores private key securely          |
| Workflow       | Automates version updates            |
| Branch Rule    | Grants push permission to the bot    |

This setup keeps branch protection enabled while allowing controlled automation.

---
