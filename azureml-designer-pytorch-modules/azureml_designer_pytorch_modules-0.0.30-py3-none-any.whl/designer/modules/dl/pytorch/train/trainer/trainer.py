import time

import torch

from azureml.designer.modules.dl.pytorch.common.pytorch_utils import raise_error
from azureml.designer.modules.dl.pytorch.train.trainer.trainer_utils import AverageMeter
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping


class ClassificationTrainer:
    def __init__(self, model):
        self.model = model

    def fit(self,
            train_set=None,
            valid_set=None,
            epochs=None,
            batch_size=None,
            lr=0.001,
            wd=0.0001,
            momentum=0.9,
            random_seed=None,
            patience=10):
        ErrorMapping.verify_less_than_or_equal_to(value=batch_size, b=len(train_set),
                                                  arg_name='Batch size', b_name='train data count')
        logger.info('Torch cuda random seed setting.')
        # Torch cuda random seed setting
        if random_seed is not None:
            if torch.cuda.is_available():
                if torch.cuda.device_count() > 1:
                    torch.cuda.manual_seed_all(random_seed)
                else:
                    torch.cuda.manual_seed(random_seed)
            else:
                torch.manual_seed(random_seed)

        logger.info("Data start loading.")
        # Set data loader
        train_loader = torch.utils.data.DataLoader(train_set,
                                                   batch_size=batch_size,
                                                   shuffle=True,
                                                   pin_memory=(torch.cuda.is_available()),
                                                   num_workers=0,
                                                   drop_last=True)
        valid_loader = torch.utils.data.DataLoader(valid_set,
                                                   batch_size=batch_size,
                                                   shuffle=False,
                                                   pin_memory=(torch.cuda.is_available()),
                                                   num_workers=0)
        if torch.cuda.is_available():
            self.model = self.model.cuda()

        logger.info(f'Device count: {torch.cuda.device_count()}')
        if torch.cuda.device_count() > 1:
            self.model = torch.nn.parallel.DataParallel(self.model).cuda()

        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr, momentum=momentum, nesterov=True, weight_decay=wd)
        scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[0.5 * epochs, 0.75 * epochs], gamma=0.1)
        logger.info('Start training epochs.')
        best_error = 1
        counter = 0
        last_epoch_valid_loss = -1
        best_model = self.model
        for epoch in range(epochs):
            scheduler.step(epoch=epoch)
            try:
                _, train_loss, train_error = self.train_one_epoch(loader=train_loader,
                                                                  optimizer=optimizer,
                                                                  epoch=epoch,
                                                                  epochs=epochs)
            except Exception as e:
                raise_error(e, batch_size=batch_size)

            try:
                _, valid_loss, valid_error, _ = self.evaluate(loader=valid_loader)
            except Exception as e:
                raise_error(e, mode='Validation')

            # Determine if model is the best
            if valid_error < best_error:
                is_best = True
                best_error = valid_error
            else:
                is_best = False

            # Early stop
            if epoch == 0:
                last_epoch_valid_loss = valid_loss
            else:
                if valid_loss >= last_epoch_valid_loss:
                    counter += 1
                else:
                    counter = 0
                last_epoch_valid_loss = valid_loss

            logger.info(f'Valid loss did not decrease consecutively for {counter} epoch')
            # TODO: save checkpoint files, but removed now to increase web service deployment efficiency.
            logger.info(','.join([
                f'Epoch {epoch + 1:d}', f'train_loss {train_loss:.6f}', f'train_error {train_error:.6f}',
                f'valid_loss {valid_loss:.5f}', f'valid_error {valid_error:.5f}'
            ]))
            if is_best:
                logger.info(f'Get better top1 accuracy: {1-best_error:.4f}, best checkpoint will be updated.')
                best_model = self.model

            early_stop = True if counter >= patience else False
            if early_stop:
                logger.info("Early stopped.")
                break

        return best_model

    def train_one_epoch(self, loader, optimizer, epoch, epochs, print_freq=1):
        """Training process every epoch.

        :param self:
        :param loader: torch.utils.data.DataLoader
        :param optimizer: torch.optim
        :param epoch: int
        :param epochs: int
        :param print_freq: int
        :return average batch_time, loss, error: float, float, float
        """
        batch_time = AverageMeter()
        losses = AverageMeter()
        error = AverageMeter()
        # Model on train mode
        self.model.train()
        end = time.time()
        batches = len(loader)
        for batch_idx, (input, target) in enumerate(loader):
            # Create variables
            if torch.cuda.is_available():
                input = input.cuda()
                target = target.cuda()

            # Compute output
            output = self.model(input)
            loss = torch.nn.functional.cross_entropy(output, target)
            # Measure accuracy and record loss
            batch_size = target.size(0)
            _, pred = output.data.cpu().topk(1, dim=1)
            error.update(torch.ne(pred.squeeze(), target.cpu()).float().sum().item() / batch_size, batch_size)
            losses.update(loss.item(), batch_size)
            # Compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # Measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()
            if batch_idx % print_freq == 0:
                res = '\t'.join([
                    f'Epoch: [{epoch + 1}/{epochs}]', f'Iter: [{batch_idx + 1}/{batches}]',
                    f'Avg_Time_Batch/Avg_Time_Epoch: {batch_time.val:.3f}/{batch_time.avg:.3f}',
                    f'Avg_Loss_Batch/Avg_Loss_Epoch: {losses.val:.4f}/{losses.avg:.4f}',
                    f'Avg_Error_Batch/Avg_Error_Epoch: {error.val:.4f}/{error.avg:.4f}'
                ])
                logger.info(res)

        # Return summary statistics
        return batch_time.avg, losses.avg, error.avg

    def evaluate(self, loader, print_freq=1):
        batch_time = AverageMeter()
        losses = AverageMeter()
        error = AverageMeter()
        # Model on eval mode
        self.model.eval()
        end = time.time()
        target_list = []
        pred_top1_list = []
        # Disabling gradient calculation for inference, which will reduce memory consumption for computations.
        with torch.no_grad():
            for batch_idx, (input, target) in enumerate(loader):
                # Create variables
                if torch.cuda.is_available():
                    input = input.cuda()
                    target = target.cuda()
                # compute output
                output = self.model(input)
                loss = torch.nn.functional.cross_entropy(output, target)
                # measure accuracy and record loss
                batch_size = target.size(0)
                _, pred = output.data.cpu().topk(1, dim=1)
                target_list += target.tolist()
                pred_top1_list += [i[0] for i in pred.tolist()]
                error.update(torch.ne(pred.squeeze(), target.cpu()).float().sum().item() / batch_size, batch_size)
                losses.update(loss.item() / batch_size, batch_size)
                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()
                # print stats
                if batch_idx % print_freq == 0:
                    res = '\t'.join([
                        'Validation',
                        'Iter: [{:d}/{:d}]'.format(batch_idx + 1, len(loader)),
                        'Avg_Time_Batch/Avg_Time_Epoch: {:.3f}/{:.3f}'.format(batch_time.val, batch_time.avg),
                        'Avg_Loss_Batch/Avg_Loss_Epoch: {:.4f}/{:.4f}'.format(losses.val, losses.avg),
                        'Avg_Error_Batch/Avg_Error_Epoch: {:.4f}/{:.4f}'.format(error.val, error.avg),
                    ])
                    logger.info(res)

        # Return summary statistics
        return batch_time.avg, losses.avg, error.avg, (target_list, pred_top1_list)
