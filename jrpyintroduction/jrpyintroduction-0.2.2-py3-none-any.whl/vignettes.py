import webbrowser
from pkg_resources import resource_listdir
from pkg_resources import resource_filename


def browse():
    """
    List all of the vignettes available for this package.
    """
    outs = _get_vignette_titles()

    if len(outs) > 0:
        print("\nAvailable documents: \n")
        print("\n".join(outs))
        print(f"\nTo open use e.g load('{outs[0]}')\n")
    else:
        print("\nNo documents available\n")


def load(name):
    """
    Open a particular vignette from the package.
    """
    outs = _get_vignette_titles()
    if name in outs:
        path = resource_filename("jrpyintroduction", f"vignettes/{name}")
        webbrowser.open_new(path)
    else:
        print(f"\nVignette '{name}' not found")
        browse()


def _get_vignette_titles():
    x = resource_listdir("jrpyintroduction", "vignettes")
    # grab only those which are pdfs or html
    pdfs = [file for file in x if file.endswith(".pdf")]
    htmls = [file for file in x if file.endswith(".html")]
    # Concat pdfs and htmls
    outs = pdfs + htmls
    # Return in some legible order
    outs.sort()
    return outs
