# Good patterns

This document contains a list of dos and don'ts. The intent is to emphasize lessons learned.

## Using local and network storage appropriately

The place where your data is stored during computation is a major factor in performance. Make sure that any and all data you use for computing resides on local storage (`/local/work`). Failure to do so will slow your compute down (often by a factor of 1000) and impact all other users.

Also make sure that results are written to local storage and later moved or copied to a shared filesystem.

## VSCode: Prevent Expensive Full Text Searches

We notice some users running processes taking a lot of CPU and network IO with `rg` (short for ripgrep). This code is executed by Visual Studio Code when running full text searches (e.g., <kbd>cmd</kbd> + <kbd>shift</kbd> + <kbd>f</kbd>). Be aware that such searches may be _very_ expensive when you have many files in your project, especially when your code is on an NFS location (e.g., `/homes` or `/groups`)

Therefore, you should limit the search space. Two options:

1. (recommended) VSCode by default excludes files from search that match patterns in `.gitignore` and `.ignore`.  So best practice is to have a language-specific gitignore in the project to avoid searches over directories which have tens of thousands of small files (like venv, node_modules, dist, etc.). Most likely you also want to exclude `data/`.
2. Disable search. Open vscode settings, search for `search.exclude`, add pattern (`**` and `*`). This will exclude all files from search.
