#!/usr/bin/env python3
"""Run the actual shared shader geometry on CPU, without a graphics device."""
from pathlib import Path
import re
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / 'shared/newpixie.glsl').read_text()
functions = '\n'.join(re.search(r'(?:vec2|float) ' + name + r'\([^)]*\) \{[^}]*\}', source).group() for name in ('curve', 'edgeMask'))
code = r'''
#include <algorithm>
#include <cassert>
#include <cmath>
struct vec2 { double x,y; vec2(double a,double b):x(a),y(b){} vec2(double a):x(a),y(a){} };
vec2 operator+(vec2 a,vec2 b){return {a.x+b.x,a.y+b.y};}
vec2 operator-(vec2 a,vec2 b){return {a.x-b.x,a.y-b.y};}
vec2 operator*(vec2 a,vec2 b){return {a.x*b.x,a.y*b.y};}
vec2 min(vec2 a,vec2 b){return {std::min(a.x,b.x),std::min(a.y,b.y)};}
using std::min;
double smoothstep(double a,double b,double x){double t=std::clamp((x-a)/(b-a),0.0,1.0);return t*t*(3-2*t);}
''' + functions + r'''
void close(double a,double b){assert(std::abs(a-b)<1e-6);}
int main(){
 auto center=curve({.5,.5});close(center.x,.5);close(center.y,.5);
 for(int y=0;y<=100;y++)for(int x=0;x<=100;x++){
  vec2 uv(x/100.0,y/100.0);auto p=curve(uv);
  auto mirrorX=curve({1-uv.x,uv.y});auto mirrorY=curve({uv.x,1-uv.y});
  close(p.x,1-mirrorX.x);close(p.y,mirrorX.y);close(p.x,mirrorY.x);close(p.y,1-mirrorY.y);
  assert(std::isfinite(p.x)&&std::isfinite(p.y));
  if(x<100)assert(curve({uv.x+.01,uv.y}).x>p.x);
  if(y<100)assert(curve({uv.x,uv.y+.01}).y>p.y);
 }
 for(auto resolution:{vec2(640,480),vec2(1920,1080),vec2(2732,2048)}){
  close(edgeMask(center,resolution),1);
  for(int i=0;i<=100;i++){
   double t=i/100.0;
   for(auto uv:{vec2(0,t),vec2(1,t),vec2(t,0),vec2(t,1)})close(edgeMask(curve(uv),resolution),0);
  }
  close(edgeMask({.5/resolution.x,.5},resolution),.5);
  close(edgeMask({1/resolution.x,.5},resolution),1);
  close(edgeMask({-.001,.5},resolution),0);
  close(edgeMask({1.001,.5},resolution),0);
 }
}
'''
with tempfile.TemporaryDirectory() as tmp:
    cpp = Path(tmp) / 'geometry.cpp'
    executable = Path(tmp) / 'geometry'
    cpp.write_text(code)
    subprocess.run(['clang++', '-std=c++17', str(cpp), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
subprocess.run(['python3', str(root / 'scripts/generate_shader_source.py'), '--check'], check=True)
print('CRT geometry: center, bilateral symmetry, monotonicity, four black borders and pixel feather passed; both backends match.')
