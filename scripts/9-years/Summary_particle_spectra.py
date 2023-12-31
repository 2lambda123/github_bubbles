""" Plots the SED of all latitude stripes necessary to observe the Fermi bubbles. """

import numpy as np
import pyfits
from matplotlib import pyplot
import healpylib as hlib
import dio
from yaml import load
import auxil
from optparse import OptionParser

########################################################################################################################## Parameters

parser = OptionParser()
parser.add_option("-l", "--latitude", dest = "latitude", default = "7", help="latitude (7 = GP)")
parser.add_option("-p", "--particles", dest = "particles", default = "electrons", help="electrons or protons")
(options, args) = parser.parse_args()

latitude = int(options.latitude)
particles = str(options.particles)

fn_ending = ".pdf"
Save_dct = True

Es = 10**np.arange(1,5,0.25)

########################################################################################################################## Constants

#colours = ["blue", "red"]
lowE_ranges = ["0.3-1.0", "0.3-0.5", "0.5-1.0", "1.0-2.2"]

GeV2MeV = 1000.
m2cm = 100
delta = 0.3837641821164575                                                              # logarithmic distance between two energy bins
plot_dir = '../../plots/Plots_9-year/'
speed_of_light = 2.998e+10


dct  = dio.loaddict('dct/Low_energy_range0/dct_boxes_source.yaml')

Lc = dct['3) Center_of_lon_bins']
Bc = dct['4) Center_of_lat_bins']
dL = 10.
dB = [10., 10., 10., 10., 10., 4., 4., 4., 4., 4., 10., 10., 10., 10., 10.]

def plaw(N_0, gamma, Ecut):  # powerlaw
    return lambda E: N_0 * E**(-gamma) * np.exp(-E / Ecut)

########################################################################################################################## Load dictionaries

print "Latitude: ", Bc[latitude]
l = 0
b = latitude



