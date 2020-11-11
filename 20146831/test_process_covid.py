import pytest
from process_covid import load_covid_data
from pathlib import Path

def test_data_load():
    with pytest.raises(ImportError):
        data_directory = Path("")
        data_file = "Dodgy_data.json"
        data_er = load_covid_data(data_directory / data_file)