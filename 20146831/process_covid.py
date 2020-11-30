import json
import matplotlib.pyplot as plt

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
    population_age = input_data['region']['population']['age']
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
            nested_dict[pop_age_bin[i]][date] = dat_data[i]/population_age[i]
    
    return nested_dict

def hospital_vs_confirmed(data):
    #Initializae empty lists
    dates_arr = []
    ratios_arr = []
    
    #Extract dates
    dates = data['evolution'].keys()
    #Loop over dates to create list with ratios and list with corresponding dates
    for date in dates:
        dat_data = data['evolution'][date]
        new_hosp = dat_data['hospitalizations']['hospitalized']['new']['all']
        new_cases = dat_data['epidemiology']['confirmed']['new']['all']
        if new_hosp == [] or new_cases == []:
            pass
        else:
            ratio = new_hosp/new_cases
            dates_arr.append(date)
            ratios_arr.append(ratio)
            
    return dates_arr,ratios_arr

def generate_data_plot_confirmed(data, sex, max_age, status):
    """
    At most one of sex or max_age allowed at a time.
    sex: only 'male' or 'female'
    max_age: sums all bins below this value, including the one it is in.
    status: 'new' or 'total' (default: 'total')
    """
    #Initializae empty lists
    dates_arr = []
    conf_arr = []

    if len(sex)>0:
        #Extract dates
        dates = data['evolution'].keys()
        #Loop over dates to create list with cases and list with corresponding dates
        for date in dates:
            dat_data = data['evolution'][date]
            new_confirmed = dat_data['epidemiology']['confirmed']['new'][sex]
            dates_arr.append(date)
            conf_arr.append(new_confirmed)
    
    if max_age>0:
        #Extract dates
        dates = data['evolution'].keys()
        
        pop_age_bin = data['metadata']['age_binning']['population']
        n = 0
        #Loop over dates to create list with ratios and list with corresponding dates
        for i in range(len(pop_age_bin)):
            ages = pop_age_bin[i]
            lower = ages.partition('-')[0]
            upper = ages.partition('-')[2]
            if int(lower) > max_age:
                break

            else:
                n += 1
        for date in dates:
            dat_data = data['evolution'][date]
            new_confirmed = sum(dat_data['epidemiology']['confirmed']['new']['age'][0:n])
            dates_arr.append(date)
            conf_arr.append(new_confirmed)
    return dates_arr,conf_arr
        
def create_confirmed_plot(input_data, sex=False, max_ages=[], status=..., save=...):
    # Check that only sex or age is specified
    bool_1 = sex
    bool_2 = len(max_ages)>0
    if bool_1 & bool_2:
        raise ValueError('Too many inputs only one of sex or max_ages allowed')
       
    fig = plt.figure(figsize=(10, 10))
    
    # Only runs when the sex plot is required
    if sex:
        for sex in ['male', 'female']:
            date,confirmed = generate_data_plot_confirmed(input_data, sex, max_age=0,status=[])
            plt.plot(date, confirmed,label=sex)
    
    # Only runs  when the age plot is required
    if bool_2:
        for age in max_ages:
            date,confirmed = generate_data_plot_confirmed(input_data, sex=[], max_age = age,status=[])
            plt.plot(date, confirmed,label='Age <' +str(age))
    
    fig.autofmt_xdate()  # To show dates nicely
    plt.title('Confirmed cases in ' + str(input_data['region']['name']))
    plt.xlabel('Dates')
    plt.ylabel('Confirmed Cases')
    plt.legend()
    # TODO Change logic to show or save it into a '{region_name}_evolution_cases_{type}.png'
    #      where type may be sex or age
    plt.show()

def compute_running_average(data, window):
    raise NotImplementedError

def simple_derivative(data):
    raise NotImplementedError

def count_high_rain_low_tests_days(input_data):
    raise NotImplementedError
