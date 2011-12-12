from workflow import *

def main(file):
    """LEAD Mesoscale Meterology workflow (Figure 1 in Ramakrishnan and Gannon)"""
    w = Workflow()
    
    infile = File(name="input.txt", size=147*MB)
    
    tppo1 = File(name="tpp.txt", size=0.2*MB)
    tpp = Job(id="tpp", namespace="leadmm", name="TerrainPreProcessor", runtime=4*SECONDS, outputs=[tppo1])
    w.addJob(tpp)
    
    wrfstatico1 = File(name="wrfstatic.txt", size=19*MB)
    wrfstatic = Job(id="wrfstatic", namespace="leadmm", name="WrfStatic", runtime=338*SECONDS, outputs=[wrfstatico1])
    w.addJob(wrfstatic)
    
    lbio1 = File("lbi.txt", size=488*MB)
    lbi = Job(id="lbi", namespace="leadmm", name="LateralBoundaryInterpolator", runtime=146*SECONDS, inputs=[infile, tppo1], outputs=[lbio1])
    lbi.addParent(tpp)
    w.addJob(lbi)
    
    tdio1 = File("tdi.txt", size=243*MB)
    tdi = Job(id="tdi", namespace="leadmm", name="3DInterpolator", runtime=88*SECONDS, inputs=[infile, tppo1], outputs=[tdio1])
    tdi.addParent(tpp)
    w.addJob(tdi)
    
    wrf_dat = File("wrf.dat", size=206*MB)
    arps2wrf = Job(id="arps2wrf", namespace="leadmm", name="ARPS2WRF", runtime=78*SECONDS, inputs=[lbio1, tdio1], outputs=[wrf_dat])
    arps2wrf.addParent(lbi)
    arps2wrf.addParent(tdi)
    arps2wrf.addParent(wrfstatic)
    w.addJob(arps2wrf)
    
    wrf_out = File("wrf.dat.out", size=2422*MB)
    wrf = Job(id="wrf", namespace="leadmm", name="WRF", runtime=4570*SECONDS, cores=16, inputs=[wrf_dat], outputs=[wrf_out])
    wrf.addParent(arps2wrf)
    w.addJob(wrf)
    
    w.write(file)

if __name__ == '__main__':
    main("/dev/stdout")
