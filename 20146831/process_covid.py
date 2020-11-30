import json

def load_covid_data(filepath):
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    
    #Check the loaded dataset has the correct keys
    if set(['evolution', 'metadata', 'region']) == set(data.keys()) and set(data.get('metadata').keys()) == set(['time-range', 'age_binning']) and set(data.get('region').keys()) == set(['name', 'key', 'latitude', 'longitude', 'elevation', 'area', 'population', 'open_street_maps', 'noaa_station', 'noaa_distance']) :
        pass
    else:
        #Raise error if incorrect keys
        raise ImportError('Incorrect keys in .json file')
    return(data)

def cases_per_population_by_age(input_data):
    #Check the binning of hospitalization and population
    hosp_age_bin = input_data['metadata']['age_binning']['hospitalizations']
    pop_age_bin = input_data['metadata']['age_binning']['population']
    
    #Initialize empty dictionary
    nested_dict = {}
    for i in range(len(pop_age_bin)):
        #Add layer for each age bin
        nested_dict[pop_age_bin[i]] = {}
    
    #Extract dates
    dates = input_data['evolution'].keys()
    #Loop over dates to extract age binned data
    for date in dates:
        dat_data = input_data['evolution'][date]['epidemiology']['confirmed']['total']['age']

        for i in range(len(pop_age_bin)):
            nested_dict[pop_age_bin[i]][date] = dat_data[i]
    
    return nested_dict

def hospital_vs_confirmed(input_data):
    raise NotImplementedError

def generate_data_plot_confirmed(input_data, sex, max_age, status):
    """
    At most one of sex or max_age allowed at a time.
    sex: only 'male' or 'female'
    max_age: sums all bins below this value, including the one it is in.
    status: 'new' or 'total' (default: 'total')
    """
    raise NotImplementedError

def create_confirmed_plot(input_data, sex=False, max_ages=[], status=..., save=...):
    # FIXME check that only sex or age is specified.
    fig = plt.figure(figsize=(10, 10))
    # FIXME change logic so this runs only when the sex plot is required
    for sex in ['male', 'female']:
        # FIXME need to change `changeme` so it uses generate_data_plot_confirmed
        plt.plot('date', 'value', changeme)
    # FIXME change logic so this runs only when the age plot is required
    for age in max_ages:
        # FIXME need to change `changeme` so it uses generate_data_plot_confirmed
        plt.plot('date', 'value', changeme)
    fig.autofmt_xdate()  # To show dates nicely
    # TODO add title with "Confirmed cases in ..."
    # TODO Add x label to inform they are dates
    # TODO Add y label to inform they are number of cases
    # TODO Add legend
    # TODO Change logic to show or save it into a '{region_name}_evolution_cases_{type}.png'
    #      where type may be sex or age
    plt.show()

def compute_running_average(data, window):
    raise NotImplementedError

def simple_derivative(data):
    raise NotImplementedError

def count_high_rain_low_tests_days(input_data):
    raise NotImplementedError
