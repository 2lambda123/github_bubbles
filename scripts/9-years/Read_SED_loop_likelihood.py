""" Plots the SED of all latitude stripes necessary to observe the Fermi bubbles. """

import numpy as np
import pyfits
import healpy
from matplotlib import pyplot
import healpylib as hlib
from iminuit import Minuit
from optparse import OptionParser
import dio
from yaml import load
import gamma_spectra
import auxil

########################################################################################################################## Parameters

fit_plaw = True
fit_IC  = True
fit_pi0 = True



parser = OptionParser()
parser.add_option("-c", "--data_class", dest = "data_class", default = "source", help="data class (source or ultraclean)")
parser.add_option("-E", "--lowE_range", dest="lowE_range", default='0', help="There are 3 low-energy ranges: (3,5), (3,3), (4,5), (6,7)")
parser.add_option("-i", "--input_data", dest="input_data", default="boxes", help="Input data can be: data, lowE, boxes, GALPROP")
parser.add_option("-o", "--cutoff", dest="cutoff", default="True", help="Write True if you want cutoff")
(options, args) = parser.parse_args()

data_class = str(options.data_class)
low_energy_range = int(options.lowE_range) # 0: baseline, 4: test
input_data = str(options.input_data) # data, lowE, boxes, GALPROP

cutoff = False
if str(options.cutoff) == "True":
    cutoff = True

########################################################################################################################## Constants

lowE_ranges = ["0.3-1.0", "0.3-0.5", "0.5-1.0", "1.0-2.2"]
colours = ['blue', 'red']

fn_ending = '.pdf'
if cutoff:
    fn_ending = 'cutoff.pdf'

dL = 10.
dB = [10., 10., 10., 10., 10., 4., 4., 4., 4., 4., 10., 10., 10., 10., 10.]

GeV2MeV = 1000.
delta = 0.3837641821164575                                                              # logarithmic distance between two energy bins
plot_dir = '../../plots/Plots_9-year/Low_energy_range' + str(low_energy_range) +'/'

c_light = 2.9979e8                                                                      # m/s speed of light
h_Planck = 4.1357e-15                                                                   # eV * s Planck constant
kB = 8.6173303e-5                                                                       # eV/K
T_CMB = 2.73 * kB                                                                       # CMB temperature

ISFR_heights = [10, 10, 5, 5, 2, 1, 0.5, 0, 0.5, 1, 2, 5, 5, 10, 10]
E_e = 10.**np.arange(-1., 8.001, 0.1)                                                   # Electron-energies array (0.1 - 10^8 GeV)
p_p = 10.**np.arange(-0.5, 6., 0.1)                                                     # Proton-momenta array



########################################################################################################################## Load dictionaries

dct  = dio.loaddict('dct/Low_energy_range' + str(low_energy_range) +'/dct_' + input_data + '_counts_' + data_class + '.yaml')

Lc = dct['3) Center_of_lon_bins']
Bc = dct['4) Center_of_lat_bins']

Es = np.asarray(dct['5) Energy_bins'])
diff_profiles = dct['6) Differential_flux_profiles']
std_profiles = dct['7) Standard_deviation_profiles']

nB = len(diff_profiles)
nL = len(diff_profiles[0])
nE = len(diff_profiles[0][0])
print 'nB, nL, nE = ' + str(nB) + ', ' + str(nL) + ', ' + str(nE)



expo_dct = dio.loaddict('dct/Low_energy_range' + str(low_energy_range) +'/dct_expo_' + data_class + '.yaml')
exposure_profiles = expo_dct['6) Exposure_profiles'] # shape: (nB, nL, nE)
print "expo_profiles shape: " + str(len(exposure_profiles)) + ", " + str(len(exposure_profiles[0])) + ", " + str(len(exposure_profiles[0][0]))
deltaE = expo_dct['8) deltaE']
dOmega = expo_dct['7) dOmega_profiles']


########################################################################################################################## Read SED from dcts and plot

for b in [6,7,8]: #xrange(nB)
    auxil.setup_figure_pars(plot_type = 'spectrum')
    pyplot.figure()
    colour_index = 0
    
    for l in xrange(nL):
        
        map  = np.asarray(diff_profiles[b][l])
        std_map = np.asarray(std_profiles[b][l])
        expo_map = np.asarray(exposure_profiles[b][l])
                
        label = r'$\ell \in (%i^\circ$' % (Lc[l] - dL/2) + r', $%i^\circ)$' % (Lc[l] + dL/2)
        flux_map = map * Es**2 / dOmega[b][l] / deltaE / expo_map
        flux_std_map = std_map * Es**2 / dOmega[b][l] / deltaE / expo_map

        pyplot.errorbar(Es, flux_map, flux_std_map, color=colours[colour_index], marker='s', markersize=4, markeredgewidth=0.4, linestyle = '', label=label)


