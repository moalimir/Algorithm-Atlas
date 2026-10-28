"""Rebuild mathematical reference plots and verify their exported coordinates.
Requires Matplotlib and NumPy; the tutorial itself has no runtime dependency.
"""
from pathlib import Path
import json
import re
import math
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/figures'
OUT.mkdir(parents=True, exist_ok=True)
BG, FG, GRID = '#0c1621', '#c7d5e0', '#304357'
MINT, ORANGE, VIOLET = '#75e1ce', '#ffc18c', '#c5b8ff'
plt.rcParams.update({'svg.fonttype': 'none', 'svg.hashsalt': 'algorithm-atlas-math', 'path.simplify': False,
                     'font.family': 'DejaVu Sans', 'font.size': 12, 'axes.labelcolor': FG,
                     'xtick.color': FG, 'ytick.color': FG, 'text.color': FG,
                     'axes.edgecolor': '#8095a8', 'axes.facecolor': BG, 'figure.facecolor': BG})

def axes_style(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.grid(color=GRID, linewidth=.7, alpha=.7)
    ax.set_axisbelow(True)

# A concrete theorem witness, not a sketch: 5N² − f(N) = (N − 4)(2N + 3).
fig = plt.figure(figsize=(11, 6.3), dpi=160)
ax = fig.add_axes([.10, .15, .86, .71])
x = np.linspace(0, 12, 1201)
functions = [('bounds-lower', 3*x*x, ORANGE, r'$3N^2$ (lower)', '--'),
             ('bounds-f', 3*x*x+5*x+12, MINT, r'$f(N)=3N^2+5N+12$', '-'),
             ('bounds-upper', 5*x*x, VIOLET, r'$5N^2$ (upper)', ':')]
for gid,y,color,label,style in functions:
    line, = ax.plot(x,y,color=color,label=label,linewidth=2.3,linestyle=style)
    line.set_gid(gid)
band=ax.fill_between(x,3*x*x,5*x*x,where=x>=4,color=MINT,alpha=.09)
band.set_gid('bounds-band')
ax.axvline(4,color=FG,linewidth=1,linestyle='--')
ax.scatter([4],[80],s=45,color=MINT,zorder=6)
ax.annotate(r'$N_0=4$; $f(4)=80$',xy=(4,80),xytext=(.7,180),color=FG,
            arrowprops={'arrowstyle':'->','color':FG},fontsize=11)
ax.set(xlim=(0,12),ylim=(0,800),xlabel='Input N',ylabel='Work units')
ax.set_xticks(np.arange(0,13,2));ax.set_yticks(np.arange(0,801,100));axes_style(ax)
ax.legend(loc='upper left',frameon=False,labelcolor=FG,fontsize=11)
fig.text(.10,.94,'A computed example of a tight asymptotic bound',fontsize=17,weight='bold')
fig.text(.10,.045,r'For every N ≥ 4: 3N² ≤ 3N² + 5N + 12 ≤ 5N². Curves use the same linear axes.',fontsize=11)
fig.savefig(OUT/'asymptotic-bounds.svg',metadata={'Date':None})
fig.savefig(OUT/'asymptotic-bounds.png',dpi=160)
plt.close(fig)
# Replace sampled polynomial strokes with analytic quadratic Bézier paths.
# Matplotlib owns the axes/layout; each Q segment exactly represents its polynomial.
svg_path=OUT/'asymptotic-bounds.svg'
svg=ET.parse(svg_path).getroot();ns={'s':'http://www.w3.org/2000/svg'}
W,H=11*72,6.3*72
left,right=.10*W,.96*W;top,bottom=(1-.86)*H,(1-.15)*H
X=lambda n:left+n/12*(right-left)
Y=lambda value:bottom-value/800*(bottom-top)
def quadratic(a,b,c,start=0,end=12):
    delta=end-start
    y0=a*start*start+b*start+c
    y1=y0+(2*a*start+b)*delta/2
    y2=a*end*end+b*end+c
    return (X(start),Y(y0),X((start+end)/2),Y(y1),X(end),Y(y2))
xml=svg_path.read_text()
max_svg_error=0
for gid,coef in [('bounds-lower',(3,0,0)),('bounds-f',(3,5,12)),('bounds-upper',(5,0,0))]:
    q=quadratic(*coef)
    d=f'M {q[0]:.15g} {q[1]:.15g} Q {q[2]:.15g} {q[3]:.15g} {q[4]:.15g} {q[5]:.15g}'
    pattern=rf'(<g id="{gid}">\s*<path d=")[^"]*'
    xml,count=re.subn(pattern,lambda m:m[1]+d,xml,count=1);assert count==1,gid
    for t in np.linspace(0,1,1201):
        u=(1-t)**2*q[0]+2*(1-t)*t*q[2]+t*t*q[4]
        v=(1-t)**2*q[1]+2*(1-t)*t*q[3]+t*t*q[5]
        n=(u-left)/(right-left)*12
        work=(bottom-v)/(bottom-top)*800
        expected=coef[0]*n*n+coef[1]*n+coef[2]
        max_svg_error=max(max_svg_error,abs(work-expected));assert abs(work-expected)<1e-9
upper=quadratic(5,0,0,4,12);lower=quadratic(3,0,0,12,4)
band_d=f'M {upper[0]} {upper[1]} Q {upper[2]} {upper[3]} {upper[4]} {upper[5]} L {lower[0]} {lower[1]} Q {lower[2]} {lower[3]} {lower[4]} {lower[5]} Z'
clip=svg.find('.//s:g[@id="bounds-f"]/s:path',ns).attrib['clip-path']
precise=ET.fromstring(xml)
band_node=precise.find('.//s:g[@id="bounds-band"]',ns)
for child in list(band_node):band_node.remove(child)
ET.SubElement(band_node,'{http://www.w3.org/2000/svg}path',{'d':band_d,'fill':MINT,'fill-opacity':'.09','stroke':'none','clip-path':clip})
ET.register_namespace('','http://www.w3.org/2000/svg')
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ET.ElementTree(precise).write(svg_path,encoding='utf-8',xml_declaration=True)
ET.parse(svg_path)
assert all(3*n*n<=3*n*n+5*n+12<=5*n*n for n in range(4,10001))
assert 3*3*3+5*3+12>5*3*3

# Discrete N: do not invent a continuous factorial curve or interpolate samples.
N=np.arange(1,13,dtype=int)
series=[('1',np.ones_like(N),'o','#b4c3cf'),('log₂ N',np.log2(N),'v',VIOLET),
        ('N',N,'s',MINT),('N log₂ N',N*np.log2(N),'D','#93bfff'),
        ('N²',N*N,'^',ORANGE),('2ᴺ',2.**N,'x','#ffa6bb'),
        ('N!',np.array([math.factorial(int(n)) for n in N]),'P','#ffdf7c')]
fig,ax=plt.subplots(figsize=(11,6.3),dpi=160)
fig.subplots_adjust(left=.10,right=.97,bottom=.16,top=.82)
for label,values,marker,color in series:
    keep=values>0
    ax.scatter(N[keep],values[keep],marker=marker,color=color,label=label,s=35,linewidths=1.5)
ax.set_yscale('log');ax.set(xlim=(.5,12.5),xlabel='Integer input N',ylabel='Normalized work (logarithmic scale)')
ax.set_xticks(N);axes_style(ax)
fig.legend(loc='upper center',bbox_to_anchor=(.54,.91),ncol=7,frameon=False,labelcolor=FG,fontsize=10.5)
fig.text(.10,.96,'Growth models at integer inputs',fontsize=17,weight='bold')
fig.text(.10,.04,'Each marker is a computed value. log₂(1) = 0 is omitted on the logarithmic axis. No connecting curves.',fontsize=10.5)
fig.savefig(OUT/'growth-models.svg',metadata={'Date':None});fig.savefig(OUT/'growth-models.png',dpi=160);plt.close(fig)
# Include a generic sans fallback so SVG image documents do not fall back to serif.
for filename in ['asymptotic-bounds.svg','growth-models.svg']:
    file=OUT/filename
    file.write_text(file.read_text().replace("font-family: 'DejaVu Sans'", "font-family: 'DejaVu Sans', Arial, sans-serif"))

manifest={'bounds':{'function':'3*N**2 + 5*N + 12','g':'N**2','lower_constant':3,'upper_constant':5,'N0':4,
 'x_limits':[0,12],'y_limits':[0,800],'svg_geometry':'analytic quadratic Bezier segments','svg_inverse_projection_max_error':max_svg_error,
 'curve_interpolation':'none; quadratic polynomial encoded analytically','proof':'5*N**2 - f(N) = (N-4)*(2*N+3)'},
 'growth':{'domain':'integer N from 1 to 12','scale':'logarithmic','interpolation':'none',
 'rows':[{'N':int(n),'values':[float(values[i]) for _,values,_,_ in series]} for i,n in enumerate(N)]},
 'tool_versions':{'matplotlib':matplotlib.__version__,'numpy':np.__version__}}
(OUT/'mathematical-models.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'PASS: exact quadratic SVG paths checked at 3,603 parameter values (max floating-point error {max_svg_error:.2g}); N₀=4 checked; discrete growth exports generated')
