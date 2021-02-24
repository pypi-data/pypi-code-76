# Membership Recency + Frequency

import pandas as pd
import glob
import os
import sys

path = os.getcwd() # use your path
all_files = glob.glob(path + "/*.xlsx")
# print(all_files)

li = []
for filename in all_files:
    df = pd.read_excel(filename, #engine='openpyxl',
     skiprows=2)
    new_header = df.iloc[1] #grab the first row for the header
    df = df[5:] #take the data less the header row
    # print(df.head)
    # print(100*'-')
#     df.columns = new_header #set the header row as the df header
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

people = frame[frame['individual_id'].notna()]

people.shape

people.tail()

print(people.shape)
people = people.set_index('individual_id')

people['Membership Year'].value_counts()


# #### 116,880 total Meeting Attendees since 2015

# # Using individual_id as Index allows for the following aggregate to run properly

people['Last Membership'] = pd.to_numeric(people.groupby(['individual_id'], sort=False)['Membership Year'].max())
people['Recency'] = 2021 - people['Last Membership']
people['Frequency'] = pd.to_numeric(people.groupby(['individual_id'], sort=False)['Membership Year'].count())

final_membership_rf = people[['first_last_name','primary_email_address','Last Membership','Frequency', 'Recency', 'Membership Product Group', 'Primary Member Type','Country', 'Membership Year']]
print(final_membership_rf.shape)
final_membership_rf.sample(10)


# Does this include all 2020 members? I filtered for last membership 2020 and 2 year membership and I am only getting approx. 3800 records but we had 14000 2 years members in 2020. So I was wondering if we intentionally omitted some people. 

final_membership_rf['Last Membership'].value_counts()

final_membership_rf[['Membership Year', 'Membership Product Group']].value_counts()

final_membership_rf.shape

final_membership_rf.to_csv('MembershipRecencyFrequency_w_Product.csv', index=True)
print("Shape:", final_membership_rf.shape)
print(final_membership_rf.sample(5))
print(100*'-')
print("Complete!")
