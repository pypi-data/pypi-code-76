import torch
import time
import logging
import numpy as np
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from itertools import chain
from torch.utils.data import BatchSampler, DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
from unitorch.utils.buffer import buffer_to_cuda, buffer_to_cpu, merge_buffer

try:
    from apex import amp

    amp.register_float_function(torch, "sigmoid")
except:
    logging.info("FP16 is not support.")

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True


class core_task(object):
    def __init__(self):
        pass

    @classmethod
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def train(self):
        pass

    def score(self):
        pass

    def infer(self):
        pass


class supervised_task(core_task):
    def __init__(
        self,
        seed=1123,
    ):
        try:
            torch.distributed.init_process_group(backend="nccl", init_method="env://")
        except:
            logging.info("PyTorch is not in distributed mode")

        self.n_gpu = 1 if torch.cuda.is_available() else 0
        if dist.is_initialized():
            self.n_gpu = dist.get_world_size()

    def monitor(self, net_outputs, net_targets, monitor_fns):
        if self.monitor_fns is None:
            return

        for monitor_fn in monitor_fns:
            score = monitor_fn(net_outputs=net_outputs, net_targets=net_targets)
            info = str(monitor_fn.__class__.__name__)
            logging.info(f"{info} is {score}")
        return

    def train(
        self,
        model=None,
        opt=None,
        dataset_for_train=None,
        dataset_for_dev=None,
        loss_fn=None,
        score_fn=None,
        monitor_fns=None,
        scheduler=None,
        to_ckpt_dir="./to_ckpt/",
        local_rank=-1,
        train_batch_size=128,
        dev_batch_size=128,
        pin_memory=True,
        num_workers=4,
        opt_fp16="O0",
        log_freq=100,
        ckpt_freq=10000,
        grad_acc_step=1,
        max_grad_norm=1.0,
        epochs=5,
    ):

        global_rank = -1
        if self.n_gpu > 1:
            model = nn.parallel.DistributedDataParallel(
                model,
                device_ids=[local_rank],
                output_device=local_rank,
                find_unused_parameters=True,
            )
            global_rank = dist.get_rank()

        model, opt = amp.initialize(model, opt, opt_level=opt_fp16)

        train_sampler = DistributedSampler if self.n_gpu > 1 else RandomSampler
        dev_sampler = DistributedSampler if self.n_gpu > 1 else SequentialSampler

        iter_for_train = DataLoader(
            dataset_for_train,
            sampler=train_sampler(dataset_for_train),
            batch_size=train_batch_size,
            shuffle=False,
            pin_memory=pin_memory,
            num_workers=num_workers,
        )

        iter_for_dev = DataLoader(
            dataset_for_dev,
            sampler=dev_sampler(dataset_for_dev),
            batch_size=dev_batch_size,
            shuffle=False,
            pin_memory=pin_memory,
            num_workers=num_workers,
        )
        score_best = float("-inf")
        log_loss = 0
        dev_epoch = 0
        for e in range(0, epochs):
            torch.cuda.empty_cache()
            if hasattr(iter_for_train.sampler, "set_epoch"):
                iter_for_train.sampler.set_epoch(e)
            model.train()
            for step, data_buf in enumerate(iter_for_train):
                if torch.cuda.is_available():
                    data_buf = buffer_to_cuda(data_buf)
                assert "net_inputs" in data_buf
                outputs = model(**data_buf.get("net_inputs"))
                assert "net_outputs" in outputs
                net_outputs = outputs.get("net_outputs")
                net_targets = data_buf.get("net_targets")
                loss = (
                    loss_fn(net_targets=net_targets, net_outputs=net_outputs)
                    / grad_acc_step
                )

                nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)

                if opt_fp16 != "O0":
                    with amp.scale_loss(loss, opt) as scale_loss:
                        scale_loss.backward()
                else:
                    loss.backward()

                log_loss += loss.data * grad_acc_step
                if (step + 1) % grad_acc_step == 0:
                    opt.step()
                    if scheduler is not None:
                        scheduler.step()
                    opt.zero_grad()

                if (step + 1) % log_freq == 0 and global_rank in [-1, 0]:
                    logging.info(
                        f"epoch {e} step {step}: loss -- { log_loss / log_freq }"
                    )
                    log_loss = 0

                if (step + 1) % ckpt_freq == 0:
                    if hasattr(iter_for_dev.sampler, "set_epoch"):
                        iter_for_dev.sampler.set_epoch(dev_epoch)
                        dev_epoch += 1

                    ret_dict = self.score(model, iter_for_dev, score_fn)
                    self.monitor(
                        net_outputs=ret_dict.get("net_outputs"),
                        net_targets=ret_dict.get("net_targets"),
                        monitor_fns=monitor_fns,
                    )
                    new_score = ret_dict.get("new_score")
                    if new_score > score_best:
                        score_best = new_score
                        model.save_checkpoint(ckpt_dir=to_ckpt_dir)

            if hasattr(iter_for_dev.sampler, "set_epoch"):
                iter_for_dev.sampler.set_epoch(dev_epoch)
                dev_epoch += 1

            ret_dict = self.score(model, iter_for_dev, score_fn)
            self.monitor(
                net_outputs=ret_dict.get("net_outputs"),
                net_targets=ret_dict.get("net_targets"),
                monitor_fns=monitor_fns,
            )
            new_score = ret_dict.get("new_score")
            if new_score > score_best:
                score_best = new_score
                model.save_checkpoint(ckpt_dir=to_ckpt_dir)

    @torch.no_grad()
    def score(self, model, iter_for_dev, score_fn):
        base_model = model.module if hasattr(model, "module") else model
        base_model.eval()
        net_outputs, net_targets = [], []
        for _, data_buf in enumerate(iter_for_dev):
            if torch.cuda.is_available():
                data_buf = buffer_to_cuda(data_buf)
            assert "net_inputs" in data_buf
            outputs = base_model(**data_buf.get("net_inputs"))
            assert "net_outputs" in outputs
            batch_outputs = outputs.get("net_outputs")
            batch_targets = data_buf.get("net_targets")
            net_outputs.append(buffer_to_cpu(batch_outputs))
            net_targets.append(buffer_to_cpu(batch_targets))

        net_outputs = merge_buffer(*net_outputs)
        net_targets = merge_buffer(*net_targets)

        if dist.is_initialized():
            net_outputs = ddp_sync_buffer(net_outputs)
            net_targets = ddp_sync_buffer(net_targets)

        new_score = score_fn(net_outputs=net_outputs, net_targets=net_targets)
        base_model.train()
        return dict(
            new_score=new_score, net_outputs=net_outputs, net_targets=net_targets
        )

    @torch.no_grad()
    def infer(
        self,
        model,
        data_for_test=None,
        data_for_raw=None,
        output_header=None,
        post_process_fn=None,
        batch_size=128,
        pin_memory=True,
        num_workers=4,
        opt_fp16="O0",
        output_path="./cache/predict.txt",
        save_header=False,
    ):
        assert self.n_gpu <= 1

        sampler = SequentialSampler

        iter_for_test = DataLoader(
            data_for_test,
            sampler=sampler(data_for_test),
            batch_size=batch_size,
            shuffle=False,
            pin_memory=pin_memory,
            num_workers=num_workers,
        )

        iter_for_data = DataLoader(
            data_for_raw,
            sampler=sampler(data_for_raw),
            batch_size=batch_size,
            shuffle=False,
            pin_memory=pin_memory,
            num_workers=num_workers,
        )

        if opt_fp16 != "O0":
            model.half()

        model.eval()
        start = time.time()

        output_file = open(output_path, "w")
        for data_buf, data_raw in zip(iter_for_test, iter_for_data):
            if torch.cuda.is_available():
                data_buf = buffer_to_cuda(data_buf)
            assert "net_inputs" in data_buf
            outputs = model(**data_buf.get("net_inputs"))
            assert "net_outputs" in outputs
            outputs = buffer_to_cpu(outputs)
            batch_outputs = outputs.get("net_outputs")
            batch_outputs = post_process_fn(batch_outputs)

            data_merge = dict(**data_raw, **batch_outputs)
            if output_header is None:
                output_header = data_merge.keys()
            else:
                output_header = output_header + list(batch_outputs.keys())

            values = [data_merge.get(c) for c in output_header]
            for line in zip(*values):
                num = [
                    len(c) if isinstance(c, list) or isinstance(c, tuple) else 1
                    for c in line
                ]
                max_num = max(num)
                assert all((np.array(num) == 1) | (np.array(num) == max_num))
                lines = [
                    (c * max_num if len(c) == 1 else c)
                    if isinstance(c, list) or isinstance(c, tuple)
                    else [c] * max_num
                    for c in line
                ]
                for line in zip(*lines):
                    line = "\t".join(map(str, line))
                    output_file.write(line)
                    output_file.write("\n")
        end = time.time()
        ms = (end - start) * 1000
        logging.info(
            "{:.2f} ms, {:.1f} sample/s".format(ms, (len(data_for_test) / ms * 1000))
        )
