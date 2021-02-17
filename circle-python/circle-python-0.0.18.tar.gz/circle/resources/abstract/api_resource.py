from circle.circle_object import CircleObject


class APIResource(CircleObject):
    @classmethod
    def retrieve(cls, id, api_key=None, **kwargs):
        instance = cls(id, api_key, **kwargs)
        instance.refresh()
        return instance

    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                "APIResource is an abstract class. Perform actions on one of its subclasses (e.g. Card)."
            )

        base = cls.OBJECT_NAME.replace(".", "/")

        return "/v1/%s" % (base,)

    def instance_url(self):
        id = self.get("id")

        base = self.class_url()
        extn = id
        return "%s/%s" % (base, extn)

    def refresh(self):
        self.refresh_from(self.request("get", self.instance_url()))
        return self
