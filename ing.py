from PIL import Image as I
from os import listdir as ls
from itertools import permutations as pe


for j in ls('orig'):
    im = I.open('orig/'+j)
    il = im.load()
    c = set()
    for x in range(16):
        for y in range(16):
            c|={il[x,y]}
    c = {i for i in c if not i[-1]==0}
    print(j,len(c))

def dist(a,b):
    p=2
    return sum(abs(a[i]-b[i])**p for i in range(4))
def gs(a):
    return a[0]*3+a[1]*6+a[2]
def impose(sf,cf):
    s=I.open('orig/'+sf+'.png').load()
    c=I.open('orig/'+cf+'.png').load()
    ds,dc = {},{}
    oi = I.new('RGBA',(16,16))
    ol = oi.load()
    for x in range(16):
        for y in range(16):
            ps,pc=s[x,y],c[x,y]
            if ps[-1]==0:ps=(0,0,0,0)
            if pc[-1]==0:pc=(0,0,0,0)
            if not ps in ds:ds[ps]=0
            if not pc in dc:dc[pc]=0
            ds[ps]+=1
            dc[pc]+=1
    dc.pop((0,0,0,0))
    ds.pop((0,0,0,0))
    while len(dc)>len(ds):
        i = min(dc,key=lambda x:dc[x])
        ic = dc.pop(i)
        mi = min(dc,key=lambda x:dist(i,x))
        dc[mi]+=ic
    while len(dc)<len(ds):
        i = min(ds,key=lambda x:ds[x])
        is_ = ds.pop(i)
        mi = min(ds,key=lambda x:dist(i,x))
        ds[mi]+=is_
        for x in range(16):
            for y in range(16):
                if s[x,y]==i:s[x,y]=mi
#    sl = list([i for i in ds])
#    cl = min(pe((j for j in dc)),key=lambda x:sum(dist(sl[k],x[k]) for k in range(len(dc))))
    sl = list(sorted([i for i in ds],key=gs))
    cl = list(sorted([i for i in dc],key=gs))
    l = {sl[i]:cl[i] for i in range(len(sl))}
    l[(0,0,0,0)]=(0,0,0,0)
    
    for x in range(16):
        for y in range(16):
            if s[x,y][-1]==0:s[x,y]=(0,0,0,0)
            ol[x,y]=l[s[x,y]]
    oi.save('out/'+cf+' '+sf+'.png')


o = {'coal':0,'diamond':4,'emerald':5,'gold_ingot':6,'iron_ingot':9,'lapis_lazuli':3,'netherite_ingot':10,'redstone':8,'quartz':1,'amethyst_shard':2,'copper_ingot':7,'ruby':-1,'gold_nugget':-2,'iron_nugget':-3}
from random import randrange as rr
for i in o:o[i]=rr(222)

def gen():
    for i in o:
        for j in o:
            print(i,j)
            impose(j,i)


'''def grid(u=1):
    i = I.new('RGBA',(16*len(o)*u,16*len(o)*u))
    il=i.load()
    for j in range(len(o)):
        for k in range(len(o)):
            cf=sorted(o)[j]
            sf=sorted(o)[k]
            ii = I.open('out/'+cf+' '+sf+'.png').load()
            for a in range(u):
                for b in range(u):
                    for x in range(16):
                        for y in range(16):
                            il[16*(j*u+a)+x,16*(k*u+b)+y]=ii[x,y]
    i.save('grid.png')'''
def grid(u=1):
    i = I.new('RGBA',(16*len(o)*u,16*len(o)*u))
    il=i.load()
    for j in range(len(o)):
        for k in range(len(o)):
            s=lambda x:o[x]
            cf=sorted(o,key=s)[j]
            sf=sorted(o,key=s)[k]
            ii = I.open('out/'+cf+' '+sf+'.png').load()
            for a in range(u):
                for b in range(u):
                    for x in range(16):
                        for y in range(16):
                            il[u*(16*j+x)+a,u*(16*k+y)+b]=ii[x,y]
    i.save('grid.png')
gen()
grid(10)

'''i = I.open('orig/ruby.png')
il=i.load()
for x in range(16):
    for y in range(16):
        il[x,y]=il[x,y][:3]+(255,)
i.show()
'''
