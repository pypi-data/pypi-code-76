from ignite.engine import (create_supervised_trainer,
                           create_supervised_evaluator, Events)
from ignite.metrics import Accuracy, Precision, Recall

from declair import manual
from declair.frameworks.ignite.evaluators import (attach_metrics,
                                                  SacredMetricsLogger,
                                                  SacredOutputSaver)

from .evaluate import thresholded_output_transform

# The function below initializes all necessary bits and pieces to run an
# experiment (using PyTorch-ignite, in this case) and runs it.
# All necessary information needs to come from the `params` argument, which
# corresponds to `params` object from a run definition (see
# examples/sample_configs/run.yaml)
def execute(params, _run):
    """Executes a run given parameters."""
    model = params['model']
    criterion = params['criterion']
    optimizer = manual(params['optimizer'], model.parameters())
    train_loader, validation_loader, test_loader = params['dataset']
    max_epochs = params['max_epochs']

    # Trainer process function
    # the default trainer from create_supervised_trainer outputs only loss,
    # however metrics need y and y_pred to be computed
    trainer_output_transform = lambda x, y, y_pred, loss: (y_pred, y)

    # Define engines which will run the model on the datasets
    # they can be custom and fancy with whatever training/evaluation procedure
    # possible or just generic pre-configured Ignite engines like below
    train_engine = create_supervised_trainer(model, optimizer, criterion, 
                                             output_transform=trainer_output_transform)
    val_engine = create_supervised_evaluator(model)
    test_engine = create_supervised_evaluator(model)

    # Run the model on the validation set after every training epoch.
    @train_engine.on(Events.EPOCH_COMPLETED(every=1))
    def run_val_engine(engine):
        val_engine.run(validation_loader)

    # Run the model on the test set at the very end of training.
    @train_engine.on(Events.COMPLETED)
    def run_test_engine(engine):
        test_engine.run(test_loader)

    # Sort out tracking outputs:
    # - Define metrics to track and attach them to all engines
    # - Use evaluators from declair.frameworks.ignite.evaluate to save outputs
    #   in Sacred
    metrics = {
        'accuracy': Accuracy,
        'precision': {
            'metric': Precision,
            'kwargs': {
                'average': True
            }
        },
        'recall': {
            'metric': Recall,
            'kwargs': {
                'average': True
            }
        }
    }
    attach_metrics(_run, [train_engine, val_engine, test_engine],
                   metrics, output_transform=thresholded_output_transform)

    for evaluator in [SacredMetricsLogger(), SacredOutputSaver()]:
        evaluator.attach(_run, ['train', 'val', 'test'], 
                         train_engine, val_engine, test_engine)

    train_engine.run(train_loader, max_epochs=max_epochs)
    # Output metrics at the end for hyperopt optimization search.
    # The hyperopt optimizer needs to pick a single target metric to optimize.
    return {
        **{'train_{}'.format(key): value for key, value in train_engine.state.metrics.items()},
        **{'val_{}'.format(key): value for key, value in val_engine.state.metrics.items()},
        **{'test_{}'.format(key): value for key, value in test_engine.state.metrics.items()}
    }
