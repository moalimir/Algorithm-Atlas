// Verify values AND the coordinates that encode them: node scripts/check_complexity.js
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(path.join(__dirname,'..','foundations.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const model=vm.runInNewContext(script+'\nComplexityLesson;',{});
let checks=0;
function near(actual,expected,tolerance=1e-9){assert(Math.abs(actual-expected)<=tolerance*Math.max(1,Math.abs(expected)),`${actual} != ${expected}`);checks++;}
function attributes(tag){return Object.fromEntries([...tag.matchAll(/([\w-]+)="([^"]*)"/g)].map(m=>[m[1],m[2]]));}
function numericAxis(svg,id){const a=attributes(svg.match(new RegExp(`<g id="${id}"[^>]*>`))[0]);return Object.fromEntries(Object.entries(a).map(([k,v])=>[k,k.startsWith('data-')&&k!=='data-scale'?Number(v):v]));}
function formula(n,index){if(index===0)return 1;if(index===1)return Math.log2(n);if(index===2)return n;if(index===3)return n*Math.log2(n);if(index===4)return n*n;if(index===5)return 2**n;return Array.from({length:n},(_,i)=>i+1).reduce((a,b)=>a*b,1);}
assert.deepEqual(Array.from(model.growth(8)),[1,3,8,24,64,256,40320]);checks++;
for(let n=2;n<=16;n++)for(const scale of ['linear','log']){
 const svg=model.growthSvg(n,scale),axis=numericAxis(svg,'growth-axis');
 assert(!/NaN|Infinity|undefined/.test(svg));assert(!svg.includes('<polyline'));checks+=2;
 const groups=[...svg.matchAll(/<g class="growth-series" data-series="([^"]+)">/g)];assert.equal(groups.length,7);checks++;
 for(let index=0;index<7;index++){
  const section=svg.slice(groups[index].index,index===6?undefined:groups[index+1].index);
  const points=[...section.matchAll(/<g transform="translate\(([-\d.e+]+) ([-\d.e+]+)\)" class="growth-point" data-n="(\d+)" data-value="([^"]+)">/g)];
  assert.equal(points.length,n-((index===1||index===3)&&scale==='log'?1:0));checks++;
  for(const point of points){
   const x=Number(point[1]),y=Number(point[2]),k=Number(point[3]),value=Number(point[4]);
   const L=axis['data-left'],R=axis['data-right'],T=axis['data-top'],B=axis['data-bottom'],Y=axis['data-y-max'];
   near(1+(x-L)/(R-L)*(n-1),k);
   const inverted=scale==='log'?Y**((B-y)/(B-T)):(B-y)/(B-T)*Y;
   if([0,2,4,5,6].includes(index)){assert.equal(value,formula(k,index));checks++;}else near(value,formula(k,index),1e-13);if(scale==='log')near(inverted,formula(k,index),1e-11);else near(inverted/Y,formula(k,index)/Y,1e-12);
  }
 }
 // Axis tick positions must invert to their own numeric labels' values.
 for(const tick of svg.matchAll(/<text class="y-tick"[^>]*>/g)){
  const a=attributes(tick[0]),ratio=(axis['data-bottom']-Number(a.y))/(axis['data-bottom']-axis['data-top']);
  near(scale==='log'?axis['data-y-max']**ratio:axis['data-y-max']*ratio,Number(a['data-value']),1e-11);
 }
 assert.equal((model.growthTable(n).match(/<tr>/g)||[]).length,8);checks++;
}
for(let n=2;n<=8;n++){
 near(model.loop(n,'square').total,n*n);near(model.loop(n,'triangle').total,n*(n+1)/2);near(model.loop(n,'bounded').total,2*n-3);
 for(const mode of ['square','triangle','bounded']){const result=model.loop(n,mode);near(result.cells.filter(Boolean).length,result.total);near(result.rows.reduce((a,b)=>a+b,0),result.total);near((model.loopHtml(n,mode).match(/loop-cell filled/g)||[]).length,result.total);}
}
for(let n=1;n<=32;n++){
 const d=model.doubling(n),svg=model.appendSvg(n),axis=numericAxis(svg,'append-axis');
 near(d.total,n+d.copies);near(d.costs.reduce((a,b)=>a+b,0),d.total);assert(d.total<3*n);checks++;
 near(axis['data-y-max'],20);
 const bars=[...svg.matchAll(/<g class="append-bar"[^>]*>([\s\S]*?)<\/g>/g)];near(bars.length,n);
 bars.forEach((bar,i)=>{
  const a=attributes(bar[0].slice(0,bar[0].indexOf('>')+1));near(Number(a['data-cost']),d.costs[i]);
  const rects=[...bar[1].matchAll(/<rect[^>]*>/g)].map(r=>attributes(r[0]));
  near(Number(rects[0].height)/(axis['data-bottom']-axis['data-top'])*20,1);
  const sum=rects.reduce((total,r)=>total+Number(r.height),0);
  near(sum/(axis['data-bottom']-axis['data-top'])*20,d.costs[i]);
  if(rects[1])near(Number(rects[1].height)/(axis['data-bottom']-axis['data-top'])*20,d.copied[i]);
 });
}
for(const n of [1,4,16,64]){
 const d=model.dominance(n),svg=model.dominanceSvg(n),rects=[...svg.matchAll(/<rect[^>]*>/g)].map(m=>attributes(m[0]));
 let next=10,totalWidth=0;
 rects.forEach((r,i)=>{near(Number(r['data-numerator']),[3*n*n,5*n,12][i]);near(Number(r['data-denominator']),3*n*n+5*n+12);near(Number(r.x),next);near(Number(r.width)/700,Number(r['data-numerator'])/Number(r['data-denominator']));next+=Number(r.width);totalWidth+=Number(r.width);});
 near(totalWidth,700);near(d.total,3*n*n+5*n+12);
}
for(const n of [1,2,4,8]){
 const tree=model.mergeTree(n);near(tree.calls,2*n-1);near(tree.frames,Math.log2(n)+1);near(tree.nodes.length,tree.calls);
 for(let level=0;level<=tree.depth;level++){const row=tree.nodes.filter(node=>node.level===level);near(row.length,2**level);near(row.reduce((total,node)=>total+node.size,0),n);}
}
const tree=model.mergeTree(8),treeSvg=model.mergeTreeSvg(8);
for(const m of treeSvg.matchAll(/<path class="tree-edge[^>]*>/g)){
 const a=attributes(m[0]),[pl,pi]=a['data-parent'].split(':').map(Number),[cl,ci]=a['data-child'].split(':').map(Number);
 const p=tree.nodes.find(node=>node.level===pl&&node.index===pi),c=tree.nodes.find(node=>node.level===cl&&node.index===ci);
 const xy=a.d.match(/M([-\d.e+]+) ([-\d.e+]+)L([-\d.e+]+) ([-\d.e+]+)/).slice(1).map(Number);
 near(Math.hypot(xy[0]-p.x,xy[1]-p.y),21);near(Math.hypot(xy[2]-c.x,xy[3]-c.y),21);near(c.size,p.size/2);
}
const slices=model.slicesSvg('banana');let copied=0;
for(const m of slices.matchAll(/<g class="slice-row" data-row="(\d+)" data-length="(\d+)">([\s\S]*?)(?=<g class="slice-row"|$)/g)){
 const row=Number(m[1]),length=Number(m[2]),cells=[...m[3].matchAll(/<rect[^>]*>/g)].map(r=>attributes(r[0]));near(cells.length,6-row);near(length,6-row);
 cells.forEach((r,i)=>{near(Number(r.x),145+i*58);near(Number(r.width),58);near(Number(r.height),34);});if(row>0)copied+=length;
}
near(copied,15);
console.log(`PASS: ${checks} value, inverse-axis, bar-height, tree-edge, and unit-cell checks`);