if particles == "electrons": # units: 1/GeVcm^3s
    dct_boxes = dio.loaddict('plot_dct/Low_energy_range0/boxes_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE = dio.loaddict('plot_dct/Low_energy_range0/lowE_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_GALPROP = dio.loaddict('plot_dct/Low_energy_range0/GALPROP_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE1 = dio.loaddict('plot_dct/Low_energy_range1/lowE_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE2 = dio.loaddict('plot_dct/Low_energy_range2/lowE_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE3 = dio.loaddict('plot_dct/Low_energy_range3/lowE_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes1 = dio.loaddict('plot_dct/Low_energy_range1/boxes_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes2 = dio.loaddict('plot_dct/Low_energy_range2/boxes_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes3 = dio.loaddict('plot_dct/Low_energy_range3/boxes_source_IC_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    #HESS_2017 = np.array([])
    #Es_HESS_2017 = np.array([])

else: # units: 1/GeVcm^3s
    
    dct_boxes = dio.loaddict('plot_dct/Low_energy_range0/boxes_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE = dio.loaddict('plot_dct/Low_energy_range0/lowE_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_GALPROP = dio.loaddict('plot_dct/Low_energy_range0/GALPROP_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE1 = dio.loaddict('plot_dct/Low_energy_range1/lowE_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE2 = dio.loaddict('plot_dct/Low_energy_range2/lowE_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_lowE3 = dio.loaddict('plot_dct/Low_energy_range3/lowE_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes1 = dio.loaddict('plot_dct/Low_energy_range1/boxes_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes2 = dio.loaddict('plot_dct/Low_energy_range2/boxes_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')
    dct_boxes3 = dio.loaddict('plot_dct/Low_energy_range3/boxes_source_pi0_cutoff_l=-5.0_b=' + str(Bc[latitude]) + '.yaml')

factor = Es**2 * speed_of_light / 4. / np.pi

print dct_boxes['N_0']
print dct_boxes['gamma']
print dct_boxes['E_cut']

plaw_boxes = factor * plaw(dct_boxes['N_0'], dct_boxes['gamma'], dct_boxes['E_cut'])(Es)
plaw_lowE = factor * plaw(dct_lowE['N_0'], dct_lowE['2) gamma'], dct_lowE['3) E_cut'])(Es)
plaw_GALPROP = factor * plaw(dct_GALPROP['N_0'], dct_GALPROP['2) gamma'], dct_GALPROP['3) E_cut'])(Es)
plaw_boxes1 = factor * plaw(dct_boxes1['N_0'], dct_boxes1['gamma'], dct_boxes1['E_cut'])(Es)
plaw_boxes2 = factor * plaw(dct_boxes2['N_0'], dct_boxes2['gamma'], dct_boxes2['E_cut'])(Es)
plaw_boxes3 = factor * plaw(dct_boxes3['N_0'], dct_boxes3['gamma'], dct_boxes3['E_cut'])(Es)
plaw_lowE1 = factor * plaw(dct_lowE1['N_0'], dct_lowE1['gamma'], dct_lowE1['E_cut'])(Es)
plaw_lowE2 = factor * plaw(dct_lowE2['N_0'], dct_lowE2['gamma'], dct_lowE2['E_cut'])(Es)
plaw_lowE3 = factor * plaw(dct_lowE3['N_0'], dct_lowE3['gamma'], dct_lowE3['E_cut'])(Es)



########################################################################################################################## Plot


auxil.setup_figure_pars(plot_type = 'spectrum')
fig = pyplot.figure()


baseline  = plaw_boxes

syst_max = np.maximum.reduce([plaw_boxes, plaw_lowE, plaw_GALPROP])
syst_min = np.minimum.reduce([plaw_boxes, plaw_lowE, plaw_GALPROP])
#syst_max = np.maximum.reduce([plaw_boxes, plaw_lowE, plaw_GALPROP, plaw_boxes1, plaw_boxes2, plaw_boxes3, plaw_lowE1, plaw_lowE2, plaw_lowE3])
#syst_min = np.minimum.reduce([plaw_boxes, plaw_lowE, plaw_GALPROP, plaw_boxes1, plaw_boxes2, plaw_boxes3, plaw_lowE1, plaw_lowE2, plaw_lowE3])

label = "Excess region"
'''
if particles == "electrons":
    name = 'Summary_electron_spectra_' + str(int(Bc[b]))
    pyplot.plot(Es, baseline, color="green", linewidth=0.9, label=label)
    pyplot.fill_between(Es, syst_min, syst_max, color = "green", alpha = 0.2)

    fermi_LE = np.loadtxt("../../data/Electron_spectra/Fermi_LE_2017").T
    fermi_HE = np.loadtxt("../../data/Electron_spectra/Fermi_HE_2017").T
    fermi_Es = np.append((fermi_LE[0]+fermi_LE[1])/2, (fermi_HE[0]+fermi_HE[1])/2)
    fermi_dNdE = np.append(fermi_LE[4], fermi_HE[4]) * fermi_Es**2 / 100.**2  # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    fermi_err = np.append(np.sqrt(fermi_LE[5]**2+fermi_LE[6]**2), np.sqrt(fermi_HE[5]**2+fermi_HE[6]**2+fermi_HE[7]**2)) * fermi_dNdE # Relative errors (stat + sys)
    pyplot.errorbar(fermi_Es, fermi_dNdE, fermi_err, color = "black", ls = "", marker = "o", label = "Fermi-LAT (2017)")

    HESS_Es, HESS_E3dNdE, HESS_err = np.loadtxt("../../data/Electron_spectra/HESS_2017").T
    HESS_Es *= 1000. # TeV --> GeV
    HESS_E3dNdE /= (100**2 * HESS_Es) # GeV^3/m^2/s/sr --> GeV^2/cm^2/s/sr
    HESS_err /= (100**2 * HESS_Es) # GeV^3/m^2/s/sr --> GeV^2/cm^2/s/sr
    pyplot.errorbar(HESS_Es, HESS_E3dNdE, HESS_err, color = "blue", label = "H.E.S.S. (2017)", ls = "", marker = "s")

    AMS_Es, AMS_dNdE, AMS_stat = np.loadtxt("../../data/Electron_spectra/AMS02_2014")
    AMS_sys_tot = np.loadtxt("../../data/Electron_spectra/ams_electrons_syst.txt").T
    AMS_sys = AMS_sys_tot[0] * 10**AMS_sys_tot[1] 
    AMS_dNdE *= (AMS_Es**2 / 100.**2) # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    AMS_err = np.sqrt(AMS_stat**2 + AMS_sys**2) * (AMS_Es**2 / 100.**2) # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    pyplot.errorbar(AMS_Es, AMS_dNdE, AMS_err, color = "red", ls = "", marker = ">", label = "AMS-02 (2014)")

    pyplot.ylim(3e-8, 3e-2)
'''

if particles == "electrons":                                                        # Older HESS data + DAMPE data
    name = 'Summary_electron_spectra_' + str(int(Bc[b]))
    pyplot.plot(Es, baseline, color="green", linewidth=0.9, label=label)
    pyplot.fill_between(Es, syst_min, syst_max, color = "green", alpha=0.25)

    HESS_data = np.loadtxt("../../data/Electron_spectra/HESS_2008_highE.csv", delimiter=',').T
    HESS_Es = HESS_data[0]
    HESS_E2dNdE = HESS_data[1] / m2cm**2 / HESS_Es
    HESS_syst = (HESS_data[4] - HESS_data[5]) / 2.
    HESS_err_low = np.sqrt(HESS_data[2]**2 + HESS_syst**2) / m2cm**2 / HESS_Es
    HESS_err_up = np.sqrt(HESS_data[3]**2 + HESS_syst**2) / m2cm**2 / HESS_Es
    
    #HESS_Es *= 1000. # TeV --> GeV
    #HESS_E3dNdE /= (100**2 * HESS_Es) # GeV^3/m^2/s/sr --> GeV^2/cm^2/s/sr
    #HESS_err /= (100**2 * HESS_Es) # GeV^3/m^2/s/sr --> GeV^2/cm^2/s/sr
    pyplot.errorbar(HESS_Es, HESS_E2dNdE, yerr=[HESS_err_low, HESS_err_up], color = "blue", label = "H.E.S.S. (2008)", ls = "", marker = "s")

    AMS_Es, AMS_dNdE, AMS_stat = np.loadtxt("../../data/Electron_spectra/AMS02_2014")
    AMS_sys_tot = np.loadtxt("../../data/Electron_spectra/ams_electrons_syst.txt").T
    AMS_sys = AMS_sys_tot[0] * 10**AMS_sys_tot[1] 
    AMS_dNdE *= (AMS_Es**2 / 100.**2) # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    AMS_err = np.sqrt(AMS_stat**2 + AMS_sys**2) * (AMS_Es**2 / 100.**2) # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    pyplot.errorbar(AMS_Es, AMS_dNdE, AMS_err, color = "red", ls = "", marker = ">", label = "AMS-02 (2014)")

    fermi_LE = np.loadtxt("../../data/Electron_spectra/Fermi_LE_2017").T
    fermi_HE = np.loadtxt("../../data/Electron_spectra/Fermi_HE_2017").T
    fermi_Es = np.append((fermi_LE[0]+fermi_LE[1])/2, (fermi_HE[0]+fermi_HE[1])/2)
    fermi_dNdE = np.append(fermi_LE[4], fermi_HE[4]) * fermi_Es**2 / 100.**2  # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    fermi_err = np.append(np.sqrt(fermi_LE[5]**2+fermi_LE[6]**2), np.sqrt(fermi_HE[5]**2+fermi_HE[6]**2+fermi_HE[7]**2)) * fermi_dNdE # Relative errors (stat + sys)
    pyplot.errorbar(fermi_Es, fermi_dNdE, fermi_err, color = "black", ls = "", marker = "o", label = "Fermi-LAT (2017)")


    dampe = np.loadtxt("../../data/Electron_spectra/dampe_electrons.txt").T
    dampe_Es = dampe[2]
    factor = dampe[-1]
    dampe_dNdE = factor * dampe[3] * dampe_Es**2 / m2cm**2  # 1/GeV/m^2/sr/s --> GeV/cm^2/sr/s
    dampe_err = factor * np.sqrt(dampe[4]**2 + dampe[5]**2) * dampe_Es**2 / m2cm**2
    pyplot.errorbar(dampe_Es, dampe_dNdE, dampe_err, color = "magenta", ls = "", marker = "v", label = "DAMPE (2017)")


    pyplot.ylim(3e-8, 3e-2)

else:
    name = 'Summary_proton_spectra_' + str(int(Bc[b]))
    pyplot.plot(Es, baseline, color="brown", linewidth=0.9, label=label)
    pyplot.fill_between(Es, syst_min, syst_max, color = "brown", alpha = 0.2)

    AMS = np.loadtxt("../../data/Proton_spectra/AMS_2015.txt").T
    AMS_Es = (AMS[0] + AMS[1])/2
    AMS_dNdE = AMS[2] * AMS[9] * AMS_Es**2 /100.**2
    AMS_err = np.sqrt(AMS[3]**2 + AMS[8]**2)  * AMS[9] * AMS_Es**2 /100.**2 #stat + total syst error

    pyplot.errorbar(AMS_Es, AMS_dNdE, AMS_err, color = "green", ls = "", marker = "d", label = "AMS-02 (2015)")
    pyplot.ylim(4e-3,1e0)


########################################################################################################################## Cosmetics, safe plot

    
lg = pyplot.legend(loc='upper right', ncol=1)
lg.get_frame().set_linewidth(0)
pyplot.grid(True)
pyplot.xlabel('$E\ \mathrm{[GeV]}$')

ax = fig.add_subplot(111)
props = dict( facecolor='white', alpha=1, edgecolor = "white")
textstr = r'$\ell \in (%i^\circ$' % (Lc[l] - dL/2) + '$,\ %i^\circ)$\n' % (Lc[l] + dL/2) + r'$b \in (%i^\circ$' % (Bc[b] - dB[b]/2) + '$,\ %i^\circ)$' % (Bc[b] + dB[b]/2)
ax.text(0.03, 0.15, textstr, transform=ax.transAxes, fontsize = 20, verticalalignment='top', bbox=props)

if particles == "electrons":
    pyplot.ylabel(r'$ E^2\phi_\mathrm{e}\ \left[ \frac{\mathrm{GeV}}{\mathrm{cm^2\ s\ sr}} \right]$')
else:
    pyplot.ylabel(r'$ E^2\phi_\mathrm{p}\ \left[ \frac{\mathrm{GeV}}{\mathrm{cm^2\ s\ sr}} \right]$')
pyplot.xlim(1e1,1e5)

fn = plot_dir + name + fn_ending
pyplot.xscale('log')
pyplot.yscale('log')
#pyplot.ylim((1.e-8,4.e-4))
pyplot.savefig(fn, format = 'pdf')

if Save_dct:
    dct = {"x: energies" : Es}
    if particles == "electrons":
        dct_fn = "plot_dct/Low_energy_range0/Summary_electron_spectrum_source_plaw_l=" + str(Lc[l]) + "_b=" + str(Bc[b])  + ".yaml"
        dct["Comment: "] = "Min and max best-fit electron spectra assuming a lecptonic scenario for the different models (taking only the baseline low-energy range into account)."
    else:
        dct_fn = "plot_dct/Low_energy_range0/Summary_proton_spectrum_source_plaw_l=" + str(Lc[l]) + "_b=" + str(Bc[b])  +  ".yaml"
        dct["Comment: "] = "Min and max best-fit proton spectra assuming a hadronic scenario for the different models (taking only the baseline low-energy range into account)."
        
    dct["y: flux_max"] = np.array(syst_max)
    dct["y: flux_min"] = np.array(syst_min)
    dio.saveyaml(dct, dct_fn, expand = True)

