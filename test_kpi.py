import pytest
import konsumer_pris_indeks

def test_gjennomsnitt_kpi_i_år():
    assert konsumer_pris_indeks.gjennomsnitt_kpi_i_år(1954) == 7.1