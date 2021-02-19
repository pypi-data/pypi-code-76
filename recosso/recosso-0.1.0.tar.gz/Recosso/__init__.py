#update version in setup.py
#python setup.py bdist_wheel
#python3 -m twine upload --skip-existing dist/*


#python3 setup.py sdist
#python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


def reconcile(primary, secondary):
    '''
    It will reconcile two reports.
    Input is FILE NAMES.
    Output is :
        Both main dataframes
        settled and unsettled dataframes.
    '''
    
    import pandas as pd
    import numpy as np
    
    df1=pd.read_csv(primary)
    df2=pd.read_csv(secondary)
    
    # Column names: remove white spaces and convert to lower case
    df1.columns= df1.columns.str.strip().str.lower()
    df2.columns= df2.columns.str.strip().str.lower()
    
    df1=df1.add_prefix('primary_')
    df2=df2.add_prefix('secondary_')
    
    df1=df1.rename(columns={"primary_order_id": "order_id"})
    df2=df2.rename(columns={"secondary_order_id": "order_id"})
    
    temp1=pd.DataFrame()
    temp1=df1[['order_id','primary_amount']]
    
    temp2=pd.DataFrame()
    temp2=df2[['order_id','secondary_amount']]
    
    merged=pd.DataFrame()
    merged = pd.merge(left=temp1, right=temp2, left_on='order_id', right_on='order_id')
    
    merged['matched'] = np.where(merged['primary_amount'] == merged['secondary_amount'], 'yes', 'no')
    merged_unsettled=merged[merged['matched']=='no']
    merged_unsettled['remark']='AMOUNT NOT MATCHED'
    merged_settled=merged[merged['matched']=='yes']
    
    #extracting the orderID not found in secondary file
    a=temp1['order_id'].isin(merged['order_id'])
    temp1index=list()
    c=0
    for i in a:
        if i == False:
            temp1index.append(c)
        c=c+1
    temp1_unsettled=temp1.take(temp1index)
    temp1_unsettled['remark']='ORDERID NOT FOUND IN SECONDARY FILE'
    
    ########
    
    unsettled=pd.concat([merged_unsettled,temp1_unsettled], ignore_index=True)
    
    settled=merged_settled
    
    return df1 , df2 , unsettled , settled

#################################################################################################################################
#################################################################################################################################

# total orders

def total_orders(df):
    count = len(df['order_id'].unique())
    return count


#################################################################################################################################
#################################################################################################################################
# no_settled_txns
# no_processed_txns
# no_unsettled_txns

def total_txns(df):
    '''
    Please pass datafram accordingly.
    
    this function can be used to calculate values like:
    
    no_processed_txns (pass main dataframe)
    no_settled_txns (pass settled dataframe)
    no_unsettled_txns (pass unsettled dataframe)
    '''
    
    count = len(df)
    return count

#################################################################################################################################
#################################################################################################################################

### make a single function for tax commision and other numerical sum feilds.


def get_sum(df,feild, primary=True, count='1'):
    
    if feild=='amount':
        
        if primary==True:
            count = df['primary_amount'].sum()
        else:
            count = df['secondary_amount'].sum()
    
    elif feild=='tax':
        if primary==True: 
            if count=='1':
                count = df['primary_tax1'].sum()    
            elif count=='2':
                count = df['primary_tax1'].sum() + df['primary_tax2'].sum()        
            elif count=='3':
                count = df['primary_tax1'].sum() + df['primary_tax2'].sum() + df['primary_tax3'].sum()    
        elif primary==False:
            if count=='1':
                count = df['secondary_tax1'].sum()    
            elif count=='2':
                count = df['secondary_tax1'].sum() + df['secondary_tax2'].sum()
            elif count=='3':
                count = df['secondary_tax1'].sum() + df['secondary_tax2'].sum() + df['secondary_tax3'].sum()        
        else:
            count = 'Contact Recosso Team.'
            
            
######################

    elif feild=='commission':
        if primary==True: 
            if count=='1':
                count = df['primary_commission1'].sum()    
            elif count=='2':
                count = df['primary_commission1'].sum() + df['primary_commission2'].sum()        
            elif count=='3':
                count = df['primary_commission1'].sum() + df['primary_commission2'].sum() + df['primary_commission3'].sum()    
        elif primary==False:
            if count=='1':
                count = df['secondary_commission1'].sum()    
            elif count=='2':
                count = df['secondary_commission1'].sum() + df['secondary_commission2'].sum()        
            elif count=='3':
                count = df['secondary_commission1'].sum() + df['secondary_commission2'].sum() + df['secondary_commission3'].sum() 
        else:
            count = 'Contact Recosso Team.'

#####################

    elif feild=='discount':
        if primary==True: 
            if count=='1':
                count = df['primary_discount1'].sum()
            elif count=='2':
                count = df['primary_discount1'].sum() + df['primary_discount2'].sum()        
            elif count=='3':
                count = df['primary_discount1'].sum() + df['primary_discount2'].sum() + df['primary_discount3'].sum()    
        elif primary==False:
            if count=='1':
                count = df['secondary_discount1'].sum()    
            elif count=='2':
                count = df['secondary_discount1'].sum() + df['secondary_discount2'].sum()        
            elif count=='3':
                count = df['secondary_discount1'].sum() + df['secondary_discount2'].sum() + df['secondary_discount3'].sum()       
        else:
            count = 'Contact Recosso Team.'
            
            
    return count

#################################################################################################################################
#################################################################################################################################

# discount not calculated yet
def partner_details(df):
    
    '''
    funtion return a dict for each partner 
    
    order_count
    revenue
    tax paid
    #discount
    '''
    
    lis=list(df['partner'].unique())
    case_list= dict()
    for i in lis:
        amt=df['primary_amount'][df['primary_partner'] == i].sum()
        ordercount = len(df['order_id'][df1['primary_partner'] == i].unique())
        tax= df1['primary_tax1'][df1['primary_partner'] == i].sum()     # also pass the number of tax feild for futher cal
        case = {'order_count': ordercount,'revenue': amt, 'tax':tax,}
        case_list[i] = case
        
    return case_list



#################################################################################################################################
#################################################################################################################################
def partner(df):
    '''
    function return the list of partners
    '''
    lis=list(df['primary_partner'].unique())
    return lis



#################################################################################################################################
