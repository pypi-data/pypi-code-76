from intake.catalog import Catalog
from intake.catalog.local import LocalCatalogEntry
from intake.source.base import DataSource, Schema
import stripe
import pandas as pd
from . import __version__

def stripe_get_data(resource, schema=False, start_date=None, end_date=None, **kwargs):   
    """
    Get Stripe data use the List method for all resources (i.e., data tables; e.g., Subscription, Event)
    
    Basic stripe API function is like stripe.Subscription.list(). 
    We paramerized the resource and use auto-pagination to ensure we get all the data.
    
    Note: Stripe API has data limitations for some resources. 
    For example, events data only go back up to 30 days. 
    
    """
    if start_date:
        # convert to unix timestamp
        start_date = int(start_date.timestamp())
    if end_date:
        # convert to unix timestamp
        end_date = int(end_date.timestamp())
    if schema: 
        # only read 1 record to get the schema
        resource_list = getattr(stripe, resource).list(limit=1, created={"gte": start_date,"lt": end_date},**kwargs)
        return pd.DataFrame(resource_list['data'])
    else:
        # get data
        resource_list = getattr(stripe, resource).list(limit=100, created={"gte": start_date,"lt": end_date},**kwargs)
        lst = []
        for i in resource_list.auto_paging_iter():
            lst.extend([i])
        df = pd.DataFrame(lst)
        if len(df) > 0:
            df['created'] = pd.to_datetime(df['created'], unit='s')
    return df

def resource_list():
    """
    get a list of all available resources that we can do stripe.resource.list()
    """
    resource = []
    for attr in dir(stripe):
        if hasattr(getattr(stripe, attr), 'list'):
            resource.append(attr)
    return resource


class StripeAPI():

    def __init__(self, api_key, api_version="2020-08-27"):    
        stripe.api_key = api_key
        stripe.api_version = api_version

    def get_table(self, resource, schema, **kwargs):
        return stripe_get_data(resource, schema, **kwargs) 
    
    
class StripeTableSource(DataSource):
    name = 'stripe_table'
    container = 'dataframe'
    version = __version__
    partition_access = True
    
    def __init__(self, api_key, resource, metadata=None, api_version="2020-08-27", **kwargs):
        self.resource = resource
        self._df = None
        self._df_schema = None       
        self._stripe = StripeAPI(api_key, api_version)
        super(StripeTableSource, self).__init__(metadata=metadata)   #this sets npartitions to 0 
        self.npartitions = 1
        self.kwargs = kwargs

    def _get_schema(self): 
        # get column info
        if self._df_schema is None:
            self._df_schema = self._stripe.get_table(resource=self.resource, schema=True)
        return Schema(datashape=None,
                      dtype=self._df_schema,
                      shape=(None, len(self._df_schema.columns)),
                      npartitions=1,
                      extra_metadata={})
            
    def _get_partition(self, i=0):
        # get data
        if self._df is None:
            self._df = self._stripe.get_table(resource=self.resource, schema=False, **self.kwargs)
        return self._df  

    def _close(self):
        self._dataframe = None
        
class StripeCatalog(Catalog):
    name = 'stripe_catalog'
    version = __version__
    def __init__(self, api_key, *kwargs, metadata=None, api_version="2020-08-27"):
        stripe.api_key = api_key
        stripe.api_version = api_version
        self.api_key = api_key
        self.api_version = api_version
        super().__init__(name='stripe', metadata=metadata)
    
    def _load(self):
        resources = resource_list()
        for r in resources:
            e = LocalCatalogEntry(
                        name=r,
                        description=r, 
                        driver=StripeTableSource,
                        catalog=self,
                        args={
                            'api_key': self.api_key,
                            'api_version': self.api_version,
                            'resource': r
                        }
                    )
            e._plugin = [StripeTableSource]
            self._entries[r] = e