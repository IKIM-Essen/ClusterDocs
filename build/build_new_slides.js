const pptxgen = require('pptxgenjs');
const { warnIfSlideHasOverlaps, warnIfSlideElementsOutOfBounds } = require('/home/oai/skills/slides/pptxgenjs_helpers');

const OUT = '/mnt/data/clusterdocs-ng-v0.1.2-work/slides';
const pptxgenjs = pptxgen;

function baseDeck(title, subtitle) {
  const pptx = new pptxgenjs();
  pptx.layout = 'LAYOUT_WIDE';
  pptx.author = 'RCC ClusterDocs NG';
  pptx.subject = 'RCC user training';
  pptx.company = 'IKIM / RCC';
  pptx.theme = { headFontFace: 'Aptos Display', bodyFontFace: 'Aptos' };
  const slide = pptx.addSlide();
  slide.background = { color: 'F7FAFC' };
  slide.addText(title, { x:0.8, y:1.7, w:11.6, h:0.8, fontSize:38, bold:true, color:'16324F', margin:0 });
  slide.addText(subtitle, { x:0.85, y:2.65, w:10.8, h:0.6, fontSize:20, color:'435466', margin:0 });
  slide.addShape(pptx.ShapeType.line, { x:0.85, y:3.45, w:4.2, h:0, line:{ color:'2A7A80', width:3 } });
  slide.addText('RCC ClusterDocs NG', { x:0.85, y:6.65, w:4.8, h:0.3, fontSize:13, color:'607080', margin:0 });
  return pptx;
}
function title(slide, txt) { slide.addText(txt, { x:0.6, y:0.35, w:12.1, h:0.45, fontSize:28, bold:true, color:'16324F', margin:0 }); }
function footer(slide, n) { slide.addText(`Class deck · ${n}`, { x:10.7, y:7.0, w:2, h:0.25, fontSize:10, color:'7A8694', margin:0, align:'right' }); }
function box(slide, pptx, text, x, y, w, h, color='FFFFFF') { slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color},line:{color:'D6DEE6',width:1}}); slide.addText(text,{x:x+0.18,y:y+0.16,w:w-0.36,h:h-0.28,fontSize:16,color:'1D2B38',margin:0,fit:'shrink'}); }
function lane(slide,pptx,label,x,y,w,h,color) { slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color,transparency:8},line:{color}}); slide.addText(label,{x:x+0.15,y:y+0.12,w:w-0.3,h:0.3,fontSize:15,bold:true,color:'16324F',margin:0}); }
function validate(pptx){ for(const s of pptx._slides){ warnIfSlideHasOverlaps(s,pptx,{ignoreDecorativeShapes:true}); warnIfSlideElementsOutOfBounds(s,pptx); } }

