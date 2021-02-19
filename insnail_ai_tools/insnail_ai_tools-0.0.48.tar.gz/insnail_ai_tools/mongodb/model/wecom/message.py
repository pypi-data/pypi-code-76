import re
from typing import List

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin, StrChoicesMixin

ASR_RESULT_PARSE_REGEX = re.compile(
    r"\[([0-9]+:[0-9.]+),([0-9]+:[0-9.]+),(\d+)\]  (.*)"
)


class WecomMessageActionChoices(StrChoicesMixin):
    send = "发送"
    recall = "撤回"
    switch = "切换企业日志"


class WecomMessageModeChoices(StrChoicesMixin):
    personal = "私聊"
    group = "群聊"


class WecomMessageRoleChoices(StrChoicesMixin):
    user = "用户"
    external_user = "外部用户"
    robot = "机器人"


# 机器人与外部联系人的账号都是external_userid，
# 其中机器人的external_userid是以”wb”开头，例如：”wbjc7bDwAAJVylUKpSA3Z5U11tDO4AAA”，外部联系人的external_userid以”wo”或”wm”开头。
# 关于企业微信消息格式参考文档:
# https://work.weixin.qq.com/api/doc/90000/90135/91774


class WecomMessageExtra(mongoengine.EmbeddedDocument, MultiDatabaseMixin):
    is_extracted = mongoengine.BooleanField(verbose_name="是否抽取文本", default=False)
    is_checked = mongoengine.BooleanField(verbose_name="是否做了质检", default=False)

    is_legal = mongoengine.BooleanField(verbose_name="是否合法", default=True)
    illegal_level = mongoengine.IntField(verbose_name="违规等级", default=0)
    illegal_type = mongoengine.ListField(mongoengine.StringField(), verbose_name="非法类型")


class WecomMessage(mongoengine.DynamicDocument):
    msg_id = mongoengine.StringField(
        verbose_name="消息id",
        max_length=64,
        unique=True,
        help_text="消息id，消息的唯一标识，企业可以使用此字段进行消息去重。msg_id以_external结尾的消息，表明该消息是一条外部消息。",
    )
    action = mongoengine.StringField(
        verbose_name="action",
        max_length=16,
        choices=WecomMessageActionChoices.choices(),
        default="send",
        required=True,
    )
    # 消息格式，参考 https://work.weixin.qq.com/api/doc/90000/90135/91774#消息格式
    msg_type = mongoengine.StringField(verbose_name="消息类型", max_length=64)
    mode = mongoengine.StringField(
        verbose_name="消息类型，群聊还是单聊等",
        choices=WecomMessageModeChoices.choices(),
        default=WecomMessageModeChoices.personal.name,
    )

    # 身份识别相关
    from_user_id = mongoengine.StringField(
        verbose_name="发送者id",
        max_length=64,
        help_text="同一企业内容为userid，非相同企业为external_userid。消息如果是机器人发出，也为external_userid。String类型",
    )
    to_user_id_list = mongoengine.ListField(
        mongoengine.StringField(max_length=64),
        verbose_name="消息接收方列表",
        help_text="消息接收方列表，可能是多个，同一个企业内容为userid，非相同企业为external_userid。数组，内容为string类型",
    )
    room_id = mongoengine.StringField(
        verbose_name="群聊消息的群id", max_length=64, help_text="群聊消息的群id。如果是单聊则为空。String类型"
    )

    user_id = mongoengine.ListField(
        mongoengine.StringField(max_length=64),
        verbose_name="涉及到员工ID列表",
        max_length=64,
        help_text="员工ID",
    )
    external_user_id = mongoengine.ListField(
        mongoengine.StringField(max_length=64),
        verbose_name="涉及到客户ID列表",
        max_length=64,
        help_text="客户ID",
    )

    from_user_role = mongoengine.StringField(
        verbose_name="发送人身份",
        choices=WecomMessageRoleChoices.choices(),
    )

    # 消息主体内容相关
    content = mongoengine.DictField(verbose_name="消息内容")
    content_text = mongoengine.StringField(
        verbose_name="文本内容", help_text="从content中提取的文本内容，比如图片、语音、文件等会从中提取内容"
    )
    url = mongoengine.StringField(verbose_name="消息附加链接")

    # 时间相关
    msg_time = mongoengine.DateTimeField(verbose_name="消息发送时间戳")
    create_time = mongoengine.DateTimeField(verbose_name="创建时间")

    # 一些额外的内容，比如抽取，质检等
    extra = mongoengine.EmbeddedDocumentField(
        WecomMessageExtra, verbose_name="信息的额外内容", default=WecomMessageExtra
    )

    meta = {
        "collection": "wecom_message",
        "indexes": [
            "#msg_id",
            "#msg_type",
            "#type",
            "user_id_list",
            "external_user_id_list",
            "#room_id",
            "#from_user_role",
            "msg_time",
        ],
        "primary_key_field": "msg_id",
        "abstract": True,
    }

    def __str__(self):
        return f"{self.mode}: {self.msg_id}"


