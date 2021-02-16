#%%
from bergen.clients.host import HostBergen
from bergen.models import Node
import asyncio
import logging
from fiji_arnheim.helper import ImageJHelper
from fiji_arnheim.macros.filter import FilterMacro
from grunnlag.schema import Representation, RepresentationVariety, Sample
import xarray as xr


logger = logging.getLogger(__name__)


helper = ImageJHelper()



def main():

    client = HostBergen(
            host="p-tnagerl-lab1",
            port=8000,
            client_id="DSNwVKbSmvKuIUln36FmpWNVE2KrbS2oRX0ke8PJ", 
            client_secret="Gp3VldiWUmHgKkIxZjL2aEjVmNwnSyIGHWbQJo6bWMDoIUlBqvUyoGWUWAe6jI3KRXDOsD13gkYVCZR0po1BLFO9QT4lktKODHDs0GyyJEzmIjkpEOItfdCC4zIa3Qzu",
            name="image_karl"# if we want to specifically only use pods on this innstance we would use that it in the selector
    )


    blur = Node.objects.get(package="@canoncial/generic/filters", interface="gaussian-blur")

    fft = FilterMacro("""
        stack = getImageID;
        run("FFT", stack);
        """)


    @client.register(blur, gpu=True, image_k=True)
    async def bluring(helper, rep=None, sigma=None, planes=None, channel=None):
        """Sleep on the CPU

        Args:
            helper ([type]): [description]
            rep ([type], optional): [description]. Defaults to None.
        """
        rep = await Representation.asyncs.get(id=rep)
        array = fft(rep.data.sel(c=0, t=0, z=0))

        new = array.data.reshape(array.shape + (1,1,1))
        output = xr.DataArray(new, dims=list("xyczt"))
        rep = await Representation.asyncs.from_xarray(output, name="fft", sample= rep.sample.id, variety=RepresentationVariety.VOXEL)
        return { "rep": rep }

    client.run()








