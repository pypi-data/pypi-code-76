from logging import StreamHandler, getLogger
import audiolipsum
import click
import os


@click.command()
@click.argument('number', default=3)
@click.option('-lf', '--low-frequency', default=16, show_default=True)
@click.option('-hf', '--high-frequency', default=7902, show_default=True)
@click.option('-d', '--duration', default=60, show_default=True)
@click.option('-o', '--outdir', default='')
@click.option('-p', '--file-prefix', default='file-', show_default=True)
@click.option('--debug', is_flag=True)
def main(
    number,
    low_frequency,
    high_frequency,
    duration,
    outdir,
    file_prefix,
    debug
):
    """
    Generate a number of MP3 files with tones from an optional frequency range.

    Args:
        number (int): The number of files to generate.
        low_frequency (int): The lowest frequency to generate a tone at.
            Defaults to 16.
        high_frequency (int): The highest frequency to generate a tone at.
            Defaults to 7902.
        duration (int): The desired duration of the audio file in seconds.
            Defaults to 60.
        outdir (str): The directory to output files to.
            Defaults to the current working directory.
        file_prefix (str): The prefix for each generated file's name.
            Defaults to 'file-'.
        debug (bool): Enable debug logging.
            Defaults to False.

        Raises:
            click.FileError: If the output directory can't be found.
    """

    count = 0
    handler = StreamHandler()
    root = getLogger('opawg.audiolipsum')

    root.setLevel(debug and 'DEBUG' or 'INFO')
    root.addHandler(handler)

    click.echo('Audio Lipsum, by OPAWG (v%s)' % audiolipsum.__version__)
    click.echo()

    outdir = os.path.join(os.getcwd(), outdir)
    if not os.path.exists(outdir):
        raise click.FileError(outdir, 'Path does not exist')

    for source in audiolipsum.generate_mp3s(
        number,
        low_freq=low_frequency,
        high_freq=high_frequency,
        duration=duration
    ):
        count += 1
        filename = os.path.join(outdir, '%s%d.mp3' % (file_prefix, count))
        root.info('Saved %s' % filename)

        with open(filename, 'wb') as dest:
            dest.write(source.read())

    root.info(
        'Generated %d file%s in %s' % (
            count,
            count != 1 and 's' or '',
            outdir
        )
    )
