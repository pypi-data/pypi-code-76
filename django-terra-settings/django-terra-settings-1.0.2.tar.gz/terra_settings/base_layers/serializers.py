from django.utils.translation import gettext as _
from mapbox_baselayer.models import MapBaseLayer, BaseLayerTile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse


class BaseLayerTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseLayerTile
        fields = ('url', )

    def to_representation(self, instance):
        return instance.url

    def to_internal_value(self, data):
        return data


class MapBaseLayerSerializer(serializers.ModelSerializer):
    tiles = BaseLayerTileSerializer(many=True, required=False)
    tilejson_url = serializers.SerializerMethodField()

    def get_tilejson_url(self, instance):
        """
        Provide generated tilejson or mapbox url along base layer type
        """
        if instance.base_layer_type != 'mapbox':
            return reverse('baselayer-tilejson', args=(instance.pk, ),
                           request=self.context.get('request'))
        else:
            return instance.map_box_url

    def validate(self, attrs):
        if attrs.get('base_layer_type') == 'mapbox':
            if attrs.get('tiles'):
                raise ValidationError(_("'tiles' should not be filled for mapbox base layers."))
            if not attrs.get('map_box_url'):
                raise ValidationError(_("'map_box_url' should be filled for mapbox base layers."))
        else:
            if not attrs.get('tiles'):
                raise ValidationError(_("'tiles' should be filled for raster and vector base layers."))
            if attrs.get('map_box_url'):
                raise ValidationError(_("'map_box_url' should not be filled for raster and vector base layers."))
        return attrs

    def create(self, validated_data):
        """ handle sub tile definition """
        tiles = validated_data.pop('tiles')
        instance = MapBaseLayer.objects.create(**validated_data)
        for tile in tiles:
            BaseLayerTile.objects.create(base_layer=instance, url=tile)
        return instance

    def update(self, instance, validated_data):
        """ handle sub tile definition """
        tiles = validated_data.pop('tiles')
        for key, value in validated_data.items():
            # update data for each instance validated value
            setattr(instance, key, value)
        if tiles:
            # delete tiles not in putted data
            instance.tiles.exclude(url__in=[tile for tile in tiles]).delete()
            tile_instances = [
                BaseLayerTile.objects.get_or_create(url=tile,
                                                    base_layer=instance)[0] for tile in tiles
            ]
            instance.tiles.set(tile_instances)
        instance.save()
        return instance

    class Meta:
        model = MapBaseLayer
        fields = (
            'id', 'tiles', 'name', 'order', 'slug',
            'base_layer_type', 'map_box_url', 'sprite',
            'glyphs', 'min_zoom', 'max_zoom',
            'tile_size', 'attribution', 'tiles', 'tilejson_url'
        )


class PublicMapBaseLayerSerializer(serializers.ModelSerializer):
    """ Serializer used to provide quick select list in default public settings API endpoint """
    tilejson_url = serializers.SerializerMethodField()

    def get_tilejson_url(self, instance):
        """
        Provide generated tilejson or mapbox url along base layer type
        """
        if instance.base_layer_type != 'mapbox':
            return reverse('baselayer-tilejson', args=(instance.pk, ))
        else:
            return instance.map_box_url

    class Meta:
        model = MapBaseLayer
        fields = (
            'id', 'order', 'name', 'slug', 'tilejson_url'
        )
