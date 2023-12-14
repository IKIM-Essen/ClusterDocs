# Good patterns

This document contains a list of dos and don'ts. The intent is to emphasize lessons learned.

## Using local and network storage appropriately

The place where your data is stored during computation is a major factor in performance. Make sure that any and all data you use for computing resides on local storage (`/local/work`). Failure to do so will slow your compute down (often by a factor of 1000) and impact all other users.

Also make sure that results are written to local storage and later moved or copied to a shared filesystem.

## Configuring VSCode to not run rg

We notice some users running processes taking a lot of CPU and IO with rg (short for ripgrep). This code is executed by Visual Studio Code and is probably not adding any value to the user.

Jan Trienes commented:

``` { .sh }
a good thing to know here is that VSCode recursive search 
excludes patterns given in .gitignore and .  ignore. 
So best practice is to have a language-specific gitignore 
in the project to avoid searches over common directories with 
tens of thousands of small files (like venv/node_modules etc.)
```
