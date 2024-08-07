# Accessing cluster storage on Windows and Mac clients

You can access storage on the cluster directly from your laptop (or if need be from a desktop computer). This is not intended for transferring large amounts of data, but rather for editing a spreadsheet needed for the next experiment that is stored on a server in the IKIM network and is mounted to the lab instrument.

Secure access to file server storage in the cluster is available via sshFS. It is not intended for large file transfer. See [XXXX](http://some.where) for options for large file transfer.

We will first ensure all the bits are in place, test the setup and finally set your system up to automatically connect to directories on the file servers.

While you can mosly cut-copy-paste, you still
need to replace user, group and project names with your own.

Below is a resonable configuration for a home directory, a group directory and one project directory.

| name | remote directory | local directory  |  Parameters|
| ---  | --- |  -- | ---|
| Home directory    | /homes/juser/ | /Users/joe/remote/ |`-odefer_permissions,volname=HOMES-DIR`|
| Group directory    | /groups/experts/ | /Users/joe/group/ |`-defer_permissions,volname=GROUPDIR`|
| Project directory | /project/workwithme/ | /Users/joe/project/|`-odefer_permissions,volname=PROJECTDIR`|

Please insert your username, groupname and project name respectively. You can add more directories if you so desire.

## HowTo for Windows Clients

We have tested this on Windows 11, setup requires approx 5-10 minutes assuming ssh connectivity was available up front.

For Windows clients the procedure is bascially a four step procedure:

1. install [Winget](https://github.com/microsoft/winget-cli) ideally from the Microsoft [App Store](https://www.microsoft.com/p/app-installer/9nblggh4nns1)

2. install [WinFSP](https://github.com/billziss-gh/winfsp/releases/latest)
On the Windows command line:

   ```bash
   winget install -h -e --id "WinFsp.WinFsp" 
   ```
  
3. install [SSHFS-Win](https://github.com/billziss-gh/sshfs-win/releases)
  On the Windows command line:

   ```bash
   winget install -h -e --id "SSHFS-Win.SSHFS-Win"
   ```

4. map the network drive
  In `Windows Explorer` select `This PC` > `Map Network Drive` and enter the desired drive letter and SSHFS path using the following UNC syntax:

  ```bash
  \\sshfs\juser@shellhost.ikim.uk-essen.de[\homes\juser]
  ```

  Where you replace juser with your cluster login name.

We acknowledge that this is following the instructions [here](https://github.com/winfsp/sshfs-win) and [here](https://www.petergirnus.com/blog/how-to-sshfs-on-windows).

## HowTo for Mac Clients

We provide a step-by-step guide for setting up secure remote storage access.

1. Install MacFuse
 Follow the instructions at [MacFuse](https://osxfuse.github.io). Please note that this will require at least one reboot and some level of  attention to details. It should take about 3-5 minutes to complete.

2. Ensure sure that your `~/.ssh/config` file is set up correctly

   Check our [guide](access.md) on setting up the ssh config.

3. Verify your `~/.ssh/config` file
 Note: You will not need to do this to use the storage, but if this does not work, there is
something wrong with your ssh setup.

   ```ssh shellhost```

   If this does not work, please check the guide above.

4. Create an empty directory Mac for temporary purposes

   Open a  Terminal window and type

     ```mkdir ~/remote```

   Or use the Finder to create this directories. (Please note this guide assumes there is not already a file or directory by this name.)

5. Mount your homes directory into your local environment

In your Terminal execute the command below to mount, after replacing "juser" with your own username for the cluster.

   ```sshfs juser@shellhost.ikim.uk-essen.de:/homes/juser $HOME/remote/
    odefer_permissions,volname=HOMES-DIR```

We supply a volume name (`volname`) to describe the directory, you can modify the name to your liking.

5. check if things work
Type `mount | fgrep ikim` and you should see something link

    ```
    juser@shellhost.ikim.uk-essen.de:/homes/juser on /Users/joe/remote (macfuse, nodev, nosuid, 
synchronous, mounted by juser)
    ```

You are now connected to your home directory on the file server.

You can now either use command line tools like `ls` or use the Mac Finder to browse the directory. But we are not done, if you close your laptop or log out, the network drive will not re-appear. So we need to ensure its available permanently.

6. Remove the temporary bits

Before we automate the setup, we need to clean up.
You can use the Finder to unmount the directory (right-click) and remove the now empty directory that we created earlier.

Or you can type:

    ```
    diskutil unmount force ~/remote
    rmdir ~/remote
    ```

7. Now set up permanent access to the server

    1. Download ConnectMeNow
    Depending on your computer use [Apple Silicon]( https://www.tweaking4all.com/downloads/network/ConnectMeNow4-v4.0.18-macOS-arm64.dmg) or [Intel](https://www.tweaking4all.com/downloads/network/ConnectMeNow4-v4.0.18-macOS-x86-64.dmg) to download the software.

8. Follow [this guide](https://www.tweaking4all.com/software/macosx-software/connectmenow-v4/) on how to use the software to automate mounting.

    1. Ensure you set the following parameters are set for share

        ![Share-setup](./assets/ConnectMeNow-share-setup.png)
        * select SSHFS as ShareType
        * set Server Address: `shellhost.ikim.uk-essen.de`
        * set the Path to your homes-directory e.g. `/homes/juser`

    2. Ensure you set the following parameters are set for Advanced Options

        ![Advanced-setup](./assets/ConnectMeNow-advanced-setup.png)
        * ensure that the menu title makes sense, we suggest using `homes-dir`, etc.
        * ensure that under Advanced settings `Ping before mount` is disabled
        * ensure under MountStyle you use `-o follow_symlinks,defer_permissions,volname=homes-dir`

9. Success.

If everything worked well so far, you should now have set up one or more Share definition in ConnectMeNow. The software will appear as an entry in the menu bar of your Mac like this
![menubaricon](./assets/ConnectMeNow-icon.png).

You have now successfully enabled file secure server access to the server using your existing SSH configuration.

Please note that this is not the correct option to transfer very large files.

10. FAQs

    1. If you experience a permisssion denied response, you forgot the `-odefer_permissions` parameter

    2. ConnectMeNow disappeared, check the menu bar.
