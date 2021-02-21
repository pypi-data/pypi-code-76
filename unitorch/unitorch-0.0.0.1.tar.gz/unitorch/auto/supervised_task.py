import os
import torch
from functools import partial
from unitorch.tasks.base import supervised_task
from unitorch.functions import parser_process_function
from unitorch.utils.decorators import (
    add_default_section_for_init,
    add_default_section_for_instance_function,
)
from unitorch import (
    core_model,
    core_optim,
    core_loss,
    core_score,
    core_dataset,
    core_scheduler,
    core_process,
    register_task,
)


def parser_postprocess_function(process_func_str):
    ret = parser_process_function(process_func_str)
    function = ret.get("function")
    args = ret.get("args")
    kwargs = ret.get("kwargs")
    if function in core_process:
        return core_process.get(function)

    assert function == "partial" and len(args) == 1 and args[0] in core_process
    function = core_process.get(args[0])
    kwargs = {k: eval(v) for k, v in kwargs.items()}
    return partial(function, **kwargs)


@register_task("core/auto/supervised_task")
class core_supervised_task(supervised_task):
    def __init__(
        self,
        model=None,
        opt=None,
        dataset=None,
        loss_fn=None,
        score_fn=None,
        monitor_fns=None,
        scheduler=None,
        output_header=None,
        post_process_fn=None,
        from_ckpt_dir="./from_ckpt/",
        seed=1123,
        local_rank=-1,
    ):
        super().__init__(seed)
        self.model = model
        self.opt = opt
        self.dataset = dataset
        self.loss_fn = loss_fn
        self.score_fn = score_fn
        self.monitor_fns = monitor_fns
        self.scheduler = scheduler
        self.output_header = output_header
        self.post_process_fn = post_process_fn
        self.local_rank = local_rank

        if local_rank != -1:
            torch.cuda.set_device(local_rank)

        if torch.cuda.is_available():
            model.cuda()

        if os.path.exists(from_ckpt_dir):
            self.model.from_checkpoint(from_ckpt_dir)

        if opt is not None:
            self.opt = opt(self.model.parameters())

    @classmethod
    @add_default_section_for_init("core/auto/supervised_task")
    def init_from_core_configure(cls, cfg, **kwargs):
        cfg.set_default_section("core/auto/supervised_task")
        model = cfg.getoption("model", None)
        optim = cfg.getoption("optim", None)
        dataset = cfg.getoption("dataset", None)
        loss_fn = cfg.getoption("loss_fn", None)
        score_fn = cfg.getoption("score_fn", None)
        monitor_fns = cfg.getoption("monitor_fns", None)
        output_header = cfg.getoption("output_header", None)
        post_process_fn = cfg.getoption("post_process_fn", None)
        local_rank = cfg.getdefault("core/auto", "local_rank", -1)

        assert model is not None and dataset is not None

        if monitor_fns is not None:
            monitor_fns = eval(monitor_fns)
        else:
            monitor_fns = []

        if output_header is not None:
            output_header = output_header.split(",")

        post_process_fn = parser_postprocess_function(post_process_fn)

        return dict(
            model=core_model.get(model),
            opt=core_optim.get(optim),
            dataset=core_dataset.get(dataset),
            loss_fn=core_loss.get(loss_fn),
            score_fn=core_score.get(score_fn),
            monitor_fns=[core_score.get(fn) for fn in monitor_fns],
            scheduler=None,
            output_header=output_header,
            post_process_fn=post_process_fn,
            local_rank=local_rank,
        )

    @add_default_section_for_instance_function("core/auto/supervised_task")
    def train(
        self,
        to_ckpt_dir="./to_ckpt/",
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
        dataset_for_train = self.dataset.get("train")
        dataset_for_dev = self.dataset.get("dev")
        assert dataset_for_train is not None and dataset_for_dev is not None
        assert (
            self.opt is not None
            and self.loss_fn is not None
            and self.score_fn is not None
        )

        super().train(
            model=self.model,
            opt=self.opt,
            dataset_for_train=dataset_for_train,
            dataset_for_dev=dataset_for_dev,
            loss_fn=self.loss_fn,
            score_fn=self.score_fn,
            monitor_fns=self.monitor_fns,
            scheduler=None,
            to_ckpt_dir=to_ckpt_dir,
            local_rank=self.local_rank,
            train_batch_size=train_batch_size,
            dev_batch_size=dev_batch_size,
            pin_memory=pin_memory,
            num_workers=num_workers,
            opt_fp16=opt_fp16,
            log_freq=log_freq,
            ckpt_freq=ckpt_freq,
            grad_acc_step=grad_acc_step,
            max_grad_norm=max_grad_norm,
            epochs=epochs,
        )

    @torch.no_grad()
    @add_default_section_for_instance_function("core/auto/supervised_task")
    def infer(
        self,
        test_batch_size=128,
        pin_memory=True,
        num_workers=4,
        opt_fp16="O0",
        output_path="./cache/predict.txt",
        save_header=False,
    ):
        data_for_test = self.dataset.get("test")
        assert data_for_test is not None and hasattr(data_for_test, "dataset")
        assert self.post_process_fn is not None
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        super().infer(
            model=self.model,
            data_for_test=data_for_test,
            data_for_raw=data_for_test.dataset,
            output_header=self.output_header,
            post_process_fn=self.post_process_fn,
            batch_size=test_batch_size,
            pin_memory=pin_memory,
            num_workers=num_workers,
            opt_fp16=opt_fp16,
            output_path=output_path,
            save_header=save_header,
        )
