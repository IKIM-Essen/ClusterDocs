const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const OUT = '/mnt/data/rcc-curriculum-v2';
fs.mkdirSync(path.join(OUT, 'slides'), {recursive:true});
fs.mkdirSync(path.join(OUT, 'narration'), {recursive:true});

const W = 13.333, H = 7.5;
const C = {
  navy: '17324D', teal: '007C83', green: '3A8D63', blue: '2C6EAF',
  coral: 'D15B47', purple: '7057A3', amber: 'C58A13',
  ink: '1F2937', muted: '5E6B78', pale: 'F3F6F8', white: 'FFFFFF',
  line: 'D7E0E7', darkPale: 'E7EEF3', red: 'B23B3B', yellow: 'F4E8B9'
};
const FONT = 'Liberation Sans';
const MONO = 'Liberation Mono';

function addText(slide, text, x, y, w, h, opts={}) {
  slide.addText(text, {
    x,y,w,h, fontFace: opts.fontFace || FONT, fontSize: opts.fontSize || 18,
    color: opts.color || C.ink, bold: !!opts.bold, italic: !!opts.italic,
    margin: opts.margin === undefined ? 0 : opts.margin,
    valign: opts.valign || 'mid', align: opts.align || 'left',
    breakLine: false, fit: 'shrink', ...opts
  });
}
function addShape(slide, type, x,y,w,h, opts={}) {
  slide.addShape(type, {x,y,w,h, line: opts.line || {color:C.line, width:1}, fill: opts.fill || {color:C.white}, radius:opts.radius, ...opts});
}
function addFooter(slide, part, idx, total, accent) {
  slide.addShape('line',{x:.45,y:7.12,w:12.42,h:0,line:{color:C.line,width:1}});
  addText(slide, `RCC onboarding · Part ${part}`, .48, 7.17, 4.2,.18,{fontSize:9,color:C.muted});
  addText(slide, `${idx} / ${total}`, 11.9,7.17,.9,.18,{fontSize:9,color:C.muted,align:'right'});
  slide.addShape('rect',{x:.45,y:7.12,w:.55,h:.03,line:{color:accent,transparency:100},fill:{color:accent}});
}
function addHeader(slide, title, subtitle, part, idx, total, accent) {
  addText(slide,title,.55,.28,12.1,.45,{fontSize:27,bold:true,color:C.navy});
  if (subtitle) addText(slide,subtitle,.57,.78,12,.30,{fontSize:12.5,color:C.muted});
  addFooter(slide,part,idx,total,accent);
}
function card(slide, x,y,w,h, title, body, accent, opts={}) {
  addShape(slide,'roundRect',x,y,w,h,{rectRadius:.08,line:{color:opts.lineColor||C.line,width:1},fill:{color:opts.fill||C.white}});
  slide.addShape('rect',{x:x,y:y,w:.07,h:h,line:{color:accent,transparency:100},fill:{color:accent}});
  addText(slide,title,x+.22,y+.16,w-.38,.35,{fontSize:17,bold:true,color:opts.titleColor||C.navy});
  addText(slide,body,x+.22,y+.58,w-.38,h-.72,{fontSize:opts.fontSize||14.5,color:opts.color||C.ink,valign:'top',breakLine:true,fit:'shrink'});
}
function pill(slide,text,x,y,w,accent) {
  addShape(slide,'roundRect',x,y,w,.34,{line:{color:accent,transparency:100},fill:{color:accent,transparency:88}});
  addText(slide,text,x+.08,y+.02,w-.16,.28,{fontSize:11,bold:true,color:accent,align:'center'});
}
function arrow(slide,x1,y1,x2,y2,color=C.muted,width=2) {
  slide.addShape('line',{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width,beginArrowType:'none',endArrowType:'triangle'}});
}
function titleSlide(pptx, cfg, idx, total) {
  const s=pptx.addSlide();
  s.background={color:C.pale};
  s.addShape('rect',{x:0,y:0,w:W,h:H,line:{color:cfg.accent,transparency:100},fill:{color:cfg.accent}});
  s.addShape('rect',{x:.25,y:.25,w:W-.5,h:H-.5,line:{color:C.white,transparency:100},fill:{color:C.white,transparency:100}});
  addText(s,`PART ${cfg.part}`,1.0,.75,2.2,.38,{fontSize:16,bold:true,color:C.white,charSpacing:2.5});
  addText(s,cfg.title,1.0,1.35,10.9,1.2,{fontSize:34,bold:true,color:C.white,valign:'top'});
  addText(s,cfg.subtitle,1.02,2.72,10.5,.9,{fontSize:19,color:C.white,valign:'top'});
  addShape(s,'roundRect',1.0,4.35,5.6,1.15,{line:{color:C.white,transparency:75},fill:{color:C.white,transparency:88}});
  addText(s,cfg.outcome,1.28,4.58,5.05,.72,{fontSize:16,color:C.white,bold:true,valign:'top'});
  addText(s,'For biomedical researchers new to distributed computing',1.02,6.40,8.7,.35,{fontSize:13,color:C.white});
  addText(s,'RCC onboarding curriculum',10.2,6.40,2.1,.35,{fontSize:11,color:C.white,align:'right'});
  s.addNotes(cfg.notes);
  return s;
}
function simpleBullets(slide, items, x,y,w,h, opts={}) {
  const runs=[];
  items.forEach((it,i)=>{
    const [head, rest] = it.includes('::') ? it.split('::') : ['',it];
    runs.push({text: head ? head+': ' : '', options:{bullet:{indent:16},hanging:4,bold:!!head,breakLine:false}});
    runs.push({text:rest, options:{breakLine:true}});
  });
  slide.addText(runs,{x,y,w,h,fontFace:FONT,fontSize:opts.fontSize||17,color:opts.color||C.ink,breakLine:false,margin:0,paraSpaceAfterPt:9,valign:'top',fit:'shrink'});
}
function sectionBand(slide, n, label, accent, x=.55,y=1.18,w=12.2) {
  addShape(slide,'roundRect',x,y,w,.58,{line:{color:accent,transparency:100},fill:{color:accent,transparency:92}});
  addShape(slide,'ellipse',x+.14,y+.08,.42,.42,{line:{color:accent,transparency:100},fill:{color:accent}});
  addText(slide,String(n),x+.14,y+.10,.42,.36,{fontSize:13,bold:true,color:C.white,align:'center'});
  addText(slide,label,x+.69,y+.08,w-.83,.40,{fontSize:17,bold:true,color:accent});
}
function addDeck(cfg, slidesDef) {
  const pptx = new pptxgen();
  pptx.layout='LAYOUT_WIDE';
  pptx.author='RCC / IKIM Essen';
  pptx.subject=cfg.subtitle;
  pptx.title=`RCC Onboarding Part ${cfg.part}: ${cfg.title}`;
  pptx.company='Institute for AI in Medicine, University Hospital Essen';
  pptx.lang='en-US';
  pptx.theme={headFontFace:FONT,bodyFontFace:FONT,lang:'en-US'};
  pptx.defineSlideMaster({
    title:'MASTER',background:{color:C.white},objects:[]
  });
  const total=slidesDef.length+1;
  titleSlide(pptx,cfg,1,total);
  const narr=[{slide:1,title:cfg.title,text:cfg.notes}];
  slidesDef.forEach((d,k)=>{
    const idx=k+2;
    const s=pptx.addSlide('MASTER');
    s.background={color:C.white};
    addHeader(s,d.title,d.subtitle||'',cfg.part,idx,total,cfg.accent);
    d.draw(s,cfg.accent);
    s.addNotes(d.notes);
    narr.push({slide:idx,title:d.title,text:d.notes});
  });
  const out=path.join(OUT,'slides',`RCC_Onboarding_Part_${cfg.part}.pptx`);
  pptx.writeFile({fileName:out});
  let md=`# RCC Onboarding Part ${cfg.part} - Narration\n\n`;
  narr.forEach(n=>{md+=`## Slide ${n.slide}: ${n.title}\n\n${n.text}\n\n`;});
  fs.writeFileSync(path.join(OUT,'narration',`RCC_Onboarding_Part_${cfg.part}_Narration.md`),md);
  fs.writeFileSync(path.join(OUT,'narration',`RCC_Onboarding_Part_${cfg.part}_Narration.json`),JSON.stringify(narr,null,2));
}

