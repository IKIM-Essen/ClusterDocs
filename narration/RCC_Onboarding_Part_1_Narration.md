# RCC Onboarding Part 1 - Narration

## Slide 1: Your first day on the RCC cluster

Welcome to Part One of the RCC onboarding curriculum. This lesson is designed for biomedical researchers who may be very experienced in their scientific domain but new to Linux clusters. We will build a mental model before using any commands. You will see what runs on your own computer, what runs on the cluster, why secure shell is used, how Visual Studio Code connects, how data transfer differs from interactive login, and why Slurm controls compute jobs. By the end, you should be able to connect, move a small test file, submit a batch job, and verify where it ran. The examples are intentionally small and contain no sensitive research data.

## Slide 2: 1. A cluster is a shared scientific instrument

Think of the RCC as a shared scientific instrument rather than a faster desktop computer. The login host is the reception desk. It authenticates you and lets you prepare work, but it is not intended for heavy analysis. Compute nodes are the instruments that run CPU, memory, or GPU intensive jobs. Shared storage holds project data and results. Slurm is the booking and scheduling system that decides when and where a job can run. This separation protects other users and makes large analyses repeatable. A command typed in the wrong place can affect many people, so every tutorial will tell you where a command runs and what success looks like.

## Slide 3: 2. Local and remote: know where you are

A major source of confusion is the local and remote split. Your keyboard, web browser, and normal desktop applications are local. When secure shell is connected, the terminal prompt is remote and commands execute on the RCC. Visual Studio Code also has two sides: the graphical application remains on your laptop, while its remote extension starts helper processes on the cluster and opens remote files. Always inspect the hostname, current directory, and prompt before deleting or moving files. A file in Downloads on Windows or macOS is not automatically visible on RCC storage. It must be transferred through an approved transfer mechanism.

## Slide 4: 3. Why SSH and why keys?

Secure Shell, usually called S S H, provides an encrypted channel between your computer and the cluster. Encryption protects credentials and commands while they travel across networks. An SSH key pair has a private key and a public key. The private key stays on your own computer. The public key can be registered with RCC. During login, the two sides prove that the correct private key is present without sending that private key to the server. A passphrase protects the private key if the laptop is lost. Store that passphrase in an approved password manager before you finish creating the key. Never email or upload the private key.

## Slide 5: 4. Prepare Windows or macOS

On Windows, use a current supported version with the built-in OpenSSH client. PowerShell is the simplest terminal for the first test. On macOS, the Terminal application already includes an SSH client. Install the desktop version of Visual Studio Code and then install the Microsoft Remote - SSH extension. The sequence matters. First prove that the command line connection works. Only then configure VS Code, because the editor uses the same SSH configuration underneath. This makes errors easier to diagnose. Keep your operating system updated and do not install keys or configuration files from untrusted sources.

## Slide 6: 5. The SSH route: gateway, submission host, and ProxyJump

The RCC connection may use a gateway before reaching the submission host. ProxyJump tells SSH to authenticate through the gateway while preserving end-to-end SSH behavior. A small configuration file gives the route a memorable alias such as R C C. The exact hostnames and official host-key fingerprints must come from RCC administrators. Do not accept a changed fingerprint merely because a dialog appears. A changed key can indicate a rebuilt host, a configuration issue, or an attack. Test the route in a normal terminal and record the exact error message if it fails.

## Slide 7: 6. VS Code is local software with a remote workspace

Visual Studio Code is not itself the cluster. The window runs locally, but the Remote - SSH extension opens a workspace on the RCC submission host. A colored remote indicator shows the active connection. The Explorer then lists remote files, and the integrated terminal starts remotely. Extensions may need a remote installation because some code runs near the files. Before editing, verify the remote indicator, run hostname in the terminal, and open the intended project directory rather than your entire home directory. Do not launch long analyses in the integrated terminal. Use Slurm, and use tmux only to protect the lightweight workflow controller or monitoring session.

## Slide 8: 7. Data transfer is a separate workflow

Interactive SSH is optimized for commands, not for moving large biomedical datasets. The approved browser transfer service provides a managed path for uploads and downloads. Use a project directory agreed with your group, not a random folder in your home directory. Transfer only data permitted by the project and institutional policy. For a small training file, calculate a SHA two fifty-six checksum locally, upload the file, calculate the checksum on RCC, and compare the values. Matching checksums show that the bytes are identical. For clinical or identifiable data, follow the approved data-protection process rather than improvising with personal cloud storage or email.

## Slide 9: 8. Why Slurm?

Slurm is the resource manager. Instead of choosing a compute node yourself, you describe the resources required by a job: time, CPUs, memory, and sometimes a GPU. Slurm queues the job, finds a suitable node, starts the job, records its state, and releases resources afterwards. The request should be realistic. Too little memory can kill the job; too much memory can delay scheduling and waste capacity. A batch script is a plain text record of the command and requested resources. That makes it easier to repeat, audit, and share than an undocumented interactive session.

## Slide 10: 9. Your first batch job

The first job should be deliberately simple. Create a working directory and a batch script that requests one CPU, a small amount of memory, and a few minutes. The script prints the hostname, creates a few numbers, and calculates a mean using standard tools. Submit it with s batch. Slurm returns a job identifier. Use s queue to see whether it is pending or running, and s acct after completion to inspect the final state. Open the output log and confirm that the hostname belongs to a compute node. The important lesson is the job lifecycle, not the arithmetic.

## Slide 11: 10. Why tmux?

A normal SSH connection ends when the laptop sleeps, the network changes, or the terminal closes. T mux creates a persistent terminal session on the remote host. You can detach, disconnect, reconnect later, and reattach. This is useful for editing, monitoring, or running a Snakemake controller that submits jobs to Slurm. It does not grant more compute resources and it does not make it acceptable to run heavy analysis on the login host. A good mental model is that tmux preserves the steering wheel, while Slurm provides the engine. Name sessions clearly and close them when the work is complete.

## Slide 12: 11. First-day completion checklist

You are ready to continue when you can demonstrate each outcome rather than merely following the steps once. You can identify whether a terminal is local or remote. You can explain the difference between your private and public keys. You have verified the official server fingerprint. Command-line SSH works before Visual Studio Code. You can open the correct remote project directory. You can transfer a small non-sensitive file and match its checksum. You can submit a batch script, observe its job identifier, and confirm that it completed on a compute node. Keep the commands and logs; they are useful evidence when asking for support.

