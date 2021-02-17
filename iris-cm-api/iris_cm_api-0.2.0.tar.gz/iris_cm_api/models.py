from tortoise import Model, fields


class Duty(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=4098)
    secret_code = fields.CharField(max_length=100)


class Chat(Model):
    id = fields.IntField(pk=True)
    iris_id = fields.CharField(max_length=16, null=True)
    enable = fields.BooleanField(default=False)
    transcript = fields.BooleanField(default=False)
    duty = fields.ForeignKeyField(
        'models.Duty',
        on_delete=fields.SET_NULL,
        related_name='chats',
        null=True
    )
