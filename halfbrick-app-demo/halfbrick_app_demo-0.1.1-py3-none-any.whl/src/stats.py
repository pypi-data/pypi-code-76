import argparse
import csv
from datetime import datetime
import numpy as np
import pandas as pd
from dask import dataframe as dd
from dask.array import from_array as fa
from .utils import *

class Stats():
    def init_location(self, args):
        if args.filter_country is None:
            return ([], [], [], [], [], [], [])
        items = args.filter_country[0].lower().split(',')
        countries = set()
        regions = set()
        cities = set()
        country_region = set()
        country_city = set()
        region_city = set()
        country_region_city = set()
        for item in items:
            country, region, city = item.split('-')
            if country == '':
                if region == '':
                    cities.add(city)
                elif city == '':
                    regions.add(region)
                else:
                    region_city.add((region,city))
            else:
                if region == '' and city == '':
                    countries.add(country)
                elif region == '':
                    country_city.add((country,city))
                elif city == '':
                    country_region.add((country,region))
                else:
                    country_region_city.add((country,region,city))
        return (countries, regions, cities, country_region, country_city, region_city, country_region_city)
        
    def init_names(self, args):
        l = list()
        if args.filter_by_name is None:
            return None
        for a in args.filter_by_name[0].split(';'):
            items = a.split(',')
            l.append((items[0],set(x.lower() for x in items[1:])))
        return l
            
    def __init__(self, args, sep=',', blocksize=64000000):
        self.csvFilePath = args.input[0]
        if args.group_by is not None:
            self.group_by = args.group_by[0].split(',')
        else:
            args.group_by = None
        if args.start is not None:
            self.start_time = pd.to_datetime(args.start[0])
        else:
            self.start_time = None
        if args.end is not None:
            self.end_time = pd.to_datetime(args.end[0])
        else:
            self.end_time = None
        if args.blocksize is not None and args.sep is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=args.sep[0], 
                header=0, blocksize=args.blocksize[0], 
                dtype={'geo_city': 'object'}, 
                parse_dates=['timestamp_raw', 'table_date'])
        elif args.blocksize is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=sep, 
                    header=0, blocksize=args.blocksize[0], 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        elif args.sep is not None:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=args.sep[0], 
                    header=0, 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        else:
            self.dfd = dd.read_csv(self.csvFilePath, delimiter=sep, 
                    header=0, 
                    dtype={'geo_city': 'object'}, 
                    parse_dates=['timestamp_raw', 'table_date'])
        if args.filter_country is not None:
            self.countries, self.regions, self.cities, self.country_region, self.country_city, self.region_city, self.country_region_city = self.init_location(args)
        else:
            self.countries = None
        self.filter_names = self.init_names(args)
        
    def filter_by_country_region_city(self):
        self.dfd = self.dfd.fillna('')
        country_region = len(self.country_region) != 0
        country_city = len(self.country_city) != 0
        region_city = len(self.region_city) != 0
        country_region_city = len(self.country_region_city) != 0
        if country_region and country_city and region_city and country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["region_city"].isin(self.region_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region','country_city','region_city','country_region_city'], axis=1)
        elif not country_region and country_city and region_city and country_region_city:
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["region_city"].isin(self.region_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_city','region_city','country_region_city'], axis=1)
        elif country_region and not country_city and region_city and country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["region_city"].isin(self.region_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region','region_city','country_region_city'], axis=1)
        elif country_region and country_city and not region_city and country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region','country_city','country_region_city'], axis=1)
        elif country_region and country_city and region_city and not country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["region_city"].isin(self.region_city)]
            self.dfd = self.dfd.drop(['country_region','country_city','region_city'], axis=1)
        elif country_region and country_city and not region_city and not country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["country_city"].isin(self.country_city)]
            self.dfd = self.dfd.drop(['country_region','country_city'], axis=1)
        elif country_region and not country_city and region_city and not country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["region_city"].isin(self.region_city)]
            self.dfd = self.dfd.drop(['country_region','country_city','region_city','country_region_city'], axis=1)
        elif not country_region and country_city and region_city and not country_region_city:
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["region_city"].isin(self.region_city)]
            self.dfd = self.dfd.drop(['country_city','region_city'], axis=1)
        elif country_region and not country_city and not region_city and country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region','country_region_city'], axis=1)
        elif not country_region and country_city and not region_city and country_region_city:
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_city"].isin(self.country_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region','country_city','region_city','country_region_city'], axis=1)
        elif not country_region and not country_city and region_city and country_region_city:
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["region_city"].isin(self.region_city)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['region_city','country_region_city'], axis=1)
        elif country_region and not country_city and not region_city and not country_region_city:
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd["country_region"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region"].isin(self.country_region)]
            self.dfd = self.dfd.drop(['country_region'], axis=1)
        elif not country_region and country_city and not region_city and not country_region_city:
            self.dfd["country_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_city"].isin(self.country_city)]
            self.dfd = self.dfd.drop(['country_city'], axis=1)
        elif not country_region and not country_city and region_city and not country_region_city:
            self.dfd["region_city"] = self.dfd.apply(lambda x: (lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["region_city"].isin(self.region_city)]
            self.dfd = self.dfd.drop(['region_city'], axis=1)
        elif not country_region and not country_city and not region_city and country_region_city:
            self.dfd["country_region_city"] = self.dfd.apply(lambda x: (lower(x.geo_country), lower(x.geo_region), lower(x.geo_city)), axis=1)
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)
                        | self.dfd["country_region_city"].isin(self.country_region_city)]
            self.dfd = self.dfd.drop(['country_region_city'], axis=1)
        elif not country_region and not country_city and not region_city and not country_region_city:
            self.dfd = self.dfd[self.dfd.geo_country.str.lower().isin(self.countries) 
                        | self.dfd.geo_region.str.lower().isin(self.regions)
                        | self.dfd.geo_city.str.lower().isin(self.cities)]
            
    def filter_by_name(self):
        for colName, names in self.filter_names:
            self.dfd = self.dfd[self.dfd[colName].str.lower().isin(names)]
    
    def filter_by_range(self):
        if self.start_time:
            self.dfd = self.dfd[self.dfd["timestamp_raw"] >= self.start_time]
        elif self.end_time:
            self.dfd = self.dfd[self.dfd["timestamp_raw"] <= self.end_time]

    def filter(self):
        if self.filter_names is not None:
            self.filter_by_name()
        if self.start_time is not None:
            self.filter_by_range()
        if self.countries is not None:
            self.filter_by_country_region_city()
        
        
    def aggregate(self):
        df = self.dfd.groupby(self.group_by).size().compute().to_frame()
        df.name = "Aggregation"
        df.reset_index(inplace=True)
        df = df.rename(columns = {'index':self.group_by})
        df = df.rename(columns = {0:'size'})
        df["percentage"] = 100*df['size']/df['size'].sum()
        df.sort_values('size', inplace=True, ascending=False)
        return df
        

        

