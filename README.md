[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/zefr0x/check_commit/main.svg)](https://results.pre-commit.ci/latest/github/zefr0x/check_commit/main)

don't know why you need
[commitlint](https://github.com/conventional-changelog/commitlint) with 13000+
lines of code running on top of nodejs

this is just a simple regex with some python to check for
[Conventional Commits](https://www.conventionalcommits.org) standard

simple config

not user friendly

neither detailed error message nor handling, just read your docs (maybe read the
source code), it is your issue

## Usage

```
check_commit <max-line-length> <commit-types> <footer-types> <optional-file>
```

When no input file is specified it will read from stdin.

For example:

```sh
check_commit 74 feat,fix Fixes,Refs ./.git/COMMIT_EDITMSG
# or
printf "feat(ui): add new button" | check_commit 74 feat,fix Fixes,Refs
```

### pre-commit hook

```yaml
default_install_hook_types:
  - pre-commit
  - commit-msg
repos:
  - repo: https://github.com/zefr0x/check_commit
    rev: v0.1.0
    hooks:
      - id: conventional-commit-message
        stages: [commit-msg]
        # To overwrite the default config:
        args: [
          "74",
          "feat,fix,refac,deps,sty,lint,test,build,cid,dev,release,docs,i18n,data,revert",
          "Fixes,Closes,Resolves,Refs,Signed-off-by,Co-authored-by",
        ]
```