async function deckLargeData(){
 const pptx = baseDeck('Interactive large-data analysis', 'Python and R notebooks that stay friendly to shared cluster resources');
 let s = pptx.addSlide(); s.background={color:'FFFFFF'}; title(s,'The core pattern');
 lane(s,pptx,'Notebook',0.8,1.35,2.4,3.7,'DDF2F2'); lane(s,pptx,'Slurm job',4.0,1.35,2.4,3.7,'E8F0FE'); lane(s,pptx,'Project storage',7.2,1.35,2.4,3.7,'F2E8FF'); lane(s,pptx,'Reviewable output',10.4,1.35,2.1,3.7,'EAF7EA');
 s.addText('Inspect\nSample\nExplain', {x:1.05,y:2.0,w:1.9,h:1.3,fontSize:20,bold:true,color:'16324F',align:'center',margin:0});
 s.addText('Compute\nRepeat\nScale', {x:4.25,y:2.0,w:1.9,h:1.3,fontSize:20,bold:true,color:'16324F',align:'center',margin:0});
 s.addText('Read inputs\nWrite final\nAvoid small-file storms', {x:7.45,y:1.95,w:1.9,h:1.6,fontSize:17,bold:true,color:'16324F',align:'center',margin:0});
 s.addText('Figures\nTables\nMethods', {x:10.65,y:2.0,w:1.55,h:1.3,fontSize:20,bold:true,color:'16324F',align:'center',margin:0});
 s.addShape(pptx.ShapeType.chevron,{x:3.25,y:2.65,w:0.55,h:0.5,fill:{color:'2A7A80'},line:{color:'2A7A80'}}); s.addShape(pptx.ShapeType.chevron,{x:6.45,y:2.65,w:0.55,h:0.5,fill:{color:'2A7A80'},line:{color:'2A7A80'}}); s.addShape(pptx.ShapeType.chevron,{x:9.65,y:2.65,w:0.55,h:0.5,fill:{color:'2A7A80'},line:{color:'2A7A80'}});
 s.addText('Completion gate: one loopback-only notebook job, one bounded batch job, no shared accounts, no exposed ports.', {x:1.0,y:5.75,w:11.3,h:0.55,fontSize:18,color:'435466',margin:0,align:'center'}); footer(s,2);

 s = pptx.addSlide(); title(s,'Choose the right tool for the question');
 box(s,pptx,'pandas\nTeaching, moderate tables, quick checks',0.8,1.25,2.8,1.45,'F7FAFC');
 box(s,pptx,'DuckDB / Arrow\nColumn selection, SQL, larger tables',3.9,1.25,2.8,1.45,'F7FAFC');
 box(s,pptx,'data.table / dplyr\nFast R tables and readable pipelines',7.0,1.25,2.8,1.45,'F7FAFC');
 box(s,pptx,'Matplotlib / ggplot2\nReviewable figures from sampled data',10.1,1.25,2.5,1.45,'F7FAFC');
 s.addText('Start with structure, not scale', {x:0.85,y:3.3,w:4.4,h:0.4,fontSize:22,bold:true,color:'16324F',margin:0});
 s.addText('File format → columns needed → sample size → memory footprint → full computation path', {x:0.85,y:3.95,w:11.4,h:0.45,fontSize:18,color:'435466',margin:0});
 s.addShape(pptx.ShapeType.line,{x:1.0,y:5.0,w:10.8,h:0,line:{color:'2A7A80',width:3}});
 ['format','columns','sample','memory','Slurm'].forEach((t,i)=>{ s.addShape(pptx.ShapeType.ellipse,{x:0.75+i*2.7,y:4.75,w:0.55,h:0.55,fill:{color:'2A7A80'},line:{color:'2A7A80'}}); s.addText(t,{x:0.5+i*2.7,y:5.38,w:1.1,h:0.35,fontSize:13,color:'16324F',align:'center',margin:0}); }); footer(s,3);

 s = pptx.addSlide(); title(s,'Notebook safety checklist');
 const checks=['Run inside Slurm','Bind to loopback only','Keep the token enabled','Use synthetic data for learning','No secrets in cells','Stop the job when done'];
 checks.forEach((c,i)=>{ const x=i%2?6.8:1.0; const y=1.3+Math.floor(i/2)*1.25; s.addText('✓',{x,y,w:0.4,h:0.35,fontSize:22,bold:true,color:'2A7A80',margin:0}); s.addText(c,{x:x+0.45,y:y+0.03,w:4.9,h:0.35,fontSize:20,color:'1D2B38',margin:0}); });
 s.addText('A notebook is part of the analysis record. Keep it clean enough for a colleague to understand and safe enough to share.',{x:1.0,y:5.6,w:11.2,h:0.7,fontSize:18,color:'435466',align:'center',margin:0}); footer(s,4);

 s = pptx.addSlide(); title(s,'When to leave the notebook');
 box(s,pptx,'Still a notebook\nSmall samples, visual checks, method explanation, figures for discussion',0.9,1.35,3.3,3.4,'EAF7EA');
 box(s,pptx,'Move to Slurm\nFull dataset, repeated execution, overnight work, parameter sweeps, GPU use',4.95,1.35,3.3,3.4,'E8F0FE');
 box(s,pptx,'Move to a vhost\nTeam-facing interface, curated results, authenticated access, project users',9.0,1.35,3.3,3.4,'F2E8FF');
 s.addText('The best workflow is often all three: notebook for design, Slurm for computation, vhost for presentation.',{x:1.0,y:5.65,w:11.3,h:0.6,fontSize:19,bold:true,color:'16324F',align:'center',margin:0}); footer(s,5);

 s = pptx.addSlide(); title(s,'Class gates');
 s.addText('1', {x:1.0,y:1.35,w:0.6,h:0.6,fontSize:26,bold:true,color:'FFFFFF',fill:{color:'2A7A80'},margin:0,align:'center'}); s.addText('Run the interactive example validator', {x:1.85,y:1.45,w:9.5,h:0.4,fontSize:21,color:'1D2B38',margin:0});
 s.addText('2', {x:1.0,y:2.45,w:0.6,h:0.6,fontSize:26,bold:true,color:'FFFFFF',fill:{color:'2A7A80'},margin:0,align:'center'}); s.addText('Start one Jupyter job and connect through a tunnel', {x:1.85,y:2.55,w:9.5,h:0.4,fontSize:21,color:'1D2B38',margin:0});
 s.addText('3', {x:1.0,y:3.55,w:0.6,h:0.6,fontSize:26,bold:true,color:'FFFFFF',fill:{color:'2A7A80'},margin:0,align:'center'}); s.addText('Submit one Python or R batch script', {x:1.85,y:3.65,w:9.5,h:0.4,fontSize:21,color:'1D2B38',margin:0});
 s.addText('4', {x:1.0,y:4.65,w:0.6,h:0.6,fontSize:26,bold:true,color:'FFFFFF',fill:{color:'2A7A80'},margin:0,align:'center'}); s.addText('Explain what should move out of the notebook', {x:1.85,y:4.75,w:9.5,h:0.4,fontSize:21,color:'1D2B38',margin:0}); footer(s,6);
 validate(pptx); await pptx.writeFile({ fileName: `${OUT}/RCC_Class_7_Interactive_Large_Data.pptx` });
}

