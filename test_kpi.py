import pytest
import konsumer_pris_indeks


@pytest.fixture
def kpis():
   return konsumer_pris_indeks.lager_KPI_objekt_list_fra_data()

def test_gjennomsnitt_kpi_i_år(kpis):
    assert konsumer_pris_indeks.gjennomsnitt_kpi_i_år(1954, kpis) == 7.1

def test_pris_i_annet_år(kpis):
    assert round(konsumer_pris_indeks.pris_i_annet_år(2010,2000,45, kpis),2) == 54.89 