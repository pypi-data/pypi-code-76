import traceback

from qai.qconnect.qallback import qallback


def parse(el):
    segment = el["content"]["segment"]
    metadata = el["chain"]["meta"]
    language = el["content"]["languageCode"].split("-")[0]
    content = el['content']
    return segment, metadata, language, content


def add_issues(el, issues):
    el["issues"] = issues
    return el


def mock_batch_output(els):
    # Mock no issue batch prediction output
    output_els = []
    for el in els:
        el = add_issues(el, [])  # issues = []
        output_els.append(el)
    return output_els


def add_issues_format_insensitive(instance, el, validator, debug=False, verbose=False):
    # We should pull some of this code out soon
    # Why write it then? because I don't trust the calling services
    # to do what Yakiv says will happen
    segment, metadata, language, content = parse(el)

    # try except in case of unforseen problems
    issues = []
    try:
        # envisioned scenario
        # here we would like the validation
        # if validator says "no, shall not pass"
        # -> we don't callback, just return issues = []
        if verbose:
            print(f"Segment: {segment}")

        if validator(segment):
            # if not validator.has_html(segment):
            issues = qallback(instance, segment, metadata, language, content)
    except:
        print(f"Error log for segment {segment}")
        print(traceback.format_exc())

        # Qallback already failed
        # In debug mode we want to see errors so we call it again
        if debug:
            issues = qallback(instance, segment, metadata, language, content)
    finally:
        el = add_issues(el, issues)

    return el


def add_issues_format_insensitive_batch(instance, els, debug=False, verbose=False):
    # Format 1-by-1 but pass batched
    # Dependand service should take care of metdata and language
    # Consistent issue format, otherwise empty response
    # Assumption: same meta and language

    input_els = []
    output_els = []

    for el in els:
        segment, metadata, language, content = parse(el)
        input_els.append(segment)

    try:
        if verbose:
            print(f"Segment: {input_els}")
        el_issues = qallback(instance, input_els, metadata, language, content)
    except:
        print("error log for batch of segments, mocking empty response")
        print(traceback.format_exc())
        # Qallback already failed
        # In debug mode we want to see errors so we call it again
        if debug:
            qallback(instance, input_els, metadata, language, content)
        return mock_batch_output(els)

    for el_issue, el in zip(el_issues, els):
        output_els.append(add_issues(el, el_issue))

    return output_els
