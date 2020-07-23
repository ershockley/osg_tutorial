import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from multihist import Hist1d
from LowER.sciencerun import SR1
import LowER.stats as lstat
from LowER.signals import SolarAxion


def main():
    # this is setting up LowER likelihood
    # there is no partitioning here -- just a single SR1 likelihood

    print("Setting up the likelihood...")
    sr1 = SR1()

    # axion signal model. this is ABC-only
    A = SolarAxion(1e-3, gae=3.5e-12)

    # initialize the likelihood
    lf = lstat.sciencerun_likelihood(sr1, A)

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


if __name__ == "__main__":
    main()
