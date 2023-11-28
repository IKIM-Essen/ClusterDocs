# Efficient cluster Computing patterns

`Nota bene`: The cluster can accomodate so much IO at any one point. IO is where computing breaks. At the node level and certainly at the cluster level.

The cluster provices a number of storage facilities described 
[here](./storage.md). Make sure you are familiar with them _and_ you understand the nature of local vs. remote file systems.

## Local file systems
Every Linux machine has at least one local filesystem. Ours typically have a minimum of 2 hard drives. One is dedicated to system things (and some scratch space for the system) and is thus quite full and quite limited. The other is a data drive mounted at /local/work.

The local file systems are limited in size, but provide more IO bandwidth than network or remote drives.

Note: Anything that is `/homes`, `/groups` or `projects` is a remote file system. See [here](./storage.md) for some details.

## Remote file systems and what not to do
Remote file systems are a great idea, for some applications and some use cases. Computing on remote data is typically a really bad idea. You will waste a lot of cycles on your computing device waiting for data to be moved onto your computing devices RAM and subsequently any CPU or GPU caches. While the file servers are equipped to handle a lot of IO, dozens or hundreds of clients will easily overwhelm them. 

A good pattern is to stream your data to local disk (maybe from an object store) compute on it and later move or copy your result files onto a network share (never write to a network directly). This way you can avoid being slowed down by other users. We recommend an object store as this can handle more users in parallel without slowing down.