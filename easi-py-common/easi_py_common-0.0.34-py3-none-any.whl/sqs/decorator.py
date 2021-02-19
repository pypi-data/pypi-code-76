from easi_py_common.sqs.consumer import subscribe as sub


def subscribe(address,
              work_number=8,  # 协程数
              msg_lifetime=86400 * 3,  # 消息过期时间(xx秒内未消费直接丢弃)
              visibility_timeout_seconds=300):  # 消息超时时间，超过xx秒未执行完成，会走重试流程
    def wrapper(f):
        sub(address, f,
            work_number=work_number,
            msg_lifetime=msg_lifetime,
            visibility_timeout_seconds=visibility_timeout_seconds)
        return f

    return wrapper
