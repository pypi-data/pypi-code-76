import pandas as pd

def date_feat(data,feature):
    data[feature+'_month'] = data[feature].dt.month
    data[feature+'_day'] = data[feature].dt.day
    data[feature+"_quarter"] = data[feature].dt.quarter
    data[feature+"_isweekend"] = (data[feature].dt.weekday < 5).astype(float)

    dr = data[feature]
    cal = calendar()
    holidays = cal.holidays(start=dr.min(), end=dr.max())

    data[feature+'_holiday'] = data[feature].isin(holidays).astype(float)
    return data

date_feat(data,'offer_date')    