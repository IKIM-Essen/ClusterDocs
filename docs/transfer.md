# Transferring data to the IKIM cluster

`Nota bene`: The cluster can accomodate only de-identified data,  no directly patient related data can be uploaded. All PII personal identifying information has to be removed prior to upload.

The cluster provices a number of storage facilities described
[here](./storage.md).

## Introduction to data transfer

Data transfer across the network offers a great way to avoid the use of sneakernet (i.e. carrying hard drivers around campus to move data from A to B). We strongly advise reading the info on the cluster storage prior to moving forward here.

Larger scale data transfer requires some degree of familiarity with the technologies available and the sending and receiving systems.

We provide three different means for data transfer. We note that for larger transfers, the speed of the device the data is stored on remotely makes a difference.

### Using ssh / scp to move data into the cluster

In short on the remote system execute
`tar -cpf - | ssh -J login.ikim.uk-essen.de shellhost.ikim.uk-essen.de "tar -xpf -"`

Read [this](https://www.cyberciti.biz/faq/howto-use-tar-command-through-network-over-ssh-session/) for more details.

### Using NC to move data into the cluster

In short:

- ensure NC is installed on the remote system
- you need to execute commands on both sending and receiving system
On the receiving end, use this command:

``` { .sh }
cd /projects/<MY RECEIVING DIRECTORY>
nc -vl 44444 | tar zxv
netcat-receiving-tar-gzipped-directory
```

On the sending end, use:

``` { .sh }
tar czp /path/to/directory/to/send | nc -N 10.11.12.10 44444
netcat-sending-tar-gzipped-directory
```

Read this [this](https://www.maketecheasier.com/netcat-transfer-files-between-linux-computers/)

## How to pick a path here

Depending on your needs and the systems involved, your technology choices may vary. The table below might help pick the right path.

| approach | size limit | number of files | comment |
| ---  | --- |  -- | ---|
| browser  | 500 GB | <100 | easy to use |
| ssh/scp  | 5TB | unlimited | use tar to group files |
| nc       | unlimited | unlimited | complicated, use zip or tar to group files |

### Miscellaneous comments

The local storage on each node typically consists of a system partition and a data partition.

# Uploading data to the European Genome-phenome Archive (EGA)

There are different paths to upload data to different European Genome-phenome Archive (EGA) server locations, and each can be used from different interfaces to then provide the project and sample metadata.
Please refer to the [EGA submission documentation](https://ega-archive.org/) for up to date details on the different pathways.
Here, we only document working ways of doing the data upload:

## SFTP upload to the EGA Inbox

The SFTP upload to the EGA Inbox should work as described in the [EGA submission documentation](https://ega-archive.org/submission/data/uploading-files/inbox/).
However, this restricts Metadata submission to the Submitter Portal, which is not documented beyond the obvious features.
So if anything doesn't work there, you cannot finish your submission and might have to wait weeks for the HelpDesk to respond.

## FTP upload to EGA

For this pathway, make sure to first encrypt your data with [EGACryptor, as described in the EGA docs](https://ega-archive.org/submission/data/uploading-files/ftp/).
The only tool we got working for FTP upload is `LFTP`, however [**not** as described in the EGA docs](https://ega-archive.org/submission/data/uploading-files/ftp/#FTPTLS).
Instead, the following set of commands should get a working FTP connection established:

``` {.sh }
lftp # this just starts the tool and sends you to an lftp prompt, all the following commands are within lftp
set ftp:ssl-allow 0
open ftp.ega.ebi.ac.uk
USER <ega_user_name>
```

This should ask for your password and after successful login you should be able to use all the [standard `lftp` commands](https://linux.die.net/man/1/lftp), for example `ls` to query the remote directory or `mput` to upload multiple files.
With this upload route, you should then be able to use the [programmatic metadata submission via Webin](https://ega-archive.org/submission/metadata/submission/programmatic-submission-xml/).
