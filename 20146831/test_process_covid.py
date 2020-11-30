import pytest
from process_covid import load_covid_data,create_confirmed_plot
from pathlib import Path

def test_data_load():
    with pytest.raises(ImportError):
        data_directory = Path("")
        data_file = "Dodgy_data.json"
        data_er = load_covid_data(data_directory / data_file)
        
def test_plot_inputs():
    with pytest.raises(ValueError):
        create_confirmed_plot([3,4,5],sex=True,max_ages=[2,3])
    