class WecomMeetingVoiceMeta(mongoengine.DynamicEmbeddedDocument):
    start_time = mongoengine.StringField(verbose_name="开始时间")
    end_time = mongoengine.StringField(verbose_name="开始时间")
    text = mongoengine.StringField(verbose_name="对话内容")
    from_role = mongoengine.StringField(verbose_name="发送人角色")

    def __str__(self):
        return f"[{self.start_time}-{self.end_time}] {self.text}"

    @classmethod
    def parse_asr_single_result(cls, line: str) -> dict:
        if line:
            start_time, end_time, from_role, text = ASR_RESULT_PARSE_REGEX.findall(
                line
            )[0]
            return {
                "start_time": start_time,
                "end_time": end_time,
                "from_role": from_role,
                "text": text,
            }

    @classmethod
    def parse_asr_result(cls, asr_result: str) -> List[dict]:
        result = []
        for line in asr_result.split("\n"):
            line = line.strip()
            if line:
                result.append(cls.parse_asr_single_result(line))
        return result

    @classmethod
    def gen_meta_list_from_asr_result(
        cls, asr_result: str
    ) -> List["WecomMeetingVoiceMeta"]:
        result = cls.parse_asr_result(asr_result)
        return [cls(**i) for i in result]


class WecomVoiceMeeting(mongoengine.DynamicDocument, MultiDatabaseMixin):
    msg_id = mongoengine.StringField(primary_key=True, verbose_name="消息ID")
    user_id = mongoengine.StringField(verbose_name="员工ID", max_length=64)
    external_user_id = mongoengine.StringField(verbose_name="客户ID", max_length=64)
    union_id = mongoengine.StringField(verbose_name="UNION_ID", max_length=64)
    talk_time = mongoengine.IntField(verbose_name="通话时间（秒）")
    call_type = mongoengine.IntField(verbose_name="1 主叫 2 被叫")
    start_time = mongoengine.DateTimeField(verbose_name="开始时间")
    end_time = mongoengine.DateTimeField(verbose_name="结束时间")
    url = mongoengine.StringField(verbose_name="链接地址")
    create_time = mongoengine.DateTimeField(verbose_name="结束时间")
    asr_status = mongoengine.IntField(
        verbose_name="语音转录状态", help_text="语音转录状态  1待转录 2转录中 3转录成功 4转录失败"
    )

    messages = mongoengine.EmbeddedDocumentListField(
        WecomMeetingVoiceMeta, verbose_name="所有对话记录"
    )

    meta = {
        "collection": "wecom_voice_meeting",
        "indexes": [
            "#msg_id",
            "#user_id",
            "#external_user_id",
            "#union_id",
            "call_type",
            "start_time",
        ],
        "abstract": True,
    }

    def __str__(self):
        return self.msg_id
