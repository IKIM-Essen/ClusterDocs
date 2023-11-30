# Good patterns

This document contains a list of "do this" type of things. The intent is to add lessons learned on how TO DO things.


## Tips on Working with remote computing services

- [Unix Crash Course](https://tildesites.bowdoin.edu/~sbarker/unix/)
- [Another Unix Course](https://www.csoft.net/docs/course.html)
- [Tactical tmux: The 10 Most Important Commands](https://danielmiessler.com/study/tmux/)
- [How To Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)
- [Git Book](https://git-scm.com/book/en/v2)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda)



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

## GitHub Authentication through SSH

To clone GitHub repositories on the cluster over the `git+ssh` protocol, you need to (1) configure your local ssh client as per the [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), and (2) enable agent forwarding (if you use the ssh config above, this should already be done). You can verify your setup with following command:

```sh
USER@g1-9:~$ ssh -T git@github.com
Hi USER! You've successfully authenticated, but GitHub does not provide shell access.
```