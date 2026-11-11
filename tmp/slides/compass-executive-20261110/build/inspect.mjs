import fs from 'node:fs/promises';
import {FileBlob, PresentationFile} from '@oai/artifact-tool';
const root='/Users/jjacks20/jjacks/Conversational-AI';
const p=await PresentationFile.importPptx(await FileBlob.load(root+'/Minerva/Compass_Executive_Briefing_Updated.pptx'));
const slide=p.slides.getItem(0);
await fs.writeFile(root+'/tmp/slides/compass-executive-20261110/preview/original.png',new Uint8Array(await (await p.export({slide,format:'png',scale:1.5})).arrayBuffer()));
const q=await p.inspect({select:'$.slides[*]',include:['id','index','layout','elements.id','elements.kind','elements.text','elements.position','elements.style','notes.text']});
await fs.writeFile(root+'/tmp/slides/compass-executive-20261110/original-inspect.ndjson',q.ndjson);
console.log(q.ndjson);