async function deckApps(){
 const pptx = baseDeck('Shiny, Jupyter, and governed project apps','From a safe interactive session to a reviewed web service');
 let s = pptx.addSlide(); title(s,'Two modes: development and service');
 box(s,pptx,'Development\nSingle learner or developer\nSlurm allocation\nSSH tunnel\nLoopback only',1.0,1.35,4.6,3.7,'E8F0FE');
 box(s,pptx,'Governed service\nProject users\nGateway authentication\nProject-group authorization\nReviewed data paths',7.3,1.35,4.6,3.7,'F2E8FF');
 s.addShape(pptx.ShapeType.chevron,{x:6.05,y:2.85,w:0.75,h:0.65,fill:{color:'2A7A80'},line:{color:'2A7A80'}});
 s.addText('A working demo does not automatically become a production site.',{x:1.0,y:5.75,w:11.2,h:0.6,fontSize:20,bold:true,color:'16324F',align:'center',margin:0}); footer(s,2);

 s = pptx.addSlide(); title(s,'Safe data patterns for web apps');
 lane(s,pptx,'Good',0.9,1.15,5.3,4.4,'EAF7EA'); lane(s,pptx,'Avoid',7.0,1.15,5.3,4.4,'FFE8E8');
 s.addText('Read-only database views\nCurated result collections\nOpaque file identifiers\nUpload staging area\nHeavy work through Slurm', {x:1.25,y:1.75,w:4.6,h:3.2,fontSize:19,color:'1D2B38',margin:0,breakLine:false,fit:'shrink'});
 s.addText('Raw project directory browser\nUser-supplied filesystem paths\nSecrets in app code\nLong computation inside requests\nShared project passwords', {x:7.35,y:1.75,w:4.6,h:3.2,fontSize:19,color:'1D2B38',margin:0,fit:'shrink'});
 footer(s,3);

 s = pptx.addSlide(); title(s,'Application responsibilities');
 ['Check trusted identity headers','Verify project group again','Validate every input','Log user-visible actions','Return request IDs, not stack traces'].forEach((c,i)=>{ box(s,pptx,c,1.0,1.15+i*0.9,11.3,0.55, i%2?'FFFFFF':'F7FAFC'); });
 s.addText('The gateway authenticates the user. The application still protects its own data model.',{x:1.0,y:6.0,w:11.2,h:0.45,fontSize:19,bold:true,color:'16324F',align:'center',margin:0}); footer(s,4);

 s = pptx.addSlide(); title(s,'Shiny path');
 s.addShape(pptx.ShapeType.line,{x:1.1,y:3.0,w:10.5,h:0,line:{color:'2A7A80',width:3}});
 const steps=['local app','Slurm demo','data review','vhost request','governed service'];
 steps.forEach((t,i)=>{ const x=0.9+i*2.55; s.addShape(pptx.ShapeType.ellipse,{x,y:2.72,w:0.58,h:0.58,fill:{color:'2A7A80'},line:{color:'2A7A80'}}); s.addText(t,{x:x-0.35,y:3.5,w:1.3,h:0.5,fontSize:14,color:'16324F',align:'center',margin:0}); });
 s.addText('At every stage: no direct project-directory browsing and no account sharing.',{x:1.0,y:5.3,w:11.2,h:0.5,fontSize:20,bold:true,color:'16324F',align:'center',margin:0}); footer(s,5);

 s = pptx.addSlide(); title(s,'Gate before production');
 ['Project lead identified','User group defined','Data source reviewed','Resource limits estimated','Support contact named','Review date recorded'].forEach((c,i)=>{ const x=i<3?1.0:7.0; const y=1.25+(i%3)*1.25; s.addText('□',{x,y,w:0.4,h:0.35,fontSize:24,color:'2A7A80',margin:0}); s.addText(c,{x:x+0.45,y:y+0.03,w:4.6,h:0.35,fontSize:20,color:'1D2B38',margin:0}); });
 s.addText('If heavy work is needed, the request must state how Slurm will run it.',{x:1.0,y:5.65,w:11.2,h:0.6,fontSize:20,bold:true,color:'16324F',align:'center',margin:0}); footer(s,6);
 validate(pptx); await pptx.writeFile({ fileName: `${OUT}/RCC_Class_9_Shiny_Jupyter_Project_Apps.pptx` });
}

(async()=>{ await deckLargeData(); await deckApps(); })();
