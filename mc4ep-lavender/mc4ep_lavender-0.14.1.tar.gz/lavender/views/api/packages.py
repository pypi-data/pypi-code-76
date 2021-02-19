from typing import List

from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel

from lavender.models import Package, Player
from lavender.views.api.decorator import authenticated, json_response


class PackageInstance(BaseModel):
    name: str
    title: str
    version: str
    location: str

    class Config:
        allow_mutation = False
        orm_mode = True


class PackageList(BaseModel):
    minimumVersion: int = 3
    packages: List[PackageInstance] = []

    class Config:
        allow_mutation = False


@csrf_exempt
@json_response
@authenticated
def package_list(player: Player, _) -> PackageList:
    packages = [
        PackageInstance.from_orm(package)
        for package in
        Package.objects.filter(player=player)
    ]
    return PackageList(packages=packages)
