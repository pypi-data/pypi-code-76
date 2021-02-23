from dubhe.image import image
from dubhe.service import run
from dubhe.auth import auth
from dubhe.workspace import workspace
from dubhe.dataset import dataset
import os
import sys


def image_create(args):
    ret = image.Image.create(name=args.app_name, overwrite=args.overwrite, debug=args.debug)
    if ret is not None:
        print(f'create image failed: {ret}')
    else:
        print(f'create image {args.app_name} success')


def _checkout_dataset(au: auth.Auth, workspace_id: str, dataset_id: str) -> dataset.Dataset:
    ds, err = dataset.Dataset.load(au, workspace_id, dataset_id)
    if err is not None:
        print("run image error:", err, file=sys.stderr)
        return None

    def checkout_process():
        print(".", end="")

    print(f'checkout dataset {dataset_id}:')
    dataset.Dataset.checkout(checkout_process, au, dataset_id)
    print("\nSuccess")

    return ds


def image_run(args):
    # todo, parameters fix
    au = auth.Auth.load_active()
    active_wp_id = workspace.Workspace.load_active_id(au)

    # wp, err = workspace.Workspace.load(au, active_wp_id)

    # todo, check if checkout success
    if args.method == 'train':
        input_train = None
        input_valid = None
        if args.input_train is not None:
            input_train = _checkout_dataset(au, active_wp_id, args.input_train)
            if input_train is None:
                return
        else:
            print("error: the following arguments are required: --input_train", file=sys.stderr)

        if args.input_valid is not None:
            input_valid = _checkout_dataset(au, active_wp_id, args.input_valid)
            if input_valid is None:
                return

        err = run.run_train(os.getcwd(), args.method, args.id, input_train, input_valid)
        if err is not None:
            print("run_train image error:", err, file=sys.stderr)
    elif args.method == 'predict':
        input_test = None
        output_ds = None
        if args.input_test is not None:
            input_test = _checkout_dataset(au, active_wp_id, args.input_test)
            if input_test is None:
                return
        else:
            print("error: the following arguments are required: --input_train", file=sys.stderr)

        if args.output is not None:
            output_ds = _checkout_dataset(au, active_wp_id, args.output)
            if output_ds is None:
                return

        err = run.run_predict(os.getcwd(), args.method, args.id, input_test, output_ds)
        if err is not None:
            print("run_predict image error:", err, file=sys.stderr)
    else:
        print("unknown method:", args.method, file=sys.stderr)
