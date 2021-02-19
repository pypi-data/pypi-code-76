import datetime as pydatetime
from dateutil.parser import parse

from collections import defaultdict

from geodesic.client import get_client
from geodesic.stac import FeatureCollection

from shapely.geometry import shape


class Dataset:
    """Allows interaction with SeerAI datasets.

    Dataset provides a way to interact with datasets in the SeerAI
    """

    def __init__(self, **spec):
        self.name = spec["name"]
        self.alias = spec["alias"]
        self._spec = {}
        self._spec.update(spec)
        self._client = get_client()

    @property
    def type(self):
        return self._spec["type"]

    @property
    def subtype(self):
        return self._spec["subtype"]

    @property
    def stac(self):
        if self.type != "stac":
            raise ValueError("This dataset is not a STAC dataset")
        return self._spec.get("stac", {})

    def _repr_html_(self, add_style=True):
        st = ""
        if add_style:
            st = style

        providers = ""
        for p in self._spec["stac"].get("providers", []):
            pl = provider_template.format(
                name=p["name"], url=p["url"], roles=", ".join(p["roles"])
            )
            providers += pl
        return st + html_template.format(
            name=self.alias,
            description=self._spec["description"],
            clients=", ".join(self._spec["clients"]),
            providers=providers,
        )

    def query(self, bbox=None, datetime=None, **kwargs):
        """
        Query this service's OGC Features or STAC API. Unless specified by the 'api' keyword,
        this will prefer a STAC search over a OGC Features query
        """
        api = kwargs.pop("api", None)
        clients = self.clients

        if api is None:
            if "stac" in clients:
                api = "stac"
            elif "oafeat" in clients:
                api = "features"

            if api is None:
                raise ValueError("No clients available for query!")
        else:
            if api == "oafeat":
                api = "features"
            elif api == "stac":
                api = "stac"
            else:
                raise ValueError("query with api '{0}' not supported.".format(api))

        # Get all features, this will follow the link
        query_all = kwargs.pop("query_all", False)

        limit = 10
        if query_all:
            limit = 500
        else:
            limit = kwargs.pop("limit", 10)

        # Request query/body
        params = {"limit": limit}

        if api == "features":
            url = "/spacetime/api/v{version}/features/collections/{name}/items".format(
                version=self._client._api_version, name=self.name
            )

        elif api == "stac":
            params["collections"] = [self.name]
            url = "/spacetime/api/v{version}/stac/search".format(
                version=self._client._api_version
            )

        intersects = kwargs.pop("intersects", None)

        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if api == "stac":
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join(map(str, bbox))
        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson
            if isinstance(intersects, dict):
                g = shape(intersects)
            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = g.bounds
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = g.extent

        # STAC search specific
        if api == "stac":
            ids = kwargs.pop("ids", None)
            if ids is not None:
                params["ids"] = ids
            query = kwargs.pop("query", None)
            if query is not None:
                for k, v in query.items():

                    gt = v.get("gt")
                    if gt is not None and isinstance(gt, pydatetime.datetime):
                        v["gt"] = gt.isoformat()
                    lt = v.get("lt")
                    if lt is not None and isinstance(lt, pydatetime.datetime):
                        v["lt"] = lt.isoformat()
                    gte = v.get("gte")
                    if gte is not None and isinstance(gte, pydatetime.datetime):
                        v["gte"] = gte.isoformat()
                    lte = v.get("lte")
                    if lte is not None and isinstance(lte, pydatetime.datetime):
                        v["lte"] = lte.isoformat()
                    eq = v.get("eq")
                    if eq is not None and isinstance(eq, pydatetime.datetime):
                        v["eq"] = eq.isoformat()
                    neq = v.get("neq")
                    if neq is not None and isinstance(neq, pydatetime.datetime):
                        v["neq"] = neq.isoformat()
                    query[k] = v

                params["query"] = query
            sortby = kwargs.pop("sortby", None)
            if sortby is not None:
                params["sortby"] = sortby

            fields = kwargs.pop("fields", None)
            if fields is not None:
                fieldsObj = defaultdict(list)
                # fields with +/-
                if isinstance(fields, list):
                    for field in fields:
                        if field.startswith("+"):
                            fieldsObj["include"].append(field[1:])
                        elif field.startswith("-"):
                            fieldsObj["exclude"].append(field[1:])
                        else:
                            fieldsObj["include"].append(field)
                else:
                    fieldsObj = fields
                params["fields"] = fieldsObj

        if datetime is not None:
            params["datetime"] = "/".join([parsedate(d).isoformat() for d in datetime])

        if api == "features":
            res = self._client.get(url, **params)
        elif api == "stac":
            res = self._client.post(url, **params)

        collection = FeatureCollection(obj=res, dataset=self, query=params)

        if query_all:
            collection.get_all()

        if api == "stac":
            collection._is_stac = True

        return collection

    @property
    def clients(self):
        return self._spec.get("clients", [])


def parsedate(dt):
    try:
        return parse(dt)
    except TypeError:
        return dt


class DatasetList:
    def __init__(self, datasets):
        self.ddict = {dataset.name: dataset for dataset in datasets}

    def __getitem__(self, key):
        return self.ddict[key]

    def _repr_html_(self):
        html = style
        html += '<div class="container">'
        for d in self.ddict.values():
            html += d._repr_html_(False)
        html += "</div>"
        return html


style = """
<head>
<style>

body {
    background: #000;
}

.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 15%;
}
.card, .inner {
    border: 1px solid #e6e1d5;
}

.inner {
    padding: 10px;
    border-radius: 5px;
    height: 330px;
}

.card {
    width: 250px;
    height: 350px;
    margin: 10px;
    padding: 10px;
    background: #000;
    box-shadow: 5px 5px #000;
    border-radius: 5px;
    color: #e6e1d5;
}

li {
    margin-top: 3px;
    margin-bottom: 3px;
}

.content {
    height: 200px;
    overflow-y: scroll;
}

h3 .card-title {
    padding: 0px;
    color: #e6e1d5;
    font-size: 8px;
};

p .card-text  {
    padding: 0px;
    font-size: 6px;
}

div .text-box {
}

div .text-description {
    //height: 180px;
}

div .text-clients {
    //height: 50px;
}

.container {
    display: flex;
}

.scroll-style::-webkit-scrollbar-track
{
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    border-radius: 2px;
    background-color: #000;
}

.scroll-style::-webkit-scrollbar
{
    width: 4px;
    background-color: #000;
}

.scroll-style::-webkit-scrollbar-thumb
{
    border-radius: 2px;
    background-color: #e6e1d5;
}

</style>
</head>
"""

html_template = """
<div class="card">
  <div class="inner scroll-style">
    <img class="center" src="https://seerai.space/images/Logo.svg"></img>
    <h3 class="card-title">{name}</h4>
    <div class="content scroll-style">
      <div class="text-box text-description">
        <p class="card-text text-description"><b>Description:</b> {description}</p>
      </div>
      <div class="text-clients">
        <p class="card-text text-clients"><b>Clients:</b> {clients}</p>
      </div>
      <div class="links">
        <p class="card-text text-clients"><b>Providers:</b><ul>{providers}</ul></p>
      </div>
    </div>
  </div>
</div>
"""

provider_template = """
<li><p><a href="{url}">{name}</a> ({roles})</li>
"""
