import connexion
import six

from swagger_server.models.store_info import StoreInfo  # noqa: E501
from swagger_server import util
from swagger_server.logic.summary import Summary

def summary_get():  # noqa: E501
    """Gives petstore&#x27;s summary

     # noqa: E501


    :rtype: StoreInfo
    """
    summary=Summary()
    info = summary.fetch_summary()
    return info
