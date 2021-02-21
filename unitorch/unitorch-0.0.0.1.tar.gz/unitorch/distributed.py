import torch
import torch.distributed as dist


def ddp_sync_buffer(buf):
    if isinstance(buf, torch.Tensor):
        new_buf = [buf.clone() for _ in range(dist.get_world_size())]
        dist.all_gather(new_buf, buf)
        return torch.cat(new_buf)

    if isinstance(buf, tuple) or isinstance(buf, list):
        return list(ddp_sync_buffer(b) for b in buf)

    keys = buf.keys()
    return dict({k: ddp_sync_buffer(buf[k]) for k in keys})
