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
    comp = False
    if hosp_age_bin == pop_age_bin:
        pass
    else:
        comp = check_age_bins(hosp_age_bin,pop_age_bin)
    
    population_age = input_data['region']['population']['age']
    #Initialize empty dictionary
    nested_dict = {}
    for i in range(len(pop_age_bin)):
        #Add layer for each age bin
        nested_dict[pop_age_bin[i]] = {}
    
    #Extract dates
    dates = input_data['evolution'].keys()
    
    #Check whether rebinning is needed
    if comp:
        #Loop over dates to extract age binned data
        for date in dates:
            dat_data = input_data['evolution'][date]['epidemiology']['confirmed']['total']['age']

            for i in range(len(pop_age_bin)):
                #Rebin data here
                nested_dict[pop_age_bin[i]][date] = dat_data[i]/population_age[i]
    else:
        #Loop over dates to extract age binned data
        for date in dates:
            dat_data = input_data['evolution'][date]['epidemiology']['confirmed']['total']['age']

            for i in range(len(pop_age_bin)):
                #Rebin data here
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

def generate_data_plot_confirmed(data, sex, max_age, status='total'):
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
            new_confirmed = dat_data['epidemiology']['confirmed'][status][sex]
            dates_arr.append(date)
            conf_arr.append(new_confirmed)
    
    elif max_age>0:
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
            new_confirmed = sum(dat_data['epidemiology']['confirmed'][status]['age'][0:n])
            dates_arr.append(date)
            conf_arr.append(new_confirmed)
    
    return dates_arr,conf_arr
        
def create_confirmed_plot(input_data, sex=False, max_ages=[], status='total', save=False):
    # Check that only sex or age is specified
    bool_1 = sex
    bool_2 = len(max_ages)>0
    if bool_1 & bool_2:
        raise ValueError('Too many inputs only one of sex or max_ages allowed')
    
    if status == 'new':
        line_style = '--'
    elif status == 'total' or 'confirmed':
        line_style = '-'
    fig = plt.figure(figsize=(10, 10))
    
    # Only runs when the sex plot is required
    if sex:
        type_plot = 'sex'
        for sex in ['male', 'female']:
            date,confirmed = generate_data_plot_confirmed(input_data, sex, max_age=0,status=status)
            if sex == 'male':
                plt.plot(date, confirmed,label=str(status)+' '+str(sex),color='green', ls=line_style)
            elif sex == 'female':
                plt.plot(date, confirmed,label=str(status)+' '+str(sex),color='purple',ls=line_style)
    
    # Only runs  when the age plot is required
    if bool_2:
        type_plot = 'max_age'
        for age in max_ages:
            date,confirmed = generate_data_plot_confirmed(input_data, sex=[], max_age = age,status=status)
            if age <= 25:
                plt.plot(date, confirmed,label=str(status)+' Age <' +str(age),color='green',ls=line_style)
            elif age <= 50:
                plt.plot(date, confirmed,label=str(status)+' Age <'+str(age),color='orange',ls=line_style)
            elif age <= 75:
                plt.plot(date, confirmed,label=str(status)+' Age <'+str(age),color='purple',ls=line_style)
            else:
                plt.plot(date, confirmed,label=str(status)+' Age <'+str(age),color='pink',ls=line_style)
                
    fig.autofmt_xdate()  # To show dates nicely
    plt.title('Confirmed cases in ' + str(input_data['region']['name']))
    plt.xlabel('Dates')
    plt.ylabel('Confirmed Cases')
    plt.legend()
    if save:
        plt.savefig(str(input_data['region']['name'])+'_evolution_cases_'+str(type_plot)+'.png')
    plt.show()

def compute_running_average(input_data, window):
    if (a%2) == 0:
        raise ValueError('Window must be an odd number')
    else:
        means = []
        each_side = int((window_size-1)/2)
        if input_data.count(None) == 0:
            pass
        else:
            input_data = [0 if x is None else x for x in input_data]
        
        for i in range(len(input_data)+1):
            data = input_data[(i-each_side):(i+each_side+1)]
            if len(data)< window_size:
                means.append(None)
            else:
                mean = sum(data)/len(data)
                    means.append(mean)
    return means

def simple_derivative(data):
    deriv = []

    for i in range(len(input_data)):
        data = input_data[i-1:i+1]
        if data.count(None)>= 1:
            deriv.append(None)
        elif len(data)<1:
            deriv.append(None)
        else:
            deriv.append(data[1]-data[0])
    return deriv

def count_high_rain_low_tests_days(input_data):
    raise NotImplementedError

def check_age_bins(hosp_age_bin,pop_age_bin):
    lower_hosp = []
    upper_hosp = []

    lower_pop = []
    upper_pop = []

    if hosp_age_bin == pop_age_bin:
        pass
    else:
        for i in range(len(pop_age_bin)):
            a = pop_age_bin[i].partition('-')

            try:
                lower_pop.append(int(a[0]))
                upper_pop.append(int(a[2]))
            except ValueError:
                break
        for i in range(len(hosp_age_bin)):
            a = hosp_age_bin[i].partition('-')

            try:                             
                lower_hosp.append(int(a[0]))
                upper_hosp.append(int(a[2]))
            except ValueError:
                break

    if len(hosp_age_bin)>len(pop_age_bin):
        if len(set(lower_pop) & set(lower_hosp)) == len(lower_pop) or len(set(upper_pop) & set(upper_hosp)) == len(upper_pop):
            print('Compatible')
            status = True
        else:
            raise ValueError('Age bins incompatible')
    elif len(hosp_age_bin)<len(pop_age_bin):
        if len(set(lower_pop) & set(lower_hosp)) == len(lower_hosp) or len(set(upper_pop) & set(upper_hosp)) == len(upper_hosp):
            print('Compatible')
            status = True
        else:
            raise ValueError('Age bins incompatible')
    return status
