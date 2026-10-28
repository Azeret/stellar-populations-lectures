"""Run one galevo model in its own copy of galIMF and save the key tracks to .npz.
usage: python run_galevo.py <label> <imf: Kroupa|igimf> <log_SFR> <SFEN (x10 Myr)>"""
import sys, os, shutil, time, json
import numpy as np
label, imf, logsfr, sfen = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
src = '/home/claude/ext/galIMF'
wd = f'/home/claude/work/runs/{label}'
if os.path.exists(wd): shutil.rmtree(wd)
shutil.copytree(src, wd)
os.chdir(wd); sys.path.insert(0, wd)
import galevo
t = time.time()
galevo.generate_SFH('flat', logsfr, sfen, 0, 10, 0)
galevo.galaxy_evol(imf=imf, STF=0.3, SFEN=sfen, Z_0=0.00000001886, solar_mass_component="Anders1989_mass",
    str_yield_table='portinari98', IMF_name='Kroupa', steller_mass_upper_bound=150, time_resolution_in_Myr=1,
    mass_boundary_observe_low=1.5, mass_boundary_observe_up=8, SFH_model='provided', SNIa_ON=True,
    high_time_resolution=None, plot_show=None, plot_save=None, outflow=None, check_igimf=False)
keys = ['time_axis','Fe_over_H_list','Mg_over_Fe_list','O_over_Fe_list','Mg_over_H_list','gas_Z_over_X_list',
        'stellar_Fe_over_H_list','stellar_Mg_over_Fe_list','total_star_formed']
out = {}
for k in keys:
    v = getattr(galevo, k, None)
    if v is not None:
        try: out[k] = np.array(v, dtype=float)
        except Exception: pass
np.savez(f'/home/claude/work/runs/{label}.npz', imf=imf, logsfr=logsfr, sfen=sfen, **out)
print(label, 'done in', round(time.time()-t,1), 's')
