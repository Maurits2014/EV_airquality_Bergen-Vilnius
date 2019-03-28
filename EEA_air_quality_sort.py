#!/usr/bin/python3

# filename    : EEA_air_quality_scrape.py
# description : scrape weather station data data from various EEA data sets to a csv
# developer   : Maurits Pullen, s3498638
# date        : 2019-03-23

# Operating system: Arch Linux 4.14.87-1-lts
# python 3.7.1-1
# pandas 0.24.2
# scipy 1.2.1

# Standard library imports
import sys
import csv
import xml.etree.ElementTree as ET

# Third party imports
import pandas as pd
from scipy import stats


def scrape_xml_AirBase_v4():
    """scrape weather station data from AirBase v4 xml data set"""
    f = open("mean_1318.csv", "a+")
    f_csv = csv.writer(f, delimiter=",")
    # filename:station LocalID
    filename_wstation_dict = {"NO_meta.xml":"NO0059A:Danmarksplass", "LT_meta.xml":"LT00001:Vilnius - Senamiestis"}
    f_csv.writerow(["wstation","year","mean"])
    for filename in filename_wstation_dict:
        xml_tree = ET.parse(filename)
        xmlFile = xml_tree.getroot()
        for year in xmlFile.findall("./country/station[@Id='%s']/measurement_configuration[@component='Nitrogen dioxide (air) - chemiluminescence']/statistics[@Year]" % filename_wstation_dict[filename]):
            for mean in year.findall("./statistics_average_group[@value='hour']/statistic_set[@type='General']/statistic_result/statistic_shortname[.='Mean']/.."):
                f_csv.writerow([filename_wstation_dict[filename][0:7], str(year.attrib["Year"]), str(mean.find("./statistic_value").text)])
    f.close()


def scrape_csv_E1a_E2a():
    """scrape weather station data from EEA E1a and E2a data sets"""
    # write 2013-2018 mean values to mean_1318.csv file
    f = open("mean_1318.csv", "a+")
    f_csv = csv.writer(f, delimiter=",")
    csv_wstation_dict = {"NO_8_28803":"NO0059A", "LT_8_27077":"LT00001"}
    for country in csv_wstation_dict:
        # E1a and E2a are encoded with UTF-16
        for year in ["2013", "2014", "2015", "2016", "2017", "2018"]:
            csvv = open("%s_%s_timeseries.csv" % (country, year), "r", encoding="utf-16")
            csv_panda = pd.read_csv(csvv)
            f_csv.writerow([csv_wstation_dict[country], year, str(round(csv_panda["Concentration"].mean(), 3))])
            csvv.close()
    f.close()


def r_p_values():
    """calculate statistic pearson r and p values"""
    f = open("number_EVs_annual.csv", "r")
    f_panda = pd.read_csv(f)
    f2 = open("mean_1318_sort.csv", "r")
    f2_panda = pd.read_csv(f2)
    print("Norway r and p values:", stats.pearsonr((f_panda["number"].loc[f_panda["country"]=="Norway"]), (f2_panda["mean"].loc[f2_panda["wstation"]=="NO0059A"])))
    print("Lithiania r and p values:", stats.pearsonr((f_panda["number"].loc[f_panda["country"]=="Lithuania"]), (f2_panda["mean"].loc[f2_panda["wstation"]=="LT00001"])))
    f.close()
    f2.close()
    

def main():
    scrape_xml_AirBase_v4()
    scrape_csv_E1a_E2a()
    r_p_values()


if __name__ == "__main__":
    main()
