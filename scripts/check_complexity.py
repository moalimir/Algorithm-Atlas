"""Verify lesson examples, source preservation, and the local navigation contract.
Run from anywhere: python3 scripts/check_complexity.py
"""
from pathlib import Path
from html.parser import HTMLParser
from contextlib import redirect_stdout
from io import StringIO
import ast
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
STANDALONE = (ROOT / 'data-structures/index.html').exists()
ENTRY = 'index.html' if STANDALONE else 'roadmap.html'
DSA_FILE = ROOT / ('data-structures/index.html' if STANDALONE else 'index.html')
ALGORITHM_FILE = ROOT / 'algorithms/index.html' if STANDALONE else ROOT.parent / 'Algorithms-Tutorial/index.html'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.examples = {}
        self.outputs = {}
        self.last_example = None
        self.current_output = None
        self.ids = set()
        self.links = []
        self.images = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, ('duplicate id', attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'a': self.links.append(attrs['href'])
        if tag == 'img': self.images.append(attrs['src'])
        if tag == 'pre' and attrs.get('data-example'):
            self.current = attrs['data-example']
            assert self.current not in self.examples
            self.examples[self.current] = ''
            self.last_example = self.current
        elif tag == 'pre' and attrs.get('class') == 'output':
            self.current_output = self.last_example
            self.outputs[self.current_output] = ''

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.current = None
            self.current_output = None

    def handle_data(self, data):
        if self.current: self.examples[self.current] += data
        if self.current_output: self.outputs[self.current_output] += data

pages = {}
for name in ['foundations.html', ENTRY]:
    page = Page()
    page.feed((ROOT / name).read_text())
    assert page.h1 == 1, (name, 'h1 count', page.h1)
    pages[name] = page
lesson = pages['foundations.html']
source = (ROOT / 'notes/complexity-source.md').read_text()
blocks = re.findall(r'```python\n(.*?)```', source, re.S)
assert len(blocks) == 20
for number, block in enumerate(blocks, 1):
    original_defs = [node for node in ast.parse(block).body if isinstance(node, ast.FunctionDef)]
    edited_defs = [node for node in ast.parse(lesson.examples[f'source-{number}']).body if isinstance(node, ast.FunctionDef)]
    assert [ast.dump(node) for node in original_defs] == [ast.dump(node) for node in edited_defs], number

expected = {
    'source-1': 'Starting analysis\n0\n1\n2\n0\n1\n2\n',
    'source-2': '0 0\n0 1\n1 0\n1 1\n',
    'source-3': '0 0\n0 1\n0 2\n1 1\n1 2\n2 2\n',
    'source-4': '1\n2\n4\n',
    'source-5': '0\n1\n0 0\n0 1\n1 0\n1 1\n',
    'source-6': '10\n',
    'source-7': '[0, 1, 2, 3]\n',
    'source-8': '[[0, 0], [0, 0]]\n',
    'source-9': 'None\n',
    'source-10': '1\n2\n7\n8\n9\n',
    'source-11': '1 7\n1 8\n1 9\n2 7\n2 8\n2 9\n',
    'source-12': 'DSA\n',
    'source-13': '2 5\n2 9\n5 9\n',
    'source-14': '[1, 1, 1, 1, 1]\n',
    'source-15': '15\n',
    'source-16': 'ananab\n',
    'source-17': '8\n',
    'source-18': '3\n-1\n',
    'source-19': 'True\nFalse\n',
    'source-20': '1\n-1\n',
    'contains': 'True\nFalse\n',
    'nested': '13\n',
    'triangle': '6\n',
    'running-total': '2\n7\n8\n',
    'sum-from': '12 0\n12\n',
    'join-word': 'DSA\n',
}
assert set(expected) == set(lesson.examples) == set(lesson.outputs)
ns = {}
for name, code in lesson.examples.items():
    output = StringIO()
    with redirect_stdout(output): exec(compile(code, name, 'exec'), ns)
    assert output.getvalue() == expected[name], (name, output.getvalue())
    assert output.getvalue().rstrip('\n') == lesson.outputs[name], ('displayed output mismatch', name)

# Check behavior at boundaries, plus the source's corrected duplicate-space case.
assert ns['constant_space'](0) == 0
assert ns['linear_space'](0) == set()
assert ns['quadratic_space'](0) == []
matrix = ns['quadratic_space'](3)
matrix[0][0] = 9
assert matrix[1][0] == 0
assert ns['recursive_countdown'](0) is None
assert ns['contains']([], 1) is False
assert ns['triangle'](0) == 0
assert ns['sum_from']([], 0) == 0
assert ns['sum_iterative']([], 0) == 0
assert ns['get_intersection']([], [1]) == []
assert ns['get_intersection']([1], [1] * 50) == [1] * 50
assert ns['count_operations'](0) == 0
assert ns['count_operations'](16) == 31
assert ns['reverse_string']('') == ''
assert ns['reverse_string']('a') == 'a'
assert ns['calculate_fibonacci'](0) == 0
assert ns['calculate_fibonacci'](1) == 1
assert ns['binary_search']([], 1) == -1
assert ns['binary_search']([1], 1) == 0
assert ns['binary_search']([1], 0) == -1
assert ns['search_matrix']([], 7) is False
assert ns['search_matrix']([[], [7]], 7) is True
assert ns['first_unique_character']('') == -1
assert ns['first_unique_character']('aabbc') == 4
assert ns['first_unique_character']('λμλ') == 1
assert ns['build_word_joined']([]) == ''
assert ns['build_word_joined'](['DS', 'A']) == 'DSA'

# At the deepest reversal call, inspect the still-live arguments, not elapsed time.
retained_lengths = []
def profile(frame, event, arg):
    if event == 'call' and frame.f_code is ns['reverse_string'].__code__ and len(frame.f_locals['text']) == 1:
        while frame:
            if frame.f_code is ns['reverse_string'].__code__:
                retained_lengths.append(len(frame.f_locals['text']))
            frame = frame.f_back
sys.setprofile(profile)
try: ns['reverse_string']('banana')
finally: sys.setprofile(None)
assert sorted(retained_lengths) == [1, 2, 3, 4, 5, 6]
assert sum(retained_lengths) - 6 == 15

# Match local URLs to actual file/section/category/lesson destinations.
dsa_html = DSA_FILE.read_text()
dsa = json.loads(re.search(r'<script id="bundle-pages" type="application/json">(.*?)</script>', dsa_html, re.S)[1])
algorithms = ALGORITHM_FILE.read_text()
metadata = algorithms[algorithms.index('to=[{'):algorithms.index('],o2=') + 1]
categories = set(re.findall(r'id:"([a-z-]+)",title:', metadata))
labs = set(re.findall(r'lessonId:"([a-z0-9-]+)"', metadata))
links = 0
for name, page in pages.items():
    for href in page.links:
        if href.startswith(('https:', 'http:')): continue
        links += 1
        target, _, fragment = href.partition('#')
        target = target or name
        assert (ROOT / target).is_file(), (name, href)
        if fragment:
            if target in pages: assert fragment in pages[target].ids, href
            elif (ROOT / target).resolve() == DSA_FILE.resolve(): assert fragment.removeprefix('/') in dsa, href
            elif (ROOT / target).resolve() == ALGORITHM_FILE.resolve():
                kind, key = fragment.removeprefix('/').split('/', 1)
                assert key in (categories if kind == 'category' else labs), href
    for image in page.images: assert (ROOT / image).is_file(), image
assert {'cost', 'space', 'recursion', 'invariant', 'practice'}.issubset(lesson.ids)
# Useful initial teaching states exist before any JavaScript runs.
lesson_html = (ROOT / 'foundations.html').read_text()
assert len(re.findall(r'class="js-controls" hidden', lesson_html)) == 5
initial_growth = re.search(r'<svg id="growth-chart"[^>]*>(.*?)</svg>', lesson_html, re.S)[1]
assert initial_growth.count('class="growth-series"') == 7
initial_grid = re.search(r'<div id="loop-grid"[^>]*>(.*?)</div>', lesson_html, re.S)[1]
assert initial_grid.count('loop-cell filled') == 15
initial_tree = re.search(r'<svg id="merge-tree"[^>]*>(.*?)</svg>', lesson_html, re.S)[1]
assert initial_tree.count('<circle ') == 15

assert len(lesson.ids) == len(set(lesson.ids))
svg = ET.parse(ROOT / 'complexity-review.svg').getroot()
assert svg.attrib['width'] == '1400' and svg.attrib['height'] == '1900'
png = (ROOT / 'complexity-review.png').read_bytes()
assert png[:8] == b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II', png[16:24]) == (1400, 1900)

# Invert the actual exported analytic SVG curves, independently of Matplotlib.
bounds = ET.parse(ROOT / 'assets/figures/asymptotic-bounds.svg').getroot()
namespace = {'s': 'http://www.w3.org/2000/svg'}
manifest = json.loads((ROOT / 'assets/figures/mathematical-models.json').read_text())
assert manifest['bounds']['N0'] == 4
curve_checks = 0
for gid, coefficients in [('bounds-lower', (3, 0, 0)), ('bounds-f', (3, 5, 12)), ('bounds-upper', (5, 0, 0))]:
    path = bounds.find(f'.//s:g[@id="{gid}"]/s:path', namespace)
    assert ' Q ' in path.attrib['d'] and ' L ' not in path.attrib['d']
    clip_id = re.search(r'#([^)]*)', path.attrib['clip-path'])[1]
    rect = bounds.find(f'.//s:clipPath[@id="{clip_id}"]/s:rect', namespace)
    left, top, width, height = (float(rect.attrib[key]) for key in ['x','y','width','height'])
    values = list(map(float, re.findall(r'[-+]?(?:\d*\.)?\d+(?:[eE][-+]?\d+)?', path.attrib['d'])))
    assert len(values) == 6
    for i in range(1201):
        t = i / 1200
        x = (1-t)**2*values[0]+2*(1-t)*t*values[2]+t*t*values[4]
        y = (1-t)**2*values[1]+2*(1-t)*t*values[3]+t*t*values[5]
        n = (x-left)/width*12
        work = (top+height-y)/height*800
        a,b,c = coefficients
        assert abs(work-(a*n*n+b*n+c)) < 1e-8, (gid,n,work)
        curve_checks += 1
# The shaded band's two analytic boundaries must use the same polynomials.
band = bounds.find('.//s:g[@id="bounds-band"]/s:path', namespace)
coordinates = list(map(float, re.findall(r'[-+]?(?:\d*\.)?\d+(?:[eE][-+]?\d+)?', band.attrib['d'])))
assert len(coordinates) == 12
for values, start, end, coefficient in [(coordinates[:6],4,12,5),(coordinates[6:],12,4,3)]:
    for i in range(121):
        t = i / 120
        x = (1-t)**2*values[0]+2*(1-t)*t*values[2]+t*t*values[4]
        y = (1-t)**2*values[1]+2*(1-t)*t*values[3]+t*t*values[5]
        n = (x-left)/width*12
        work = (top+height-y)/height*800
        assert abs(n-(start+(end-start)*t)) < 1e-10
        assert abs(work-coefficient*n*n) < 1e-8
        curve_checks += 1
assert (3*4*4+5*4+12) == 5*4*4
assert (3*3*3+5*3+12) > 5*3*3

print(f'PASS: 20 source examples preserved; {len(expected)} outputs; 29 behavior/retention checks; {links} local links; summary assets; legacy anchors')
print(f'PASS: {curve_checks} inverse-projection checks of the exported analytic SVG curves')
print('Runtime:', sys.version.split()[0])
