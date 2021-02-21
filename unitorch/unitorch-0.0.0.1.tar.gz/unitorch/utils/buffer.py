from functools import partial
import torch
import numpy as np


def get_buffer_size(buf):
    """"""
    if isinstance(buf, torch.Tensor) or isinstance(buf, np.ndarray):
        return buf.shape[0]
    if buf is None:
        return 0
    if isinstance(buf, tuple) or isinstance(buf, list):
        b0 = buf[0]
    else:
        k0 = list(buf.keys())[0]
        b0 = buf[k0]
    return get_buffer_size(b0)


def pop_buffer_topk(buf, topk):
    if isinstance(buf, torch.Tensor) or isinstance(buf, np.ndarray):
        pop_buf, rest_buf = buf[:topk], buf[topk:]
        return pop_buf, rest_buf

    if isinstance(buf, tuple) or isinstance(buf, list):
        pop_buf, rest_buf = zip(*[pop_buffer_topk(b, topk) for b in buf])
        return pop_buf, rest_buf

    keys = buf.keys()
    pop_buf, rest_buf = dict(), dict()
    for k in keys:
        pop_buf[k], rest_buf[k] = pop_buffer_topk(buf[k], topk)
    return pop_buf, rest_buf


def buffer_to_cuda(buf):
    if buf is None:
        return buf
    if isinstance(buf, torch.Tensor):
        return buf.cuda(non_blocking=True)
    if isinstance(buf, tuple) or isinstance(buf, list):
        return list(buffer_to_cuda(t) for t in buf)
    return dict({k: buffer_to_cuda(v) for k, v in buf.items()})


def buffer_to_cpu(buf):
    if buf is None:
        return buf
    if isinstance(buf, torch.Tensor):
        return buf.cpu()
    if isinstance(buf, tuple) or isinstance(buf, list):
        return list(buffer_to_cpu(t) for t in buf)
    return dict({k: buffer_to_cpu(v) for k, v in buf.items()})


# template functions for buffer
def template_function_for_buffer(buf, torch_func=lambda x: x, np_func=lambda x: x):
    if isinstance(buf, torch.Tensor):
        return torch_func(buf)

    if isinstance(buf, np.ndarray):
        return np_func(buf)

    if isinstance(buf, tuple) or isinstance(buf, list):
        return list(
            [
                template_function_for_buffer(b, torch_func=torch_func, np_func=np_func)
                for b in buf
            ]
        )

    keys = buf.keys()
    return dict(
        {
            k: template_function_for_buffer(
                buf[k], torch_func=torch_func, np_func=np_func
            )
            for k in keys
        }
    )


def template_function_for_buffers(*bufs, torch_func=lambda x: x, np_func=lambda x: x):
    if isinstance(bufs[0], torch.Tensor):
        return torch_func(bufs)

    if isinstance(bufs[0], np.ndarray):
        return np_func(bufs)

    if isinstance(bufs[0], tuple) or isinstance(bufs[0], list):
        return list(
            [
                template_function_for_buffers(
                    *bs, torch_func=torch_func, np_func=np_func
                )
                for bs in zip(*bufs)
            ]
        )

    keys = bufs[0].keys()
    return dict(
        {
            k: template_function_for_buffers(
                *[b[k] for b in bufs], torch_func=torch_func, np_func=np_func
            )
            for k in keys
        }
    )


merge_buffer = lambda *bufs, dim=0: partial(
    template_function_for_buffers,
    torch_func=lambda x: torch.cat(x, dim=dim),
    np_func=lambda x: np.concatenate(x, axis=dim),
)(*bufs)

stack_buffer = lambda *bufs, dim=0: partial(
    template_function_for_buffers,
    torch_func=lambda x: torch.stack(x, dim=dim),
    np_func=lambda x: np.stack(x, axis=dim),
)(*bufs)