const deck1={
 part:1,accent:C.teal,title:'Your first day on the RCC cluster',
 subtitle:'Understand the cluster, connect safely, transfer data, and run a first Slurm job.',
 outcome:'Outcome: a verified remote session and a completed batch job - without treating the login node as a workstation.',
 notes:`Welcome to Part One of the RCC onboarding curriculum. This lesson is designed for biomedical researchers who may be very experienced in their scientific domain but new to Linux clusters. We will build a mental model before using any commands. You will see what runs on your own computer, what runs on the cluster, why secure shell is used, how Visual Studio Code connects, how data transfer differs from interactive login, and why Slurm controls compute jobs. By the end, you should be able to connect, move a small test file, submit a batch job, and verify where it ran. The examples are intentionally small and contain no sensitive research data.`
};
const slides1=[
 {title:'1. A cluster is a shared scientific instrument',subtitle:'Many computers, one coordinated service',notes:`Think of the RCC as a shared scientific instrument rather than a faster desktop computer. The login host is the reception desk. It authenticates you and lets you prepare work, but it is not intended for heavy analysis. Compute nodes are the instruments that run CPU, memory, or GPU intensive jobs. Shared storage holds project data and results. Slurm is the booking and scheduling system that decides when and where a job can run. This separation protects other users and makes large analyses repeatable. A command typed in the wrong place can affect many people, so every tutorial will tell you where a command runs and what success looks like.`,draw:(s,a)=>{
  const nodes=[['Your laptop','Editor, terminal\nand local files'],['Login host','Authentication\nand preparation'],['Slurm','Queues and\nresource allocation'],['Compute node','Analysis runs\nhere'],['Shared storage','Project data\nand results']];
  const xs=[.55,3.08,5.61,8.14,10.67];
  nodes.forEach((n,i)=>{card(s,xs[i],2.05,2.1,2.25,n[0],n[1],i===2?C.coral:a,{fontSize:15}); if(i<4) arrow(s,xs[i]+2.1,3.16,xs[i+1],3.16,i===1?C.coral:C.muted,2);});
  addShape(s,'roundRect',2.0,5.05,9.4,.72,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Rule of thumb: prepare on the login host; compute through Slurm; keep data in approved storage.',2.25,5.22,8.9,.36,{fontSize:18,bold:true,color:a,align:'center'});
 }},
 {title:'2. Local and remote: know where you are',subtitle:'The same screen can show two different computers',notes:`A major source of confusion is the local and remote split. Your keyboard, web browser, and normal desktop applications are local. When secure shell is connected, the terminal prompt is remote and commands execute on the RCC. Visual Studio Code also has two sides: the graphical application remains on your laptop, while its remote extension starts helper processes on the cluster and opens remote files. Always inspect the hostname, current directory, and prompt before deleting or moving files. A file in Downloads on Windows or macOS is not automatically visible on RCC storage. It must be transferred through an approved transfer mechanism.`,draw:(s,a)=>{
  card(s,.65,1.45,5.65,4.75,'LOCAL - your computer','• Browser and password manager\n• VS Code interface\n• Downloads folder\n• Private SSH key\n• Network connection',C.blue,{fontSize:18,fill:'F8FAFC'});
  card(s,7.02,1.45,5.65,4.75,'REMOTE - RCC','• Shell prompt and Linux commands\n• Project and home directories\n• VS Code remote workspace\n• Slurm commands\n• Compute jobs',a,{fontSize:18,fill:'F8FAFC'});
  arrow(s,5.95,3.16,7.35,3.16,C.coral,3);
  pill(s,'SSH connection',5.80,2.68,1.75,C.coral);
  addText(s,'Check:  hostname   pwd   whoami',4.42,6.36,4.5,.34,{fontFace:MONO,fontSize:15,bold:true,color:C.navy,align:'center'});
 }},
 {title:'3. Why SSH and why keys?',subtitle:'Encrypted access with a machine-verifiable identity',notes:`Secure Shell, usually called S S H, provides an encrypted channel between your computer and the cluster. Encryption protects credentials and commands while they travel across networks. An SSH key pair has a private key and a public key. The private key stays on your own computer. The public key can be registered with RCC. During login, the two sides prove that the correct private key is present without sending that private key to the server. A passphrase protects the private key if the laptop is lost. Store that passphrase in an approved password manager before you finish creating the key. Never email or upload the private key.`,draw:(s,a)=>{
  sectionBand(s,1,'SSH protects the connection',a);
  card(s,.8,2.05,3.65,2.8,'Private key','Stays on your laptop.\nBack it up only through an approved secure mechanism.\nNever send it to support.',C.coral,{fontSize:16});
  card(s,4.85,2.05,3.65,2.8,'Encrypted channel','Commands, file metadata, and authentication travel through a protected connection.',a,{fontSize:16});
  card(s,8.9,2.05,3.65,2.8,'Public key','Registered on RCC.\nSafe to share for account setup.\nCannot be used as the private key.',C.green,{fontSize:16});
  arrow(s,4.42,3.36,4.87,3.36,a,2); arrow(s,8.48,3.36,8.91,3.36,a,2);
  addShape(s,'roundRect',2.25,5.35,8.85,.72,{line:{color:C.red,transparency:100},fill:{color:C.red,transparency:92}});
  addText(s,'The host-key fingerprint verifies the server; your key verifies you.',2.5,5.53,8.35,.34,{fontSize:18,bold:true,color:C.red,align:'center'});
 }},
 {title:'4. Prepare Windows or macOS',subtitle:'Three components: OpenSSH, VS Code, and the Remote - SSH extension',notes:`On Windows, use a current supported version with the built-in OpenSSH client. PowerShell is the simplest terminal for the first test. On macOS, the Terminal application already includes an SSH client. Install the desktop version of Visual Studio Code and then install the Microsoft Remote - SSH extension. The sequence matters. First prove that the command line connection works. Only then configure VS Code, because the editor uses the same SSH configuration underneath. This makes errors easier to diagnose. Keep your operating system updated and do not install keys or configuration files from untrusted sources.`,draw:(s,a)=>{
  const steps=[['1','OpenSSH','Creates and tests the secure connection.'],['2','VS Code','Provides the editor and integrated terminal.'],['3','Remote - SSH','Opens files and terminals on RCC.'],['4','Terminal test','Prove `ssh rcc` works before opening VS Code.']];
  steps.forEach((st,i)=>{
   const x=.7+i*3.15; addShape(s,'ellipse',x,1.75,.62,.62,{line:{color:a,transparency:100},fill:{color:a}}); addText(s,st[0],x,1.87,.62,.3,{fontSize:17,bold:true,color:C.white,align:'center'});
   card(s,x-.05,2.55,2.78,2.75,st[1],st[2],a,{fontSize:16});
   if(i<3) arrow(s,x+2.73,3.93,x+3.12,3.93,C.muted,2);
  });
  addText(s,'Windows: PowerShell  |  macOS: Terminal',3.8,5.75,5.7,.38,{fontSize:18,bold:true,color:C.navy,align:'center'});
 }},
 {title:'5. The SSH route: gateway, submission host, and ProxyJump',subtitle:'One friendly alias can hide the multi-hop route',notes:`The RCC connection may use a gateway before reaching the submission host. ProxyJump tells SSH to authenticate through the gateway while preserving end-to-end SSH behavior. A small configuration file gives the route a memorable alias such as R C C. The exact hostnames and official host-key fingerprints must come from RCC administrators. Do not accept a changed fingerprint merely because a dialog appears. A changed key can indicate a rebuilt host, a configuration issue, or an attack. Test the route in a normal terminal and record the exact error message if it fails.`,draw:(s,a)=>{
  const items=[['Laptop','ssh rcc'],['Gateway','Internet-facing\nentry point'],['Submission host','Prepare files\nand submit jobs']];
  [1.1,5.05,9.0].forEach((x,i)=>card(s,x,1.75,3.2,2.3,items[i][0],items[i][1],i===1?C.coral:a,{fontSize:17}));
  arrow(s,4.3,2.90,5.05,2.90,C.coral,3); arrow(s,8.25,2.90,9.0,2.90,C.coral,3);
  pill(s,'ProxyJump',5.57,4.45,2.05,C.coral);
  addShape(s,'roundRect',1.25,5.28,10.85,.72,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Use only administrator-published hostnames and fingerprints.',1.6,5.46,10.15,.34,{fontSize:18,bold:true,color:a,align:'center'});
 }},
 {title:'6. VS Code is local software with a remote workspace',subtitle:'The interface stays on your laptop; files and terminals can be remote',notes:`Visual Studio Code is not itself the cluster. The window runs locally, but the Remote - SSH extension opens a workspace on the RCC submission host. A colored remote indicator shows the active connection. The Explorer then lists remote files, and the integrated terminal starts remotely. Extensions may need a remote installation because some code runs near the files. Before editing, verify the remote indicator, run hostname in the terminal, and open the intended project directory rather than your entire home directory. Do not launch long analyses in the integrated terminal. Use Slurm, and use tmux only to protect the lightweight workflow controller or monitoring session.`,draw:(s,a)=>{
  addShape(s,'roundRect',.75,1.4,11.85,4.85,{line:{color:C.line,width:1.2},fill:{color:'F7F9FB'}});
  addShape(s,'rect',{x:.75,y:1.4,w:11.85,h:.55,line:{color:C.navy,transparency:100},fill:{color:C.navy}});
  addText(s,'VS Code - SSH: rcc',1.0,1.53,4.5,.25,{fontSize:13,bold:true,color:C.white});
  addShape(s,'rect',{x:.75,y:1.95,w:2.75,h:3.85,line:{color:C.line,width:1},fill:{color:C.white}});
  addText(s,'EXPLORER\n\nproject/\n  data/\n  workflow/\n  results/',1.0,2.18,2.1,2.4,{fontFace:MONO,fontSize:15,color:C.ink,valign:'top'});
  addText(s,'Remote file editor',4.1,2.35,4.15,.38,{fontSize:20,bold:true,color:C.navy,align:'center'});
  addShape(s,'roundRect',4.25,3.0,3.85,1.15,{line:{color:a,width:1.5},fill:{color:a,transparency:93}});
  addText(s,'hostname\npwd\nwhoami',4.55,3.2,3.25,.74,{fontFace:MONO,fontSize:17,bold:true,color:a,align:'center'});
  addShape(s,'rect',{x:3.5,y:4.65,w:9.1,h:1.15,line:{color:C.line,width:1},fill:{color:'101820'}});
  addText(s,'[user@submission project]$ sbatch first_job.sh',3.78,4.98,8.4,.35,{fontFace:MONO,fontSize:15,color:'B9F6CA'});
  pill(s,'REMOTE',.93,5.86,1.45,a);
 }},
 {title:'7. Data transfer is a separate workflow',subtitle:'Move data deliberately, verify integrity, and respect data protection',notes:`Interactive SSH is optimized for commands, not for moving large biomedical datasets. The approved browser transfer service provides a managed path for uploads and downloads. Use a project directory agreed with your group, not a random folder in your home directory. Transfer only data permitted by the project and institutional policy. For a small training file, calculate a SHA two fifty-six checksum locally, upload the file, calculate the checksum on RCC, and compare the values. Matching checksums show that the bytes are identical. For clinical or identifiable data, follow the approved data-protection process rather than improvising with personal cloud storage or email.`,draw:(s,a)=>{
  const ys=2.05; const xs=[.8,3.95,7.1,10.25]; const labs=[['Select','approved source'],['Transfer','managed service'],['Store','project directory'],['Verify','matching checksum']];
  labs.forEach((n,i)=>{addShape(s,'ellipse',xs[i],ys,.72,.72,{line:{color:i===3?C.green:a,transparency:100},fill:{color:i===3?C.green:a}});addText(s,String(i+1),xs[i],ys+.15,.72,.36,{fontSize:18,bold:true,color:C.white,align:'center'}); addText(s,n[0],xs[i]-.48,3.0,1.7,.34,{fontSize:18,bold:true,color:C.navy,align:'center'});addText(s,n[1],xs[i]-.62,3.42,2.0,.56,{fontSize:14,color:C.muted,align:'center'}); if(i<3)arrow(s,xs[i]+.72,2.42,xs[i+1],2.42,C.muted,2);});
  addShape(s,'roundRect',1.45,4.75,10.4,.85,{line:{color:C.green,transparency:100},fill:{color:C.green,transparency:92}});
  addText(s,'Local SHA-256  =  RCC SHA-256  →  transfer verified',1.85,4.99,9.6,.36,{fontFace:MONO,fontSize:18,bold:true,color:C.green,align:'center'});
 }},
 {title:'8. Why Slurm?',subtitle:'A fair and auditable resource manager for shared compute',notes:`Slurm is the resource manager. Instead of choosing a compute node yourself, you describe the resources required by a job: time, CPUs, memory, and sometimes a GPU. Slurm queues the job, finds a suitable node, starts the job, records its state, and releases resources afterwards. The request should be realistic. Too little memory can kill the job; too much memory can delay scheduling and waste capacity. A batch script is a plain text record of the command and requested resources. That makes it easier to repeat, audit, and share than an undocumented interactive session.`,draw:(s,a)=>{
  const stages=[['Describe','time · CPU · RAM · GPU'],['Queue','wait fairly'],['Allocate','choose a node'],['Run','capture output'],['Account','inspect result']];
  stages.forEach((st,i)=>{const x=.52+i*2.55;card(s,x,1.65,2.25,2.55,st[0],st[1],i===1?C.amber:(i===3?C.green:a),{fontSize:15,fill:'FAFBFC'});if(i<4)arrow(s,x+2.25,2.92,x+2.54,2.92,C.muted,2);});
  addShape(s,'roundRect',1.05,4.78,11.2,1.05,{line:{color:a,width:1.2},fill:{color:a,transparency:94}});
  addText(s,'Batch script = resource request + reproducible command + output log',1.4,5.04,10.5,.42,{fontSize:20,bold:true,color:a,align:'center'});
 }},
 {title:'9. Your first batch job',subtitle:'Request small resources, submit, monitor, and inspect',notes:`The first job should be deliberately simple. Create a working directory and a batch script that requests one CPU, a small amount of memory, and a few minutes. The script prints the hostname, creates a few numbers, and calculates a mean using standard tools. Submit it with s batch. Slurm returns a job identifier. Use s queue to see whether it is pending or running, and s acct after completion to inspect the final state. Open the output log and confirm that the hostname belongs to a compute node. The important lesson is the job lifecycle, not the arithmetic.`,draw:(s,a)=>{
  addShape(s,'roundRect',.7,1.35,6.1,4.95,{line:{color:C.line,width:1},fill:{color:'101820'}});
  addText(s,'#!/bin/bash\n#SBATCH --job-name=first\n#SBATCH --time=00:05:00\n#SBATCH --cpus-per-task=1\n#SBATCH --mem=512M\n\nhostname\nprintf "1\\n2\\n3\\n4\\n5\\n" > values.txt\nawk \'{s+=$1} END {print s/NR}\' values.txt',1.0,1.64,5.5,4.3,{fontFace:MONO,fontSize:15,color:'D6F5DD',valign:'top'});
  const cmds=[['Submit','sbatch first_job.sh'],['Monitor','squeue -u $USER'],['Inspect','sacct -j JOBID'],['Read log','cat slurm-JOBID.out']];
  cmds.forEach((c,i)=>card(s,7.25,1.35+i*1.23,5.35,1.02,c[0],c[1],i===2?C.green:a,{fontSize:16,fill:'FAFBFC'}));
 }},
 {title:'10. Why tmux?',subtitle:'Protect a lightweight control session - not a compute job',notes:`A normal SSH connection ends when the laptop sleeps, the network changes, or the terminal closes. T mux creates a persistent terminal session on the remote host. You can detach, disconnect, reconnect later, and reattach. This is useful for editing, monitoring, or running a Snakemake controller that submits jobs to Slurm. It does not grant more compute resources and it does not make it acceptable to run heavy analysis on the login host. A good mental model is that tmux preserves the steering wheel, while Slurm provides the engine. Name sessions clearly and close them when the work is complete.`,draw:(s,a)=>{
  const x=.75;
  card(s,x,1.55,3.35,3.95,'Without tmux','Laptop sleeps\n↓\nSSH disconnects\n↓\ninteractive process ends',C.red,{fontSize:18,fill:'FFF9F8'});
  card(s,4.98,1.55,3.35,3.95,'With tmux','Detach session\n↓\nSSH disconnects\n↓\nreattach later',a,{fontSize:18,fill:'F7FCFC'});
  card(s,9.21,1.55,3.35,3.95,'Still use Slurm','tmux protects control\n\nSlurm supplies CPU, RAM, GPU, and compute nodes',C.green,{fontSize:18,fill:'F7FCF9'});
  addText(s,'tmux ≠ compute allocation',4.42,5.86,4.5,.38,{fontSize:20,bold:true,color:C.red,align:'center'});
 }},
 {title:'11. First-day completion checklist',subtitle:'Evidence that the setup works',notes:`You are ready to continue when you can demonstrate each outcome rather than merely following the steps once. You can identify whether a terminal is local or remote. You can explain the difference between your private and public keys. You have verified the official server fingerprint. Command-line SSH works before Visual Studio Code. You can open the correct remote project directory. You can transfer a small non-sensitive file and match its checksum. You can submit a batch script, observe its job identifier, and confirm that it completed on a compute node. Keep the commands and logs; they are useful evidence when asking for support.`,draw:(s,a)=>{
  const items=['Identify local versus remote','Protect the private SSH key','Verify the server fingerprint','Connect with `ssh rcc`','Open an RCC workspace in VS Code','Transfer and checksum a test file','Submit and inspect a Slurm job','Explain when tmux is appropriate'];
  items.forEach((it,i)=>{const col=i<4?0:1;const row=i%4;const x=.75+col*6.2;const y=1.45+row*1.18;addShape(s,'ellipse',x,y,.42,.42,{line:{color:C.green,transparency:100},fill:{color:C.green}});addText(s,'✓',x,y+.03,.42,.30,{fontSize:15,bold:true,color:C.white,align:'center'});addText(s,it,x+.62,y-.02,5.2,.48,{fontSize:17,bold:true,color:C.navy});});
  addShape(s,'roundRect',2.0,6.18,9.3,.55,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Next: reproducible environments, Snakemake, statistics, and DNA workflows.',2.25,6.30,8.8,.30,{fontSize:16,bold:true,color:a,align:'center'});
 }}
];

const deck2={part:2,accent:C.blue,title:'Reproducible scientific workflows',subtitle:'Use environments, Snakemake, Slurm, and version control for statistical and DNA analysis.',outcome:'Outcome: a small workflow that can be rerun, inspected, and extended without relying on memory.',notes:`Part Two moves from access to reproducible analysis. Biomedical projects combine data, software, parameters, compute resources, and scientific interpretation. Reproducibility requires us to describe all of those layers. We will explain why environments exist, why Miniforge and Bioconda are useful, why Snakemake models dependencies, and how Slurm executes the expensive work. We will use two intentionally small examples: a statistical analysis of tabular data and a DNA sequence workflow using synthetic reads. The goal is not to teach every method. The goal is to establish a structure that remains understandable when a project grows.`};
const slides2=[
 {title:'1. A result is more than a script',subtitle:'Reproducibility has several interacting layers',notes:`A scientific result depends on more than the code file. It also depends on input data, software versions, parameters, reference data, the order of operations, and the compute environment. If any of those are implicit, a colleague may be unable to reproduce the result even when the script is available. A good workflow separates immutable source data from generated output, records software dependencies, and makes each transformation explicit. In regulated or clinically adjacent work, this structure also supports review and provenance. The cluster does not automatically make work reproducible; it only provides shared resources.`,draw:(s,a)=>{
  const items=[['Data','raw inputs and metadata'],['Code','scripts and rules'],['Software','versions and dependencies'],['Parameters','thresholds and references'],['Execution','resources and logs'],['Interpretation','figures and conclusions']];
  items.forEach((it,i)=>{const ang=i*Math.PI/3;const cx=6.67+3.4*Math.cos(ang), cy=3.45+1.95*Math.sin(ang);card(s,cx-1.25,cy-.64,2.5,1.28,it[0],it[1],i===2?C.coral:a,{fontSize:12.5});arrow(s,cx,cy,6.67,3.45,C.line,1.4);});
  addShape(s,'ellipse',5.72,2.5,1.9,1.9,{line:{color:a,transparency:100},fill:{color:a}});addText(s,'REPRODUCIBLE\nRESULT',5.87,3.00,1.6,.9,{fontSize:17,bold:true,color:C.white,align:'center'});
 }},
 {title:'2. Project structure prevents accidental science',subtitle:'Separate source data, workflow logic, environments, logs, and results',notes:`A project directory is a small information architecture. Raw data should be treated as read-only. Workflow files describe how outputs are created. Scripts contain substantial analysis code. Environment files declare software. Logs and benchmarks describe execution. Results are generated and can be recreated. This separation prevents common mistakes such as editing a raw file, overwriting a result by hand, or losing track of which parameters produced a figure. Use meaningful sample identifiers and a metadata table rather than encoding all information in filenames. Keep secrets and patient identifiers out of Git repositories and logs.`,draw:(s,a)=>{
  addShape(s,'roundRect',.85,1.35,5.25,5.1,{line:{color:C.line,width:1.2},fill:{color:'101820'}});
  addText(s,'project/\n├── README.md\n├── config/\n├── data/\n│   ├── raw/\n│   └── metadata.tsv\n├── workflow/\n│   ├── Snakefile\n│   ├── rules/\n│   └── envs/\n├── scripts/\n├── logs/\n└── results/',1.22,1.67,4.45,4.55,{fontFace:MONO,fontSize:18,color:'D6F5DD',valign:'top'});
  card(s,6.55,1.35,5.9,1.35,'Raw data','Read-only source material; never silently modified.',C.coral,{fontSize:15});
  card(s,6.55,2.93,5.9,1.35,'Workflow + environments','Machine-readable dependencies, commands, and software.',a,{fontSize:15});
  card(s,6.55,4.51,5.9,1.35,'Results + logs','Generated outputs plus the evidence needed to interpret them.',C.green,{fontSize:15});
 }},
 {title:'3. What is a software environment?',subtitle:'A named, isolated set of compatible tools and libraries',notes:`Scientific software has dependencies. One tool may need a specific Python version, another a compiled library, and a third a command-line executable. Installing everything globally creates conflicts and makes projects fragile. An environment is an isolated collection of compatible packages. Miniforge provides the conda and mamba tools without a large preselected package set. Mamba resolves and installs packages efficiently. Bioconda is a community channel containing many bioinformatics packages. An environment file records the package names and, where appropriate, versions. It is a recipe, not a substitute for validation. Part Four will explain why large active environments should not live on network storage.`,draw:(s,a)=>{
  const layers=[['Analysis','Snakemake, R, Python, tools'],['Libraries','NumPy, pandas, htslib'],['Runtime','Python or R version'],['System','Linux on RCC']];
  layers.forEach((l,i)=>{const x=1.15+i*.55,y=1.45+i*1.12,w=10.95-i*1.1;addShape(s,'roundRect',x,y,w,.88,{line:{color:i===0?a:C.line,width:1.2},fill:{color:i===0?a:C.darkPale}});addText(s,l[0],x+.25,y+.13,2.0,.34,{fontSize:18,bold:true,color:C.navy});addText(s,l[1],x+2.25,y+.13,w-2.5,.34,{fontSize:16,color:C.ink});});
  addText(s,'environment.yml = software recipe',4.3,6.17,4.8,.38,{fontFace:MONO,fontSize:17,bold:true,color:a,align:'center'});
 }},
 {title:'4. Conda, Mamba, Bioconda, and channels',subtitle:'Different roles in the same packaging ecosystem',notes:`Conda is the environment and package model. Mamba is a compatible, faster resolver and installer. Miniforge is a compact distribution that provides these tools. Channels are package repositories, and Bioconda specializes in bioinformatics software. Channel order matters because packages from different repositories may be built against different libraries. Follow the RCC-supported configuration rather than copying arbitrary commands from an old tutorial. Keep the environment definition in the project, test it on synthetic data, and avoid continuously changing a shared environment underneath an active analysis. For production, a pinned container image is often more robust, as covered in Part Four.`,draw:(s,a)=>{
  const items=[['Miniforge','small distribution'],['Mamba','dependency solver'],['Conda environment','isolated package set'],['Bioconda','bioinformatics packages']];
  items.forEach((it,i)=>{const x=.65+i*3.15;card(s,x,1.65,2.78,2.3,it[0],it[1],i===3?C.green:a,{fontSize:16});if(i<3)arrow(s,x+2.78,2.78,x+3.12,2.78,C.muted,2);});
  addShape(s,'roundRect',1.05,4.65,11.2,1.12,{line:{color:C.coral,transparency:100},fill:{color:C.coral,transparency:93}});
  addText(s,'Use RCC-approved channel order and storage locations.\nAn environment definition must be tested; it is not proof of scientific validity.',1.45,4.88,10.4,.67,{fontSize:17,bold:true,color:C.coral,align:'center'});
 }},
 {title:'5. Snakemake describes dependencies, not just command order',subtitle:'Rules connect inputs to outputs in a directed acyclic graph',notes:`Snakemake is a workflow management system. Each rule declares input files, output files, software, resources, and a command or script. Snakemake builds a directed acyclic graph showing which outputs depend on which inputs. It runs only the steps needed to create the requested target. If an upstream input changes, the affected downstream steps can be recomputed. This is safer than a long shell script that assumes every previous command succeeded. The workflow graph also helps colleagues review the scientific logic. A dry run shows what would happen without executing commands.`,draw:(s,a)=>{
  const boxes=[{x:.65,y:2.6,t:'metadata.csv',c:C.coral},{x:3.25,y:1.55,t:'validate',c:a},{x:3.25,y:3.65,t:'summarize',c:a},{x:6.05,y:1.55,t:'clean.csv',c:C.green},{x:6.05,y:3.65,t:'stats.tsv',c:C.green},{x:9.0,y:2.6,t:'report.pdf',c:C.purple}];
  boxes.forEach(b=>{addShape(s,'roundRect',b.x,b.y,2.3,.9,{line:{color:b.c,width:1.5},fill:{color:b.c,transparency:92}});addText(s,b.t,b.x+.12,b.y+.23,2.06,.34,{fontFace:b.t.includes('.')?MONO:FONT,fontSize:17,bold:true,color:b.c,align:'center'});});
  arrow(s,2.95,3.05,3.25,2.0,C.muted,2);arrow(s,2.95,3.05,3.25,4.1,C.muted,2);arrow(s,5.55,2.0,6.05,2.0,C.muted,2);arrow(s,5.55,4.1,6.05,4.1,C.muted,2);arrow(s,8.35,2.0,9.0,3.05,C.muted,2);arrow(s,8.35,4.1,9.0,3.05,C.muted,2);
  pill(s,'snakemake -n',5.15,5.55,2.95,a);
 }},
 {title:'6. Snakemake and Slurm have different jobs',subtitle:'The workflow controller plans; Slurm allocates compute resources',notes:`Snakemake and Slurm solve different problems. Snakemake understands scientific dependencies and decides which rule is ready. The Slurm executor translates each ready rule into a cluster job with requested CPUs, memory, runtime, and other resources. The lightweight Snakemake controller can run in a tmux session on the submission host. The expensive commands run on compute nodes. This separation lets a workflow execute many independent samples in parallel without manually submitting hundreds of jobs. Resource values should be declared per rule and refined using measurements rather than copied blindly.`,draw:(s,a)=>{
  card(s,.75,1.5,3.35,3.95,'Snakemake controller','• Reads the DAG\n• Selects ready rules\n• Tracks files\n• Submits jobs\n• Retries only by policy',a,{fontSize:17});
  card(s,4.98,1.5,3.35,3.95,'Slurm','• Queues jobs\n• Allocates nodes\n• Enforces resources\n• Records states\n• Returns exit status',C.coral,{fontSize:17});
  card(s,9.21,1.5,3.35,3.95,'Compute nodes','• Run R, Python, aligners\n• Use CPU, RAM, GPU\n• Read and write data\n• Produce logs and outputs',C.green,{fontSize:17});
  arrow(s,4.1,3.45,4.98,3.45,C.coral,3);arrow(s,8.33,3.45,9.21,3.45,C.coral,3);
  addText(s,'tmux protects the controller; Slurm protects the cluster.',3.35,5.95,6.65,.36,{fontSize:18,bold:true,color:C.navy,align:'center'});
 }},
 {title:'7. A minimal statistical workflow',subtitle:'Validate → summarize → test → plot',notes:`A statistical workflow starts with input validation. Check column names, data types, missing values, group labels, and expected sample identifiers before calculating anything. The demonstration dataset contains synthetic measurements from two groups. One rule validates and cleans the table. Another calculates group counts, means, and variability. A third performs a Welch t test and records the effect estimate and uncertainty rather than reporting only a p value. A final rule creates a figure. The workflow is pedagogical; the correct statistical model for a real biomedical study depends on design, pairing, repeated measures, batch effects, confounders, and pre-specified hypotheses.`,draw:(s,a)=>{
  const stages=[['Validate','schema\nmissingness'],['Summarize','n · mean · SD'],['Model','effect\nuncertainty'],['Visualize','distribution\nand context']];
  stages.forEach((st,i)=>{const x=.72+i*3.15;card(s,x,1.55,2.78,3.25,st[0],st[1],i===2?C.purple:a,{fontSize:19});if(i<3)arrow(s,x+2.78,3.17,x+3.12,3.17,C.muted,2);});
  addShape(s,'roundRect',1.25,5.35,10.85,.76,{line:{color:C.coral,transparency:100},fill:{color:C.coral,transparency:93}});
  addText(s,'Workflow reproducibility does not replace appropriate study design or statistical review.',1.55,5.55,10.25,.35,{fontSize:17,bold:true,color:C.coral,align:'center'});
 }},
 {title:'8. DNA workflows add domain-specific file types',subtitle:'FASTQ, references, BAM/CRAM, VCF, and quality reports',notes:`DNA sequence analysis introduces file formats with different purposes. FASTQ stores reads and quality values and is normally kept compressed. A reference FASTA stores sequences. BAM or CRAM stores aligned reads in a binary, indexable format. VCF stores sequence variants and may use block compression with an index. Quality reports summarize technical characteristics but do not automatically establish biological validity. A typical small workflow validates read files, performs quality control, aligns or classifies reads, creates indexed outputs, and summarizes results. Real clinical or research pipelines require validated references, contamination controls, sample identity checks, and documented versions.`,draw:(s,a)=>{
  const files=[['FASTQ.gz','compressed reads'],['FASTA','reference'],['BAM / CRAM','aligned reads'],['VCF.gz','variants'],['HTML / TSV','QC + summary']];
  files.forEach((f,i)=>{const x=.52+i*2.55;card(s,x,1.62,2.25,2.5,f[0],f[1],i===0?C.coral:(i===4?C.green:a),{fontSize:15});if(i<4)arrow(s,x+2.25,2.87,x+2.54,2.87,C.muted,2);});
  addText(s,'Keep compressed, indexed, provenance-rich formats when the toolchain supports them.',1.45,5.15,10.4,.46,{fontSize:20,bold:true,color:C.navy,align:'center'});
  pill(s,'synthetic training data only',4.78,5.92,3.8,C.coral);
 }},
 {title:'9. Dry runs, targets, logs, and benchmarks',subtitle:'Know what will run and preserve what happened',notes:`Before a substantial run, request a specific target and perform a Snakemake dry run. Inspect the planned rules, inputs, and job count. Then execute through the RCC-supported Slurm profile. Each rule should have a useful log, and performance-sensitive rules should have a benchmark file. A completed workflow is not automatically a correct workflow. Review exit states, expected file counts, quality metrics, and biological plausibility. Avoid redirecting all commands into one giant log. Per-rule and per-sample logs make failures diagnosable and support audit trails.`,draw:(s,a)=>{
  const checks=[['Plan','snakemake -n'],['Visualize','DAG / summary'],['Execute','Slurm profile'],['Observe','logs + benchmarks'],['Validate','scientific checks']];
  checks.forEach((c,i)=>{const x=.52+i*2.55;addShape(s,'ellipse',x+0.73,1.5,.78,.78,{line:{color:i===4?C.green:a,transparency:100},fill:{color:i===4?C.green:a}});addText(s,String(i+1),x+.73,1.69,.78,.34,{fontSize:18,bold:true,color:C.white,align:'center'});card(s,x,2.65,2.25,2.45,c[0],c[1],i===4?C.green:a,{fontSize:15});if(i<4)arrow(s,x+1.5,1.89,x+3.08,1.89,C.muted,2);});
  addText(s,'Success = correct files + correct states + plausible scientific content',2.0,5.7,9.3,.38,{fontSize:19,bold:true,color:C.navy,align:'center'});
 }},
 {title:'10. Git records changes - not sensitive data',subtitle:'Version workflow logic, configuration, and documentation',notes:`Git records changes to text files and supports review through branches and pull requests. Commit the Snakefile, scripts, environment definitions, configuration templates, and documentation. Do not commit raw sequencing data, patient identifiers, credentials, private keys, large binary outputs, or secrets. Use a gitignore file to exclude generated directories and local configuration. Small, descriptive commits make it possible to understand how a method evolved. Tag or record the exact workflow version used for an analysis. For collaborative projects, a pull request allows a colleague to review scientific logic and operational safety before changes reach the main branch.`,draw:(s,a)=>{
  card(s,.75,1.45,5.7,4.7,'COMMIT','✓ Snakefile and rules\n✓ scripts\n✓ environment definitions\n✓ configuration templates\n✓ README and methods notes\n✓ small synthetic test data',C.green,{fontSize:18,fill:'F7FCF9'});
  card(s,6.88,1.45,5.7,4.7,'DO NOT COMMIT','✗ patient identifiers\n✗ private SSH keys or tokens\n✗ raw biomedical data\n✗ large generated results\n✗ passwords and secrets\n✗ unapproved reference data',C.red,{fontSize:18,fill:'FFF9F8'});
 }},
 {title:'11. Part Two completion checklist',subtitle:'A reproducible small workflow before scaling up',notes:`You are ready for larger examples when the project has a clear directory structure and read-only source data; the software environment is declared; Snakemake can perform a dry run; the workflow submits rules through the approved Slurm profile; statistical inputs are validated; sequence files use appropriate compressed and indexed formats; logs and benchmarks are generated; and workflow changes are recorded in Git without sensitive data. The next lesson focuses on performance. It explains why an analysis with correct code can still take months when CPU, memory, and especially input-output behavior are structured poorly.`,draw:(s,a)=>{
  const items=['Project structure is explicit','Raw inputs are read-only','Software is declared','Dry run is understood','Rules request Slurm resources','Statistics begin with validation','Sequence formats are appropriate','Logs and benchmarks exist','Git excludes sensitive data'];
  items.forEach((it,i)=>{const col=i%3,row=Math.floor(i/3);const x=.65+col*4.2,y=1.45+row*1.35;addShape(s,'ellipse',x,y,.4,.4,{line:{color:C.green,transparency:100},fill:{color:C.green}});addText(s,'✓',x,y+.02,.4,.30,{fontSize:14,bold:true,color:C.white,align:'center'});addText(s,it,x+.57,y-.03,3.35,.55,{fontSize:16.5,bold:true,color:C.navy});});
  addShape(s,'roundRect',1.7,5.85,9.9,.62,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Next: CPU, GPU, RAM, storage, I/O, and bottleneck diagnosis.',1.95,5.99,9.4,.32,{fontSize:17,bold:true,color:a,align:'center'});
 }}
];

const deck3={part:3,accent:C.coral,title:'Performance and efficient I/O',subtitle:'Match CPU, GPU, memory, storage, and data movement to the scientific workload.',outcome:'Outcome: diagnose the limiting resource and structure workflows so hours do not become months.',notes:`Part Three explains performance engineering for biomedical research. The most important message is that faster hardware does not rescue a poorly structured workflow. A computation that should finish in hours can extend to weeks or months when it repeatedly scans network storage, opens millions of small files, requests the wrong number of threads, or runs out of memory and restarts. We will separate CPU, GPU, RAM, disk capacity, and input-output behavior. We will also explain streaming versus random access, large versus small files, compression, node-local scratch, and the tools used to find a bottleneck. The goal is not maximum speed at any cost. The goal is predictable, fair, and scientifically correct performance.`};
const slides3=[
 {title:'1. Performance is a systems property',subtitle:'The slowest required resource limits the whole workflow',notes:`Performance is not a single number. An analysis may be limited by CPU instructions, GPU kernels, memory capacity, memory bandwidth, network transfer, storage throughput, storage latency, or metadata operations. Improving a resource that is not limiting usually changes little. For example, adding CPU cores to a job that waits for thousands of small files can increase contention without shortening runtime. Start by describing the data path and measuring where elapsed time is spent. Then change one variable at a time. This approach is more reliable than guessing from the reputation of a tool or copying a resource request from another project.`,draw:(s,a)=>{
  const resources=[['CPU','computation'],['GPU','parallel kernels'],['RAM','working set'],['Storage','capacity'],['I/O','data movement']];
  resources.forEach((r,i)=>{const x=.52+i*2.55;card(s,x,1.55,2.25,2.6,r[0],r[1],i===4?a:C.blue,{fontSize:16});if(i<4)arrow(s,x+2.25,2.85,x+2.54,2.85,C.line,1.5);});
  addShape(s,'roundRect',1.25,4.75,10.85,1.0,{line:{color:a,transparency:100},fill:{color:a,transparency:93}});
  addText(s,'Elapsed time is constrained by the bottleneck - not by the most impressive hardware.',1.6,5.02,10.15,.42,{fontSize:20,bold:true,color:a,align:'center'});
 }},
 {title:'2. The same analysis can take hours or months',subtitle:'Repeated inefficient work multiplies across samples and workflow steps',notes:`Consider a workflow with five thousand samples. If a step spends one second on useful computation and twenty seconds opening, seeking, and closing small files on shared storage, the overhead dominates. Repeat that pattern across many rules and retries, and a nominally short analysis can occupy the system for weeks. Another common pattern is decompressing the same source repeatedly, copying entire directories for each rule, or requesting one core for software configured to use sixteen. Performance mistakes multiply by the number of samples, files, and workflow stages. Estimate scale before launch: number of jobs, files per job, bytes read and written, and expected runtime per unit.`,draw:(s,a)=>{
  card(s,.75,1.45,5.65,4.6,'WELL STRUCTURED','Sequential reads\nCompressed inputs\nNode-local temporary work\nMeasured threads and RAM\nOne pass per transformation\n\nIllustrative runtime: hours',C.green,{fontSize:18,fill:'F7FCF9'});
  card(s,6.93,1.45,5.65,4.6,'POORLY STRUCTURED','Random network I/O\nMillions of tiny files\nRepeated decompression\nOversubscribed threads\nFrequent restart or swapping\n\nIllustrative runtime: weeks to months',C.red,{fontSize:18,fill:'FFF9F8'});
  arrow(s,6.35,3.72,6.93,3.72,a,3);
 }},
 {title:'3. CPU: cores, threads, and parallel efficiency',subtitle:'More requested cores help only when the software can use them',notes:`A CPU node contains cores that execute instruction streams. Some tools expose a threads option. Slurm must allocate at least that many CPUs per task, and the command must be told to use them. Parallel efficiency usually declines as thread count increases because threads coordinate, share memory bandwidth, and wait for input. Two independent samples may run faster as two smaller jobs than as one very wide job. Measure elapsed time and CPU utilization at several thread counts using representative data. Never start many background processes outside the allocation, and do not assume that a tool called multithreaded scales linearly.`,draw:(s,a)=>{
  const bars=[{n:1,t:100},{n:2,t:58},{n:4,t:36},{n:8,t:29},{n:16,t:27}];
  addText(s,'Illustrative runtime',.85,1.35,3.0,.35,{fontSize:17,bold:true,color:C.navy});
  bars.forEach((b,i)=>{const y=1.95+i*.78;addText(s,`${b.n} thread${b.n>1?'s':''}`,.85,y,1.25,.3,{fontSize:14,color:C.muted});addShape(s,'rect',2.2,y,6.4*(b.t/100),.38,{line:{color:a,transparency:100},fill:{color:a}});addText(s,`${b.t} min`,8.8,y,1.1,.3,{fontSize:14,bold:true,color:C.ink});});
  card(s,9.8,1.45,2.75,3.85,'Measure','• elapsed time\n• CPU efficiency\n• memory use\n• I/O wait\n\nChoose the smallest efficient allocation.',C.blue,{fontSize:15});
  addText(s,'Doubling cores rarely halves runtime.',3.45,6.15,6.5,.38,{fontSize:20,bold:true,color:a,align:'center'});
 }},
 {title:'4. GPU: powerful, specialized, and easy to underuse',subtitle:'A GPU helps only when the application and data path are GPU-aware',notes:`GPUs contain many execution units optimized for highly parallel numerical work. They can accelerate deep learning, image analysis, molecular simulation, and selected sequence-analysis tools. A CPU program does not become GPU-enabled merely because a GPU is allocated. Request the correct GPU resource, use software built for the available driver and libraries, and monitor utilization with nvidia-smi. Low utilization may indicate tiny batches, CPU preprocessing, slow data loading, insufficient parallelism, or frequent host-to-device transfers. GPUs are scarce shared resources, so release them when the GPU portion is complete rather than reserving one during long CPU-only stages.`,draw:(s,a)=>{
  card(s,.7,1.45,3.45,4.65,'GOOD GPU FIT','Large matrix operations\nDeep-learning training or inference\nGPU-enabled image processing\nGPU-aware simulation\nSufficient batch size',C.green,{fontSize:17});
  card(s,4.94,1.45,3.45,4.65,'COMMON BOTTLENECK','CPU preprocessing\nSmall batches\nSlow file loading\nFrequent transfers\nUnsupported software build',a,{fontSize:17});
  card(s,9.18,1.45,3.45,4.65,'OBSERVE','nvidia-smi\nGPU utilization\nGPU memory\nPower state\nCPU and I/O at the same time',C.blue,{fontSize:17});
 }},
 {title:'5. RAM: capacity is not the same as speed',subtitle:'Request enough for the working set, but avoid waste',notes:`RAM holds the active working set: data structures, indices, buffers, and program state. If a job exceeds its Slurm memory allocation, the job may be terminated. If the operating system begins swapping, performance can collapse because disk is far slower than RAM. Requesting far more memory than needed can delay scheduling and reduce capacity for everyone. Use Slurm accounting to inspect maximum resident memory after representative jobs. Some tools scale memory with threads or input size, so record the relationship. A memory leak shows steadily rising use; a normal workload often rises to a plateau.`,draw:(s,a)=>{
  const vals=[['Too little','OOM kill or restart',C.red],['Right-sized','stable working set',C.green],['Too much','longer queue, wasted capacity',C.amber]];
  vals.forEach((v,i)=>card(s,.75+i*4.23,1.45,3.75,3.55,v[0],v[1],v[2],{fontSize:18}));
  addShape(s,'roundRect',1.35,5.45,10.65,.72,{line:{color:C.blue,transparency:100},fill:{color:C.blue,transparency:93}});
  addText(s,'Use sacct MaxRSS and representative benchmarks to size memory requests.',1.7,5.63,9.95,.34,{fontFace:MONO,fontSize:17,bold:true,color:C.blue,align:'center'});
 }},
 {title:'6. Disk space and I/O are different questions',subtitle:'Capacity asks “how much?”; I/O asks “how fast and in what pattern?”',notes:`Disk space is capacity. Input-output performance describes how data moves. Four useful dimensions are throughput, latency, input-output operations per second, and metadata rate. Throughput matters for large sequential reads such as scanning a compressed FASTQ. Latency matters when a program waits for individual operations. IOPS matters for many small reads and writes. Metadata rate matters when listing directories, checking file existence, opening files, or creating thousands of paths. Network storage is designed for shared durable data, but it cannot provide local-disk behavior to every job simultaneously. Match the access pattern to the storage tier.`,draw:(s,a)=>{
  const metrics=[['Capacity','GB / TB','How much can be stored?'],['Throughput','MB/s or GB/s','How quickly do long streams move?'],['Latency + IOPS','ms + ops/s','How costly are small random operations?'],['Metadata','creates / stats / lists','How many paths are being managed?']];
  metrics.forEach((m,i)=>card(s,.65+i*3.15,1.45,2.78,3.95,m[0],`${m[1]}\n\n${m[2]}`,i===2?a:C.blue,{fontSize:16}));
  addText(s,'A storage system can have plenty of free space and still be the bottleneck.',2.05,5.85,9.25,.38,{fontSize:19,bold:true,color:C.navy,align:'center'});
 }},
 {title:'7. Streaming versus random I/O',subtitle:'Long sequential reads are efficient; tiny scattered accesses are expensive',notes:`Streaming input-output reads or writes long contiguous sequences. This lets storage, operating-system caches, compression libraries, and network protocols work efficiently. Random input-output jumps among many positions or files and repeatedly pays seek, latency, and metadata costs. Indexed BAM and VCF access can be appropriate when querying a small genomic interval, but repeatedly issuing tiny queries across the entire genome can be slower than one sequential pass. Against network storage, avoid database-like random write patterns and large collections of temporary shards. Stage active files to node-local disk, process them there, and return only the required outputs.`,draw:(s,a)=>{
  card(s,.75,1.45,5.65,4.45,'STREAMING I/O','████████████████████\n\nOne long read or write\nHigh throughput\nEfficient prefetch and compression\nGood fit for FASTQ scans and large outputs',C.green,{fontFace:MONO,fontSize:17,fill:'F7FCF9'});
  card(s,6.93,1.45,5.65,4.45,'RANDOM / SMALL I/O','█  █   █ █    █  █\n↕  ↕   ↕ ↕    ↕  ↕\nMany seeks, opens, stats, and closes\nLatency and metadata dominate\nPoor fit for network temporary work',C.red,{fontFace:MONO,fontSize:17,fill:'FFF9F8'});
 }},
 {title:'8. Large files, small files, and crowded directories',subtitle:'File count can be more expensive than byte count',notes:`A directory with hundreds of thousands of files can make listing, tab completion, backups, workflow discovery, and deletion painfully slow. Small files also waste storage blocks and require metadata operations. Many bioinformatics tools create temporary fragments, per-read outputs, or tiny environment files. Prefer a reasonable directory hierarchy, one result bundle per sample or batch, and archive cold collections when appropriate. Do not use tar archives as a substitute for formats that need random indexed access, but do use structured containers or archives for collections that are transferred and consumed together. Clean temporary files through workflow rules instead of leaving them indefinitely.`,draw:(s,a)=>{
  addShape(s,'roundRect',.65,1.45,5.9,4.75,{line:{color:C.red,width:1.2},fill:{color:'FFF9F8'}});
  addText(s,'CROWDED DIRECTORY',1.0,1.75,5.2,.35,{fontSize:20,bold:true,color:C.red,align:'center'});
  for(let r=0;r<7;r++) for(let c=0;c<12;c++) addShape(s,'rect',1.0+c*.39,2.35+r*.37,.22,.18,{line:{color:C.red,transparency:50,width:.5},fill:{color:C.red,transparency:55}});
  addText(s,'100,000 paths → metadata bottleneck',1.35,5.38,4.5,.35,{fontSize:16,bold:true,color:C.red,align:'center'});
  addShape(s,'roundRect',6.85,1.45,5.9,4.75,{line:{color:C.green,width:1.2},fill:{color:'F7FCF9'}});
  addText(s,'STRUCTURED HIERARCHY',7.2,1.75,5.2,.35,{fontSize:20,bold:true,color:C.green,align:'center'});
  addText(s,'project/\n  batch_001/\n    sample_001/\n    sample_002/\n  batch_002/\n  archives/\n  manifests/',7.8,2.45,4.1,2.85,{fontFace:MONO,fontSize:19,color:C.ink,valign:'top'});
 }},
 {title:'9. Leave files compressed when the toolchain supports it',subtitle:'Compression reduces storage and I/O - decompression costs CPU',notes:`Biomedical data is often compressible. FASTQ is commonly stored as gzip-compressed FASTQ. VCF can use block gzip with an index. BAM and CRAM are compressed binary alignment formats. Keeping files compressed reduces bytes transferred and stored, which often saves more time than decompression costs. Avoid repeatedly expanding a file to network storage merely because one command expects a path. Many tools read compressed input directly, and Unix pipes can stream decompressed data between compatible tools. Confirm that the chosen compression is splittable or indexable when parallel access is required. Keep the original compressed source and generate only formats needed for downstream analysis.`,draw:(s,a)=>{
  const flows=[['FASTQ.gz','smaller transfer'],['tool reads gzip','CPU decompression'],['stream / pipe','no intermediate'],['BAM / report','required output']];
  flows.forEach((f,i)=>{const x=.65+i*3.15;card(s,x,1.7,2.78,2.75,f[0],f[1],i===0?C.coral:(i===2?C.green:a),{fontSize:16});if(i<3)arrow(s,x+2.78,3.08,x+3.12,3.08,C.muted,2);});
  addShape(s,'roundRect',1.35,5.08,10.65,.82,{line:{color:C.green,transparency:100},fill:{color:C.green,transparency:92}});
  addText(s,'Move fewer bytes. Avoid unnecessary expanded intermediates. Preserve indexable formats.',1.7,5.30,9.95,.38,{fontSize:18,bold:true,color:C.green,align:'center'});
 }},
 {title:'10. Use node-local scratch through Snakemake',subtitle:'Stage active inputs locally, compute locally, return required outputs',notes:`Node-local scratch is temporary storage attached to the compute node. It provides lower latency and avoids making shared storage handle every temporary read and write. Snakemake can expose the job temporary directory through the standard tmpdir resource. Shadow rules can execute in an isolated directory, with modes that link or copy the required inputs. For tools that perform random access or create many temporary files, use an RCC-tested pattern: copy the required inputs to local scratch, run the command there, validate the output, and copy only final results back. Scratch is temporary, so the workflow must not treat it as durable storage.`,draw:(s,a)=>{
  const stages=[['Shared input','durable\ncompressed'],['Stage','copy selected\ninputs'],['Local scratch','random I/O +\ntemporary files'],['Validate','exit status +\nexpected output'],['Return','final outputs\nto shared storage']];
  stages.forEach((st,i)=>{const x=.52+i*2.55;card(s,x,1.52,2.25,3.25,st[0],st[1],i===2?a:(i===4?C.green:C.blue),{fontSize:16});if(i<4)arrow(s,x+2.25,3.15,x+2.54,3.15,C.muted,2);});
  addText(s,'Shared storage is for durable data; scratch is for active temporary work.',2.05,5.35,9.2,.38,{fontSize:19,bold:true,color:C.navy,align:'center'});
 }},
 {title:'11. Measure the bottleneck with the right tools',subtitle:'Observe job accounting, processes, disks, and GPUs together',notes:`Use Slurm accounting first. S acct shows job state, elapsed time, allocated CPUs, and fields such as maximum resident memory. S stat reports live statistics for running jobs. Inside an allocation, time measures elapsed and CPU time, top or h top shows processes, and tools such as pidstat, vmstat, iostat, or dstat can reveal CPU wait, memory pressure, and storage activity when available. N v i d i a s m i reports GPU utilization and memory. Snakemake benchmark files connect measurements to specific rules. Interpret metrics together: low CPU plus high I/O wait suggests storage; full memory and rising swap suggests RAM; low GPU utilization with busy CPUs suggests preprocessing or data loading.`,draw:(s,a)=>{
  const rows=[['sacct','after job','state, elapsed, MaxRSS, allocation'],['sstat','during job','live CPU and memory statistics'],['time / pidstat','inside job','CPU time and process behavior'],['iostat / vmstat','inside job','I/O wait, devices, memory pressure'],['nvidia-smi','GPU job','GPU use, memory, processes'],['Snakemake benchmark','per rule','repeatable rule-level evidence']];
  const y0=1.35; rows.forEach((r,i)=>{const y=y0+i*.78;addShape(s,'roundRect',.68,y,12.0,.61,{line:{color:i%2?C.line:'E5EBF0',width:1},fill:{color:i%2?'FAFBFC':'F3F6F8'}});addText(s,r[0],.9,y+.12,2.3,.32,{fontFace:MONO,fontSize:15,bold:true,color:a});addText(s,r[1],3.35,y+.12,1.65,.32,{fontSize:14,color:C.muted});addText(s,r[2],5.1,y+.12,7.2,.32,{fontSize:15,color:C.ink});});
 }},
 {title:'12. A bottleneck diagnosis matrix',subtitle:'Use symptoms to choose the next measurement',notes:`A symptom is not a diagnosis. Low CPU efficiency may be caused by input-output wait, serial code, thread oversubscription, or frequent synchronization. A job killed for memory needs either a larger allocation or a method that reduces the working set. A GPU at ten percent utilization may be waiting on CPU preprocessing or tiny batches. A workflow that pauses while discovering files may have a metadata problem. Build a small representative benchmark, change one factor, and compare elapsed time and resource efficiency. Stop when performance is adequate and fair; optimization also has engineering cost and can introduce scientific errors.`,draw:(s,a)=>{
  const heads=['Symptom','Likely candidates','Next evidence']; const col=[.65,3.55,8.25], widths=[2.65,4.45,4.43];
  heads.forEach((h,i)=>{addShape(s,'rect',col[i],1.35,widths[i],.62,{line:{color:a,transparency:100},fill:{color:a}});addText(s,h,col[i]+.12,1.50,widths[i]-.24,.32,{fontSize:16,bold:true,color:C.white});});
  const data=[['Low CPU efficiency','I/O wait · serial region · too many threads','sstat, pidstat, iostat'],['OOM / killed','working set too large · leak','sacct MaxRSS, time series'],['Low GPU use','CPU preprocessing · small batch · I/O','nvidia-smi plus CPU/I/O'],['Long startup','many files · environment metadata','file counts, strace if supported'],['Fast compute, slow end','large output · compression · network write','bytes written, throughput']];
  data.forEach((r,j)=>{r.forEach((v,i)=>{const y=1.97+j*.82;addShape(s,'rect',col[i],y,widths[i],.82,{line:{color:C.line,width:1},fill:{color:j%2?'FAFBFC':'FFFFFF'}});addText(s,v,col[i]+.12,y+.10,widths[i]-.24,.59,{fontSize:i===0?14.5:14,color:i===0?C.navy:C.ink,bold:i===0,valign:'mid'});});});
 }},
 {title:'13. Part Three operating rules',subtitle:'Efficient, measurable, and considerate use of shared resources',notes:`The operating rules are straightforward. Measure before scaling. Match Slurm requests to the software configuration. Keep source data compressed where possible. Prefer sequential streaming access. Avoid random temporary input-output on network storage. Stage active files to node-local scratch through a tested Snakemake pattern. Reduce small-file and directory counts. Preserve only necessary outputs and clean temporary files. Use Slurm accounting, Snakemake benchmarks, and operating-system tools to identify the actual bottleneck. Above all, perform a pilot at realistic scale. An inefficient workflow multiplied across thousands of samples can turn hours into months and degrade the shared service for colleagues.`,draw:(s,a)=>{
  const items=['Measure a representative pilot','Align threads with allocated CPUs','Right-size memory from MaxRSS','Use GPUs only for GPU-enabled stages','Keep source files compressed','Prefer streaming over random I/O','Use local scratch for active temporary work','Control file and directory counts','Benchmark rules before full-scale launch'];
  items.forEach((it,i)=>{const col=i%3,row=Math.floor(i/3);const x=.55+col*4.25,y=1.35+row*1.35;addShape(s,'ellipse',x,y,.42,.42,{line:{color:C.green,transparency:100},fill:{color:C.green}});addText(s,'✓',x,y+.03,.42,.30,{fontSize:14,bold:true,color:C.white,align:'center'});addText(s,it,x+.58,y-.04,3.48,.58,{fontSize:16.2,bold:true,color:C.navy});});
  addShape(s,'roundRect',1.25,5.73,10.85,.77,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Bad structure scales into bad runtime: hours can become months.',1.6,5.94,10.15,.36,{fontSize:19,bold:true,color:a,align:'center'});
 }}
];

const deck4={part:4,accent:C.purple,title:'Containers with Apptainer',subtitle:'Package software reproducibly while keeping network storage out of the small-file hot path.',outcome:'Outcome: run trusted Apptainer images manually and from Snakemake with deliberate binds, cache, scratch, and provenance.',notes:`Part Four introduces containers using Apptainer. Containers package an application and its libraries into a portable image. On RCC, the operational reason is especially important: a large Conda environment contains thousands of small files. If those files are repeatedly opened from network storage by many jobs, metadata and random input-output can dominate runtime. A read-only Apptainer S I F image consolidates that software stack into one managed artifact and is suitable for shared high-performance computing. We will distinguish the image from project data, explain cache and temporary storage, cover bind mounts and GPU access, and show how Snakemake associates a container with a rule.`};
const slides4=[
 {title:'1. The problem: software can become an I/O workload',subtitle:'Conda environments contain many small files and metadata operations',notes:`A Conda environment can contain tens of thousands of files: Python modules, shared libraries, metadata records, executables, and package caches. Starting a command may trigger many opens, stats, library searches, and imports before useful computation begins. On local solid-state storage this may be acceptable. On shared network storage, hundreds of simultaneous jobs can turn environment startup into a metadata bottleneck. The result may look like slow software even though the CPU is mostly waiting. Containers address this by packaging the software stack into a smaller number of image artifacts and by making the environment immutable and reproducible.`,draw:(s,a)=>{
  addShape(s,'roundRect',.65,1.4,5.9,4.9,{line:{color:C.red,width:1.2},fill:{color:'FFF9F8'}});
  addText(s,'NETWORK CONDA ENVIRONMENT',1.0,1.72,5.2,.4,{fontSize:20,bold:true,color:C.red,align:'center'});
  for(let r=0;r<8;r++) for(let c=0;c<13;c++) addShape(s,'rect',1.0+c*.37,2.35+r*.34,.18,.15,{line:{color:C.red,transparency:70,width:.4},fill:{color:C.red,transparency:50}});
  addText(s,'many small opens · stats · imports',1.35,5.45,4.5,.36,{fontSize:16,bold:true,color:C.red,align:'center'});
  addShape(s,'roundRect',6.85,1.4,5.9,4.9,{line:{color:a,width:1.2},fill:{color:'F9F7FC'}});
  addText(s,'APPTAINER SIF IMAGE',7.2,1.72,5.2,.4,{fontSize:20,bold:true,color:a,align:'center'});
  addShape(s,'roundRect',8.2,2.55,3.9,2.1,{line:{color:a,width:2},fill:{color:a,transparency:88}});addText(s,'analysis.sif\nread-only software image',8.5,3.02,3.3,1.0,{fontFace:MONO,fontSize:20,bold:true,color:a,align:'center'});
  addText(s,'one managed artifact · predictable runtime stack',7.55,5.45,4.5,.36,{fontSize:16,bold:true,color:a,align:'center'});
 }},
 {title:'2. What a container is - and is not',subtitle:'A packaged user space, not a virtual machine and not a data store',notes:`A container image packages user-space software, libraries, and selected configuration. It does not include a separate hardware machine and normally shares the host Linux kernel. Apptainer is designed for multi-user high-performance computing and runs processes with the user identity rather than a privileged daemon model. The image is not the correct place for active project data, credentials, or patient information. Project inputs and outputs remain in approved storage and are made visible through explicit bind mounts. Containers improve reproducibility of software, but they do not validate algorithms, reference data, parameters, or scientific interpretation.`,draw:(s,a)=>{
  card(s,.7,1.45,3.65,4.75,'CONTAINER INCLUDES','Application\nRuntime\nLibraries\nCommand-line tools\nSelected static configuration',a,{fontSize:18});
  card(s,4.85,1.45,3.65,4.75,'HOST PROVIDES','Linux kernel\nCPU and GPU devices\nSlurm allocation\nFilesystems\nUser identity',C.blue,{fontSize:18});
  card(s,9.0,1.45,3.65,4.75,'KEEP OUTSIDE','Research data\nSecrets and credentials\nWritable results\nTemporary scratch\nSite-specific policy',C.coral,{fontSize:18});
 }},
 {title:'3. SIF: an immutable image artifact',subtitle:'A read-only image is easier to distribute, verify, and share',notes:`Apptainer commonly uses the Singularity Image Format, or S I F. A SIF image can contain a compressed read-only filesystem plus metadata and signatures. Read-only images reduce accidental drift: a job cannot silently install a different library into the image. The same image can be used by many jobs. Record the image source, digest or checksum, creation recipe, and validation status. Do not rely only on a floating tag such as latest. A container is a versioned research dependency and should be managed with the same care as a reference genome or analysis script.`,draw:(s,a)=>{
  addShape(s,'roundRect',1.05,1.35,4.15,4.85,{line:{color:a,width:1.5},fill:{color:a,transparency:91}});
  addText(s,'analysis.sif',1.55,1.78,3.15,.52,{fontFace:MONO,fontSize:25,bold:true,color:a,align:'center'});
  const layers=['application','runtime','libraries','metadata / signature'];layers.forEach((l,i)=>{addShape(s,'roundRect',1.55,2.65+i*.72,3.15,.52,{line:{color:a,transparency:45,width:.8},fill:{color:C.white,transparency:8}});addText(s,l,1.72,2.76+i*.72,2.82,.27,{fontSize:15,bold:true,color:C.navy,align:'center'});});
  card(s,5.75,1.35,6.55,1.35,'Immutable','The software stack does not drift during the analysis.',C.green,{fontSize:16});
  card(s,5.75,3.02,6.55,1.35,'Verifiable','Record checksum, source registry, and build recipe.',C.blue,{fontSize:16});
  card(s,5.75,4.69,6.55,1.35,'Shareable','Many jobs can use the same approved image artifact.',a,{fontSize:16});
 }},
 {title:'4. Image, cache, temporary space, and project data',subtitle:'Four locations with four different lifecycles',notes:`Container workflows involve several storage locations. The SIF image is a durable, versioned software artifact. The Apptainer cache stores downloaded layers and should use an RCC-approved path; uncontrolled caches on a shared home directory can consume space and create metadata traffic. Temporary build or extraction space should use local scratch when possible. Project data remains in approved shared storage and is bound into the container. Distinguishing these locations prevents accidental data loss and avoids turning network storage into a scratch disk. The RCC should publish standard environment variables and paths for image stores, caches, and temporary directories.`,draw:(s,a)=>{
  const items=[['SIF image','durable + versioned','project software store'],['Cache','reusable downloads','approved cache path'],['TMPDIR','ephemeral work','node-local scratch'],['Project data','durable research data','approved shared storage']];
  items.forEach((it,i)=>{const x=.65+i*3.15;card(s,x,1.45,2.78,4.25,it[0],`${it[1]}\n\n${it[2]}`,i===2?C.coral:(i===3?C.green:a),{fontSize:17});});
  addText(s,'Do not treat any one location as suitable for every purpose.',2.35,6.05,8.65,.38,{fontSize:19,bold:true,color:C.navy,align:'center'});
 }},
 {title:'5. Trust the image deliberately',subtitle:'Pin versions, record digests, and validate the scientific contents',notes:`Only run images from trusted sources or images built from reviewed definitions. Prefer immutable digests over floating tags. Calculate and record a checksum for a SIF image when it is transferred. Inspect image metadata and labels. Record the base image, installed package versions, build date, and definition file. Scan or review images according to institutional policy. Most importantly, validate the scientific behavior with synthetic and reference data. A correctly signed image can still contain an unsuitable algorithm, outdated database, or incorrect default parameter. Trust has both a software-supply-chain component and a scientific-validation component.`,draw:(s,a)=>{
  const steps=[['Source','trusted registry or reviewed build'],['Pin','version + digest'],['Inspect','labels + recipe + packages'],['Test','synthetic and reference data'],['Approve','documented scientific use']];
  steps.forEach((st,i)=>{const x=.52+i*2.55;addShape(s,'ellipse',x+.73,1.35,.78,.78,{line:{color:i===4?C.green:a,transparency:100},fill:{color:i===4?C.green:a}});addText(s,String(i+1),x+.73,1.54,.78,.34,{fontSize:18,bold:true,color:C.white,align:'center'});card(s,x,2.52,2.25,2.75,st[0],st[1],i===4?C.green:a,{fontSize:14.5});if(i<4)arrow(s,x+1.51,1.74,x+3.07,1.74,C.muted,2);});
 }},
 {title:'6. Run an image with explicit commands and a clean environment',subtitle:'Use exec for predictable command invocation',notes:`Apptainer exec runs a command inside an image. Start with a harmless version check, then a small synthetic test. The clean environment option reduces accidental inheritance of host variables that could change behavior. The contain-all or site-recommended isolation options may be appropriate depending on policy. Record the full command in the workflow log. Avoid interactive changes inside writable sandboxes for production work because those changes are difficult to reproduce. If a command depends on locale, threads, temporary paths, or license variables, declare them explicitly and document why they are needed.`,draw:(s,a)=>{
  addShape(s,'roundRect',.75,1.45,7.0,4.65,{line:{color:C.line,width:1},fill:{color:'101820'}});
  addText(s,'apptainer exec --cleanenv \\\n  analysis.sif \\\n  tool --version\n\napptainer exec --cleanenv \\\n  --bind "$PWD/data:/data:ro" \\\n  --bind "$PWD/results:/results" \\\n  analysis.sif \\\n  tool /data/input.fastq.gz \\\n       --out /results/report.tsv',1.08,1.78,6.35,3.95,{fontFace:MONO,fontSize:16,color:'D6F5DD',valign:'top'});
  card(s,8.15,1.45,4.45,1.35,'exec','Run one explicit command.',a,{fontSize:16});
  card(s,8.15,3.05,4.45,1.35,'--cleanenv','Reduce unintended host-variable inheritance.',C.blue,{fontSize:16});
  card(s,8.15,4.65,4.45,1.35,'read-only inputs','Prevent accidental modification of source data.',C.green,{fontSize:16});
 }},
 {title:'7. Bind mounts connect approved data to the container',subtitle:'Expose only the paths the job needs, with clear read/write intent',notes:`A bind mount makes a host path visible at a chosen path inside the container. Bind source data read-only whenever possible. Bind a dedicated result directory read-write. Bind node-local scratch for temporary work. Avoid binding your entire home directory merely for convenience, because that makes hidden configuration and credentials visible and reduces reproducibility. Use stable internal paths such as slash data, slash results, and slash tmp so the command is independent of the host project layout. Verify ownership and permissions before starting thousands of jobs.`,draw:(s,a)=>{
  card(s,.65,1.4,3.25,4.95,'HOST PATHS','/project/data\nread-only\n\n/project/results\nread-write\n\n$TMPDIR\nephemeral',C.blue,{fontFace:MONO,fontSize:17});
  addShape(s,'roundRect',5.08,1.4,3.2,4.95,{line:{color:a,width:1.5},fill:{color:a,transparency:91}});addText(s,'CONTAINER',5.48,1.72,2.4,.4,{fontSize:21,bold:true,color:a,align:'center'});addText(s,'/data\n\n/results\n\n/tmp',5.75,2.45,1.85,2.75,{fontFace:MONO,fontSize:21,bold:true,color:C.navy,align:'center'});
  card(s,9.48,1.4,3.25,4.95,'ACCESS INTENT','inputs cannot change\n\noutputs are deliberate\n\ntemporary I/O stays local\n\nno broad home-directory bind',C.green,{fontSize:17});
  arrow(s,3.9,3.87,5.08,3.87,a,3);arrow(s,8.28,3.87,9.48,3.87,a,3);
 }},
 {title:'8. Containers do not remove I/O physics',subtitle:'The image fixes software packaging; data access still needs good patterns',notes:`A container does not make random network input-output fast. The executable may be packaged efficiently, but inputs, outputs, caches, and temporary files still follow the underlying storage behavior. Keep compressed inputs compressed when supported. Stage files that require random access or many temporary writes to node-local scratch. Avoid writing package caches or application caches into the project directory. Limit the number of tiny output files and organize directories. A container can even make performance worse if every job independently pulls an image from a registry. Pre-stage approved images and use a shared read-only image location or an RCC-supported cache strategy.`,draw:(s,a)=>{
  const layers=[['Container image','software reads','usually efficient artifact'],['Input data','stream or indexed access','keep compressed when possible'],['Temporary work','random / small I/O','node-local scratch'],['Final output','durable write','return only required results']];
  layers.forEach((l,i)=>{const y=1.35+i*1.23;addShape(s,'roundRect',.75,y,12.0,.93,{line:{color:i===2?C.coral:C.line,width:i===2?1.5:1},fill:{color:i===2?'FFF6F3':(i%2?'FAFBFC':'FFFFFF')}});addText(s,l[0],1.0,y+.18,2.45,.35,{fontSize:18,bold:true,color:i===2?C.coral:C.navy});addText(s,l[1],3.65,y+.18,2.55,.35,{fontSize:16,color:C.muted});addText(s,l[2],6.4,y+.18,5.8,.35,{fontSize:17,bold:true,color:C.ink});});
 }},
 {title:'9. GPU access from Apptainer',subtitle:'The container supplies user libraries; the host supplies the device and driver',notes:`For a GPU job, request the GPU through Slurm and run Apptainer with the N V option so the relevant NVIDIA devices and host driver libraries are available inside the container. The image should contain compatible user-space frameworks such as CUDA-enabled PyTorch or TensorFlow, but it should not attempt to replace the host kernel driver. Test compatibility on a small allocation and use nvidia-smi both on the host allocation and, where appropriate, inside the container. Record image digest, GPU type, driver, framework version, and command. GPU access does not change the need to optimize data loading and batch size.`,draw:(s,a)=>{
  card(s,.7,1.45,3.45,4.75,'SLURM','Allocates GPU\nSelects node\nTracks resource\nEnforces time and memory',C.coral,{fontSize:18});
  card(s,4.94,1.45,3.45,4.75,'APPTAINER --nv','Binds devices\nExposes host driver libraries\nRuns container command',a,{fontSize:18});
  card(s,9.18,1.45,3.45,4.75,'IMAGE','GPU-enabled framework\nApplication code\nPinned libraries\nValidated model or method',C.green,{fontSize:18});
  arrow(s,4.15,3.82,4.94,3.82,C.muted,3);arrow(s,8.39,3.82,9.18,3.82,C.muted,3);
 }},
 {title:'10. Snakemake associates images with rules',subtitle:'Software, resources, inputs, and outputs become one executable specification',notes:`Snakemake can associate a container image with a rule and execute the workflow using the Apptainer deployment method. This places the software dependency next to the declared inputs, outputs, threads, resources, log, and command. Use an RCC-supported Apptainer prefix or image store so jobs do not repeatedly download images. The rule should still use tmpdir or a shadow pattern when the tool needs local temporary work. Pin the image to an immutable digest or version and record it in reports. Test both the workflow logic and the image before scaling to production data.`,draw:(s,a)=>{
  addShape(s,'roundRect',.68,1.35,7.0,4.95,{line:{color:C.line,width:1},fill:{color:'101820'}});
  addText(s,'rule align:\n    input:\n        "data/{sample}.fastq.gz"\n    output:\n        "results/{sample}.bam"\n    threads: 8\n    resources:\n        mem_mb=16000,\n        tmpdir="/local/scratch"\n    container:\n        "docker://org/tool@sha256:…"\n    shell:\n        "tool -t {threads} {input} > {output}"',1.02,1.66,6.35,4.38,{fontFace:MONO,fontSize:15,color:'D6F5DD',valign:'top'});
  card(s,8.08,1.35,4.52,1.35,'Rule','scientific dependency',C.blue,{fontSize:16});
  card(s,8.08,2.95,4.52,1.35,'Resources','Slurm allocation + scratch',C.coral,{fontSize:16});
  card(s,8.08,4.55,4.52,1.35,'Container','pinned software artifact',a,{fontSize:16});
 }},
 {title:'11. Build once, test, publish, and reuse',subtitle:'Production images should come from reviewed definitions',notes:`A production image should be built from a version-controlled Apptainer definition file or an equivalent reviewed recipe. Build in an approved environment, because image construction may require privileges or a remote builder. Record base images and package versions. Run automated smoke tests, workflow tests with synthetic data, and scientific validation. Publish the image to an approved registry or image store, record the digest, and make it read-only. Rebuild through the recipe rather than modifying an existing image. Deprecate images that contain security problems or obsolete references, but preserve provenance for completed analyses.`,draw:(s,a)=>{
  const stages=[['Definition','version-controlled recipe'],['Build','approved builder'],['Test','software + scientific'],['Publish','registry or image store'],['Run','pinned digest in workflow']];
  stages.forEach((st,i)=>{const x=.52+i*2.55;card(s,x,1.55,2.25,3.45,st[0],st[1],i===2?C.coral:(i===4?C.green:a),{fontSize:15});if(i<4)arrow(s,x+2.25,3.28,x+2.54,3.28,C.muted,2);});
  addShape(s,'roundRect',1.25,5.45,10.85,.72,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Rebuild from the recipe; do not “repair” production images interactively.',1.6,5.63,10.15,.34,{fontSize:18,bold:true,color:a,align:'center'});
 }},
 {title:'12. Part Four operating rules',subtitle:'Reproducible software without a network-small-file storm',notes:`The container rules are these. Use trusted, immutable SIF images. Record source, digest, build recipe, and validation. Keep project data outside the image. Bind source data read-only, results deliberately, and temporary space to local scratch. Place caches and images in RCC-approved locations. Use clean environments and explicit commands. Request GPUs through Slurm and use the Apptainer GPU option only for compatible images. In Snakemake, pin the container per rule or workflow and avoid repeated pulls. Remember that containers improve software reproducibility and startup I/O, but good data input-output patterns, performance measurement, and scientific validation remain essential.`,draw:(s,a)=>{
  const items=['Prefer immutable SIF images','Pin source and digest','Keep data outside the image','Bind inputs read-only','Put temporary work on local scratch','Use approved image and cache paths','Use --cleanenv and explicit commands','Request GPU through Slurm','Test and validate before scale'];
  items.forEach((it,i)=>{const col=i%3,row=Math.floor(i/3);const x=.55+col*4.25,y=1.35+row*1.35;addShape(s,'ellipse',x,y,.42,.42,{line:{color:C.green,transparency:100},fill:{color:C.green}});addText(s,'✓',x,y+.03,.42,.30,{fontSize:14,bold:true,color:C.white,align:'center'});addText(s,it,x+.58,y-.04,3.48,.58,{fontSize:16.2,bold:true,color:C.navy});});
  addShape(s,'roundRect',1.15,5.73,11.05,.77,{line:{color:a,transparency:100},fill:{color:a,transparency:92}});
  addText(s,'Containerize software; stage active data; preserve provenance.',1.55,5.94,10.25,.36,{fontSize:19,bold:true,color:a,align:'center'});
 }}
];

(async()=>{
 addDeck(deck1,slides1); addDeck(deck2,slides2); addDeck(deck3,slides3); addDeck(deck4,slides4);
 // write metadata used by video builder
 fs.writeFileSync(path.join(OUT,'meta','deck_info.json'),JSON.stringify([
   {part:1,accent:deck1.accent,title:deck1.title},
   {part:2,accent:deck2.accent,title:deck2.title},
   {part:3,accent:deck3.accent,title:deck3.title},
   {part:4,accent:deck4.accent,title:deck4.title}
 ],null,2));
 console.log('Created four slide decks and narration sources.');
})();
