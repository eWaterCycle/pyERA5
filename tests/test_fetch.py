"""Tests for era5cli Fetch class."""

from era5cli import fetch


def initialize(outputformat='netcdf', split=True):
    """Initializer of the class."""
    era5 = fetch.Fetch(years=[2008, 2009],
                       months=list(range(1, 13)),
                       days=list(range(1, 32)),
                       hours=list(range(0, 24)),
                       variables=['total_precipitation'],
                       outputformat=outputformat,
                       outputprefix='era5',
                       period='hourly',
                       ensemble=True,
                       statistics=None,
                       synoptic=None,
                       pressurelevels=None,
                       split=split,
                       threads=2)
    return era5


def test_init():
    """Test init function of Fetch class."""
    era5 = fetch.Fetch(years=[2008, 2009],
                       months=list(range(1, 13)),
                       days=list(range(1, 32)),
                       hours=list(range(0, 24)),
                       variables=['total_precipitation'],
                       outputformat='netcdf',
                       outputprefix='era5',
                       period='hourly',
                       ensemble=True,
                       statistics=None,
                       synoptic=None,
                       pressurelevels=None,
                       split=True,
                       threads=2)

    valid_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    assert era5.months == valid_months

    valid_days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                  '31']
    assert era5.days == valid_days

    valid_hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                   '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                   '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                   '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    assert era5.hours == valid_hours

    assert era5.variables == ['total_precipitation']
    assert era5.outputformat == 'netcdf'
    assert era5.outputprefix == 'era5'
    assert era5.period == 'hourly'
    assert era5.ensemble
    assert era5.statistics is None
    assert era5.synoptic is None
    assert era5.pressure_levels is None
    assert era5.split
    assert era5.threads == 2


def test_fetch():
    """Test fetch function of Fetch class."""
    era5 = initialize()
    assert era5.fetch(dryrun=True) is None
    del era5

    era5 = initialize(outputformat='grib', split=False)
    assert era5.fetch(dryrun=True) is None


def test_extension():
    """Test _extension function of Fetch class."""
    era5 = initialize()
    era5._extension()
    assert era5.ext == 'nc'
    del era5
    era5 = initialize(outputformat='grib', split=False)
    era5._extension()
    assert era5.ext == 'grb'


def test_define_outputfilename():
    """Test _define_outputfilename function of Fetch class."""
    era5 = initialize()
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', [2008])
    assert fname == 'era5_total_precipitation_2008_hourly_ensemble.nc'

    era5 = initialize(outputformat='grib', split=False)
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', era5.years)
    assert fname == 'era5_total_precipitation_2008-2009_hourly_ensemble.grb'


def test_product_type():
    """Test _product_type function of Fetch class."""
    era5 = initialize()
    producttype = era5._product_type()
    assert producttype == 'ensemble_members'

    era5.ensemble = False
    producttype = era5._product_type()
    assert producttype == 'reanalysis'

    era5.period = 'monthly'
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis'

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis_by_hour_of_day'

    era5.ensemble = False
    era5.statistics = True
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis_by_hour_of_day'


def test_build_request():
    """Test _build_request function of Fetch class."""
    era5 = initialize()
    (name, request) = era5._build_request('total_precipitation', [2008])
    assert name == 'reanalysis-era5-single-levels'
    req = {'variable': 'total_precipitation', 'year': [2008],
           'product_type': 'ensemble_members',
           'month': ['01', '02', '03', '04', '05', '06',
                     '07', '08', '09', '10', '11', '12'],
           'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09',
                   '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', '23', '24', '25', '26', '27',
                   '28', '29', '30', '31'],
           'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
           'format': 'netcdf'}
    assert request == req