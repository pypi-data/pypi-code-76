from bergen.types.model import ArnheimAsyncModelManager, ArnheimModelManager

class RepresentationManager(ArnheimModelManager["Representation"]):

    def from_xarray(self, array, compute=True, **kwargs):
        instance = self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = self.update(id=instance.id, **kwargs)
        return instance


class AsyncRepresentationManager(ArnheimAsyncModelManager["Representation"]):

    async def from_xarray(self, array, compute=True, **kwargs):
        instance = await self.create(**kwargs)
        instance.save_array(array, compute=compute)
        instance = await self.update(id=instance.id, **kwargs)
        return instance