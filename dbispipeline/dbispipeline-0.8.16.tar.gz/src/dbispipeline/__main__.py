"""Declaring the main method of this package."""
import argparse

from dbispipeline.cli.main import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='executes dbis config files')
    # TODO: configurationfile is required but it is i.e. not needed for restore
    parser.add_argument('plan', help='file that holds config')
    parser.add_argument('-f',
                        '--force',
                        action='store_true',
                        help='Run with dirty git')
    parser.add_argument('--dryrun',
                        action='store_true',
                        help='run without sending results to database.')
    parser.add_argument(
        '-m',
        '--mail',
        choices=[None, 'run', 'total'],
        default=None,
        help='Mail notification level. Choose one of [None, \'run\', \'total\''
        ']. If set no None, no mails will be sent. if set to \'run\', one info'
        ' mail will be sent for each run. If set to \'total\', one mail will '
        'be sent after the entire pipeline is complete.')
    parser.add_argument(
        '--restore',
        default=None,
        type=str,
        help='Restores the backup contained in the given file.')
    parser.add_argument(
        '--slurm',
        action='store_true',
        help='send this job to the slurm job queue instead of running it local'
    )
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='increase logging')
    args = parser.parse_args()
    main(args.dryrun, args.force, args.verbose, args.slurm, args.restore,
         args.mail, args.plan)
