# Transferring data to the IKIM cluster

`Nota bene`: The cluster can accomodate only de-identified data,  no directly patient related data can be uploaded. All PII personal identifying information has to be removed prior to upload.

The cluster provices a number of storage facilities described 
[here](./storage.md).

## Introduction to data transfer

Data transfer across the network offers a great way to avoid the use of sneakernet (i.e. carrying hard drivers around campus to move data from A to B). We strongly advise reading the info on the cluster storage prior to moving forward here.

Larger scale data transfer requires some degree of familiarity with the technologies available and the sending and receiving systems.

We provide three different means for data transfer. We note that for larger transfers, the speed of the device the data is stored on remotely makes a difference.

### Using a web browser to move data into the cluster

Use your web browser to upload data to a facility we yet have to build.

Details: (TBA)

Advantages: UI driven
Disadvantages: not suitable for many files
Intended data scope: up to 500GB works

### Using ssh / scp to move data into the cluster

In short on the remote system execute
`tar -cpf - | ssh -J login.ikim.uk-essen.de shellhost.ikim.uk-essen.de "tar -xpf -" `

Read [this](https://www.cyberciti.biz/faq/howto-use-tar-command-through-network-over-ssh-session/) for more details.

### Using NC to move data into the cluster

In short: 
- ensure NC is installed on the remote system
- you need to execute commands on both sending and receiving system
On the receiving end, use this command:

cd /projects/<MY RECEIVING DIRECTORY>
nc -vl 44444 | tar zxv
netcat-receiving-tar-gzipped-directory

On the sending end, use:

tar czp /path/to/directory/to/send | nc -N 10.11.12.10 44444
netcat-sending-tar-gzipped-directory

Read this [this](https://www.maketecheasier.com/netcat-transfer-files-between-linux-computers/)


## How to pick a path here

Depending on your needs and the systems involved, your technology choices may vary. The table below might help pick the right path.


| approach | size limit | number of files | comment |
| ---  | --- |  -- | ---|
| browser  | 500 GB | <100 | easy to use |
| ssh/scp  | 5TB | unlimited | use tar to group files |
| nc       | unlimiteed  | complicated, use zip or tar to group files | 

### Miscellaneous comments

The local storage on each node typically consists of a system partition and a data partition. 