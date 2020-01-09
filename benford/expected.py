from pandas import DataFrame
from numpy import array, arange, log10
from .checks import _check_digs_
from .viz import _plot_expected_


class First(DataFrame):
    '''
     Returns the expected probabilities of the First, First Two, or
     First Three digits according to Benford's distribution.

    Parameters
    ----------

    digs-> 1, 2 or 3 - tells which of the first digits to consider:
            1 for the First Digit, 2 for the First Two Digits and 3 for
            the First Three Digits.

    plot-> option to plot a bar chart of the Expected proportions.
            Defaults to True.
    '''

    def __init__(self, digs, plot=True):
        _check_digs_(digs)
        dig_name = f'First_{digs}_Dig'
        Dig = arange(10 ** (digs - 1), 10 ** digs)
        Exp = log10(1 + (1. / Dig))

        DataFrame.__init__(self, {'Expected': Exp}, index=Dig)
        self.index.names = [dig_name]

        if plot:
            _plot_expected_(self, digs)


class Second(DataFrame):
    '''
    Returns the expected probabilities of the Second Digits
    according to Benford's distribution.

    Parameters
    ----------

    plot: option to plot a bar chart of the Expected proportions.
        Defaults to True.
    '''
    def __init__(self, plot=True):
        a = arange(10, 100)
        Expe = log10(1 + (1. / a))
        Sec_Dig = array(list(range(10)) * 9)

        df = DataFrame({'Expected': Expe, 'Sec_Dig': Sec_Dig})

        DataFrame.__init__(self, df.groupby('Sec_Dig').sum())

        if plot:
            _plot_expected_(self, 22)


class LastTwo(DataFrame):
    '''
    Returns the expected probabilities of the Last Two Digits
    according to Benford's distribution.

    Parameters
    ----------

    plot: option to plot a bar chart of the Expected proportions.
        Defaults to True.
    '''
    def __init__(self, num=False, plot=True):
        exp = array([1 / 99.] * 100)
        DataFrame.__init__(self, {'Expected': exp,
                              'Last_2_Dig': _lt_(num=num)})
        self.set_index('Last_2_Dig', inplace=True)
        if plot:
            _plot_expected_(self, -2)

def _test_(digs):
    '''
    Returns the base instance for the proper test to be performed
    depending on the digit
    '''
    if digs in [1, 2, 3]:
        return First(digs, plot=False)
    elif digs == 22:
        return Second(plot=False)
    else:
        return LastTwo(num=True, plot=False)


def _lt_(num=False):
    '''
    Creates an array with the possible last two digits

    Parameters
    ----------

    num: returns numeric (ints) values. Defaluts to False,
        which returns strings.
    '''
    if num:
        n = arange(0, 100)
    else:
        n = arange(0, 100).astype(str)
        n[:10] = array(['00', '01', '02', '03', '04', '05',
                           '06', '07', '08', '09'])
    return n