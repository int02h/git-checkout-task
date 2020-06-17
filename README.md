# git-checkout-task
[![Latest release](https://img.shields.io/github/release/int02h/git-checkout-task.svg)](https://github.com/int02h/git-checkout-task/releases/latest)

Git custom command to checkout branch for a specific task

## Description

This custom git command is intended to simplify checkout of feature-branch for a specific task from issue tracker like Jira.

## Requirements

- Feature-branch must have a prefix with the task ID.  
  For example, for task `ABC-1234` you'd create branch `ABC-1234-awesome-bugfix`.

## How to use

```bash
git checkout-task ABS-1234
```

If the command name looks long for you just add an alias for it:

```bash
git config --global alias.cot checkout-task
```

## How it works

1. Grep all branches including remote ones with the task ID
1. Removes everything before the last slash inclusive from the branch name thus `remotes/origin/ABC-1234-awesome-bugfix` becomes just `ABC-1234-awesome-bugfix`
1. Checkout that branch

## Edge cases

**C** - case, **B** - behavior

**C**: You're already on the desired branch  
**B**: No branch checkout. Info message printed

**C**: There are no branches with the specified prefix  
**B**: No branch checkout. Error message printed

**C**: There is more than one branch with the specified prefix  
**B**: No branch checkout. The names of clashing branches will be printed

## How to install

Put the file `git-checkout-task` to any folder that is in the PATH and make it executable.

For example:

```bash
cd ~ && \
mkdir .gitbin && \
cd .gitbin && \
curl -o git-checkout-task https://raw.githubusercontent.com/int02h/git-checkout-task/master/git-checkout-task && \
chmod +x git-checkout-task
```

Then add `~/.gitbin` to the PATH. Put the following line in the `~/.bashrc`, or `~/.zshrc`, or in the script for whatever shell you're using:

```bash
export PATH=$PATH:~/.gitbin
```

## License

Copyright (c) 2020 Daniil Popov

Licensed under the [MIT](LICENSE) License.
