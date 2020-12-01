import pytest
from process_covid import load_covid_data,create_confirmed_plot,check_age_bins,hospital_vs_confirmed,generate_data_plot_confirmed, compute_running_average
from pathlib import Path
import json

def test_data_load():
    with pytest.raises(ImportError):
        data_directory = Path("")
        data_file = "Dodgy_data.json"
        data_er = load_covid_data(data_directory / data_file)
        
def test_plot_inputs():
    with pytest.raises(ValueError):
        create_confirmed_plot([3,4,5],sex=True,max_ages=[2,3])

def test_age_bins():
    with pytest.raises(ValueError):
        hosp_age_bin = ['0-50','51-74','75-']
        pop_age_bin = ['0-24', '25-49', '50-74', '75-']
        comp = check_age_bins(hosp_age_bin,pop_age_bin)

def test_missing_data_hosp_vs_confirmed():
    data_directory = Path("")
    data_file = "Dodgy_data_2.json"
    data_er = load_covid_data(data_directory / data_file)
    hospital_vs_confirmed(data_er)
    
def test_wrong_input_generate_data_plot_confirmed():
    with pytest.raises(ValueError):
        generate_data_plot_confirmed([3,4,5],sex=[2,3])

def test_compute_running_average():
    with pytest.raises(ValueError):
        compute_running_average([3,4,5,6],window=7.2)
    with pytest.raises(ValueError):
        compute_running_average([3,4,5,6],window=0)