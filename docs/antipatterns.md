# Anti patterns

This document contains a list of "don't do this" type of things. The intent is to add lessons learned on how NOT TO DO things.

## The most common mistake

Is to not pay attention to the storage location of your data when doing computing. Make sure any and all data you use for computing resides on local storage (/local/work).
Failure to do that will slow your compute down (often by a factor of 1000) and impact all other users.

Also make sure results are writting to local storage and later moved or copied to a shared filesystem. 

## Blocking nodes with your editor by executing ripgrep

We notice some users running processes taking a lot of CPU and IO with rg (short for ripgrep). This code is executed by Visual Studio Code and is probably not adding any value to the user.

Jan Trienes commented:

``` { .sh }
a good thing to know here is that VSCode recursive search 
excludes patterns given in .gitignore and .  ignore. 
So best practice is to have a language-specific gitignore 
in the project to avoid searches over common directories with 
tens of thousands of small files (like venv/node_modules etc.)
```