########################################################################################################################## Fit spectra



        if fit_plaw:
            if cutoff:
                dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_Plaw_cutoff_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                x, y = dct["x"], dct["y"]                
                N_0, gamma, E_cut  = dct["1) N_0"], dct["2) gamma"], dct["3) E_cut"]
                chi2_dof, TS = dct["chi^2/d.o.f."], dct["-logL"]
                # gamma is saved as spectral index of dN/dE
                if E_cut > 10000: # 10 TeV
                    label = r'$\mathrm{PL}:\ \gamma = %.2f$ ' %(gamma)
                elif E_cut > 1000:
                    label = r'$\mathrm{PL}:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.1f\ \mathrm{TeV}$ ' %(E_cut/1000)
                else:
                    label = r'$\mathrm{PL}:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.2f\ \mathrm{TeV}$ ' %(E_cut/1000)
                pyplot.errorbar(x, y, label = label, color = colours[colour_index])

            else:
                dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_Plaw_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                x, y = dct["x"], dct["y"]                
                N_0, gamma = dct["N_0"], dct["2) gamma"]
                chi2_dof, TS = dct["chi^2/d.o.f."], dct["-logL"]
                label = r'$\mathrm{PL}:\ \gamma = %.2f$ ' %(gamma)  #+ ',\n' + r'$-\log L = %.2f$' %TS + r', $\frac{\chi^2}{\mathrm{d.o.f.}} = %.2f$' %(chi2_dof)
                pyplot.errorbar(x, y, label = label, color = colours[colour_index])
                  
                 


        if fit_IC:
            if cutoff:
                dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_IC_cutoff_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                x, y = dct["x"], dct["y"]                
                N_0, gamma, E_cut  = dct["N_0"], dct["2) gamma"], dct["3) E_cut"]
                chi2_dof, TS = dct["chi^2/d.o.f."], dct["-logL"]
                # gamma is spectral index of EdN/dE
                if E_cut > 10000: # 10 TeV
                    label = r'$\mathrm{IC}:\ \gamma = %.2f$ ' %(gamma)
                elif E_cut > 1000:
                    label = r'$\mathrm{IC}:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.1f\ \mathrm{TeV}$ ' %(E_cut/1000)
                else:
                    label = r'$\mathrm{IC}:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.2f\ \mathrm{TeV}$ ' %(E_cut/1000)
                pyplot.errorbar(x, y, label = label, color = colours[colour_index], ls = '--')

            else:
                print 'plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_IC_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml'
                IC_dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_IC_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                IC_x, IC_y = IC_dct["x"], IC_dct["y"]                
                N_0, gamma = IC_dct["N_0"], IC_dct["gamma"]
                chi2_dof, TS = IC_dct["chi^2/d.o.f."], IC_dct["-logL"]
                # gamma is spectral index of dN/dp
                label = r'$\mathrm{IC}:\ \gamma = %.2f$ ' %(gamma+1)  #+ ',\n' + r'$-\log L = %.2f$' %TS + r', $\frac{\chi^2}{\mathrm{d.o.f.}} = %.2f$' %(chi2_dof)
                pyplot.errorbar(IC_x, IC_y, label = label, color = colours[colour_index], ls = '--')
            

            


            

        if fit_pi0:
            if cutoff:
                dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_pi0_cutoff_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                x, y = dct["x"], dct["y"]                
                N_0, gamma, E_cut  = dct["N_0"], dct["2) gamma"], dct["3) E_cut"]
                chi2_dof, TS = dct["chi^2/d.o.f."], dct["-logL"]

                if E_cut > 10000: # 10 TeV
                    label = r'$\pi^0:\ \gamma = %.2f$ ' %(gamma)
                elif E_cut > 1000:
                    label = r'$\pi^0:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.1f\ \mathrm{TeV}$ ' %(E_cut/1000)
                else:
                    label = r'$\pi^0:\ \gamma = %.2f,$ ' %(gamma) + r'$E_{\mathrm{cut}} = %.2f\ \mathrm{TeV}$ ' %(E_cut/1000)
                pyplot.errorbar(x, y, label = label, color = colours[colour_index], ls = ':')

            else:
                dct = dio.loaddict('plot_dct/Low_energy_range' + str(low_energy_range) +'/' + input_data + '_'  + data_class + '_pi0_l=' + str(Lc[l]) +'_b=' + str(Bc[b]) + '.yaml')
                x, y = dct["x"], dct["y"]                
                N_0, gamma = dct["N_0"], dct["gamma"]
                chi2_dof, TS = dct["chi^2/d.o.f."], dct["-logL"]
                label = r'$\pi^0:\ \gamma = %.2f$ ' %(gamma)  #+ ',\n' + r'$-\log L = %.2f$' %TS + r', $\frac{\chi^2}{\mathrm{d.o.f.}} = %.2f$' %(chi2_dof)
                pyplot.errorbar(x, y, label = label, color = colours[colour_index], ls = ':')

                
        colour_index += 1
        

                    
########################################################################################################################## Cosmetics, safe plot

       
    lg = pyplot.legend(loc='upper left', ncol=2)
    lg.get_frame().set_linewidth(0)
    pyplot.grid(True)
    pyplot.xlabel('$E\ \mathrm{[GeV]}$')
    pyplot.ylabel(r'$ E^2\frac{\mathrm{d}N}{\mathrm{d}E}\ \left[ \frac{\mathrm{GeV}}{\mathrm{cm^2\ s\ sr}} \right]$')
    pyplot.title(r'$b \in (%i^\circ$' % (Bc[b] - dB[b]/2) + ', $%i^\circ)$' % (Bc[b] + dB[b]/2))

    name = 'SED_'+ input_data +'_' + data_class + '_' + str(int(Bc[b]))
    fn = plot_dir + name + fn_ending
    pyplot.xscale('log')
    pyplot.yscale('log')
    pyplot.ylim((5.e-8,4.e-4))
    pyplot.savefig(fn, format = 'pdf')


