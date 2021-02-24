"""
The shared callback logic

expects to be called as part of a class with the properties:
* instance.should_whitelist
* instance.category
* instance.analyzer
* instance.white_lister
"""
import re

from qai.issues.meta import get_meta_value


def _is_valid(instance):
    assert instance.should_whitelist is not None
    assert instance.category is not None
    assert instance.analyzer is not None


def _has_callable(instance, method):
    return hasattr(instance, method) and callable(getattr(instance, method))


def _filter_0distance(segment, issues):
    """
    filter issues to drop 0-distance edits
    :param issues: issues to filter
    :return: filter issues
    """
    filtered_issues = []
    for issue in issues:
        if issue["suggestions"]:
            suggestions = []
            for suggestion in issue["suggestions"]:
                # shouldn't lowercase, as this would prevent capitalization fixes
                # e.g. this would prevent 1-distance edits
                # but without it, this doesn't work, for unexplained reasons
                if (segment[issue["from"]: issue["until"]]) == suggestion:
                    continue
                suggestions.append(suggestion)

            if suggestions:
                issue["suggestions"] = suggestions
                filtered_issues.append(issue)
        else:  # some services don't offer suggestions, so no need to check
            filtered_issues.append(issue)
    return filtered_issues


def _extract_quotes(segment):
    quotes = []
    for m in re.finditer(r'"((?!").)+"', segment):
        quotes.append({'start': m.start(), 'end': m.end()})
    return quotes


def _inside_quote(quotes: list, issues):
    if len(quotes):
        issues_outside = []
        for issue in issues:
            drop_issue = False
            for quote in quotes:
                if issue['from'] >= quote['start'] and issue['until'] <= quote['end']:
                    drop_issue = True
                    break
            if not drop_issue:
                issues_outside.append(issue)
        return issues_outside
    return issues


def qallback(instance, segment, metadata, language, content):
    """
    Helper libs won't memoize this for us, because
    "Arguments to memoized function must be hashable"
    so we need to build it ourselves... weakass Python can't hash class instances
    """
    _is_valid(instance)

    if language not in instance.supported_languages:
        print(
            f"Received language {language}, supported Languages: {instance.supported_languages}"
        )
        return []

    # first param is now dealt with by mediator, we don't have to look at it
    _, meta_value, sub_groups = get_meta_value(instance.category, metadata)

    if _has_callable(instance.analyzer, "analyze_with_full_meta"):
        issues = instance.analyzer.analyze_with_full_meta(segment, meta=metadata)
    elif _has_callable(instance.analyzer, "analyze_with_metadata"):
        issues = instance.analyzer.analyze_with_metadata(
            segment, language=language, meta_value=meta_value, sub_groups=sub_groups
        )
    elif _has_callable(instance.analyzer, 'analyze_with_full_payload'):
        # meta_value not implemented in this method, as it is removed from payload
        # TODO clean up meta_value code
        issues = instance.analyzer.analyze_with_full_payload(
            segment, language=language, sub_groups=sub_groups, meta=metadata, content=content
        )
    else:
        issues = instance.analyzer.analyze(segment)

    if instance.should_whitelist:
        # Should we have whitelisting on? This is a per-service setting;
        # e.g. Passive voice => no whitelisting
        # Gender bias => whitelisting
        issues = instance.white_lister(issues, meta_value, sub_groups)

    if len(issues):
        # filter issues to drop 0-distance edits
        if isinstance(issues[0], list):  # issues is List[List[dict]]
            filtered_issues = []
            for issues_list, sentence in zip(issues, segment):
                filtered_0distance_issues = _filter_0distance(sentence, issues_list)
                # drop issues inside quotes
                if instance.ignore_inside_quotes:
                    filtered_issues.append(_inside_quote(_extract_quotes(sentence), filtered_0distance_issues))
                else:
                    filtered_issues.append(filtered_0distance_issues)
        else:  # List[dict]
            # drop issues inside quotes
            if instance.ignore_inside_quotes:
                filtered_issues = _inside_quote(_extract_quotes(segment), _filter_0distance(segment, issues))
            else:
                filtered_issues = _filter_0distance(segment, issues)
        return filtered_issues
    else:
        return issues
