import matplotlib
matplotlib.use('Agg')
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
from multihist import Hist1d
from blueice.inference import bestfit_scipy
from LowER.sciencerun import SR1
import LowER.stats as lstat
from LowER.signals import SolarAxion
from tqdm import tqdm


def bestfit():
    """Second example in osg_tutorial"""

    # this is setting up LowER likelihood
    # there is no partitioning here -- just a single SR1 likelihood

    print("Setting up the likelihood...")
    sr1 = SR1()

    # axion signal model. this is ABC-only
    A = SolarAxion(1e-3, gae=3.5e-12)

    # initialize the likelihood
    lf = lstat.sciencerun_likelihood(sr1, A)

    print("Simulating dataset")
    # simulate a fake dataset
    data = lf.base_model.simulate()

    # feed the data to the likelihood
    lf.set_data(data)

    # now do a fit.
    # we use a convenience function that get best-fit, null-fit, and likelihood ratio b/t the two
    llr, bestfit, nullfit = lstat.ll_ratio(lf, 'solar_axion')

    # get significance of this sim using Wilk's theorem
    print("Background model rejected at %0.2f sigma" % (llr**0.5))

    # create histogram objects from best/null fit results
    bestfit_hist = lstat.get_fit(lf, bestfit)
    nullfit_hist = lstat.get_fit(lf, nullfit)

    # plot the data, best-fit, and null-fit
    h = Hist1d(data['ces'], bins=np.linspace(0, 30, 31))

    f = plt.figure()
    h.plot(errors=True, label='sim data')
    bestfit_hist.plot(label='best-fit')
    nullfit_hist.plot(label='null-fit')
    plt.xlim(0, 30)
    plt.ylim(0, max(h.histogram) + 20)
    plt.xlabel("Energy [keV]")
    plt.ylabel('events/keV')
    plt.legend()
    plt.title("Simulating axions on OSG")
    plt.savefig('my_axion_fit.png', dpi=300)


def upper_limit(index=None):
    """Second example in osg_tutorial
    :arg index: If passed, tags an index onto the output filename
    """

    # this is setting up LowER likelihood
    # there is no partitioning here -- just a single SR1 likelihood

    print("Setting up the likelihood...")
    sr1 = SR1()
    # remove a few sources, this helps the sims go faster
    for source in ['kr83m', 'xe131m', 'i125', 'dec']:
        sr1.remove_source(source)

    # axion signal model. this is ABC-only
    A = SolarAxion(1e-3, gae=3.5e-12)

    # initialize the likelihood
    lf = lstat.sciencerun_likelihood(sr1, A)

    nsims = 20

    limits = np.zeros(nsims)

    print("Simulating datasets")

    for i in tqdm(range(nsims)):
        # simulate a fake dataset, with axion signal = 0
        #  for a background-only simulation
        data = lf.base_model.simulate({'solar_axion': 0})

        # feed the data to the likelihood
        lf.set_data(data)

        # get upper limit on the axion rate multiplier parameter. this assumes Wilk's theorem.
        limits[i] = lf.one_parameter_interval('solar_axion_rate_multiplier', 100, bestfit_routine=bestfit_scipy,
                                               minimize_kwargs=lstat.minimize_kwargs)

    # convert limits back to limit on the axion coupling
    glimits = A.convert_limit(limits)

    output_file = "limits.npy"
    if index is not None:
        output_file = output_file.replace('.npy', '_%d.npy' % index)

    np.save(output_file, glimits)
    print("Output saved to %s" % output_file)



def main():

    parser = ArgumentParser()
    parser.add_argument('example', type=int)
    parser.add_argument('--index', type=int)

    args = parser.parse_args()

    if args.example == 1:
        bestfit()

    elif args.example == 2:
        upper_limit(args.index)


if __name__ == "__main__":
    main()
