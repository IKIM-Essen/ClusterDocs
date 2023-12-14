# Good patterns

This document contains a list of "do this" type of things. The intent is to add lessons learned on how TO DO things.

## Configuring VSCODE to not run rg

We notice some users running processes taking a lot of CPU and IO with rg (short for ripgrep). This code is executed by Visual Studio Code and is probably not adding any value to the user.

Jan Trienes commented:

``` { .sh }
a good thing to know here is that VSCode recursive search 
excludes patterns given in .gitignore and .  ignore. 
So best practice is to have a language-specific gitignore 
in the project to avoid searches over common directories with 
tens of thousands of small files (like venv/node_modules etc.)
```
