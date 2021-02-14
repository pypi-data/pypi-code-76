#!/usr/bin/env python
import logging
import re

from intermine.webservice import Service

logger = logging.getLogger(__name__)


def fetch_from_sgd() -> dict:
    """Query SGD's intermine service and return an up-to-date dict of S. Cerevisiae features (genes).
    Returned is a dictionary of "SGD_ID" -> dict of feature data. Keys in feature data are:
    sgd_id, feature_qualifier, feature_type, orf, name, aliases, chromosome, chromosomal_location, start_coordinate,
    stop_coordinate, description

    :rtype: dict
    """
    re_num = re.compile(r'(\d+)')

    service = Service("https://yeastmine.yeastgenome.org/yeastmine/service")

    query = service.new_query("Gene")
    query.add_view(
        "primaryIdentifier", "featureType", "qualifier", "secondaryIdentifier",
        "symbol", "chromosomeLocation.start", "chromosomeLocation.end",
        "description", "synonyms.value"
    )

    query.add_constraint("organism.shortName", "=", "S. cerevisiae", code="A")
    query.add_constraint("featureType", "=", "ORF", code="C")

    genes = {}

    logger.debug("Executing query on yeastmine")
    for row in query.rows():
        sgd_id = row["primaryIdentifier"]
        orf = row["secondaryIdentifier"]

        orfnum = re_num.findall(orf)
        if orfnum:
            orfnum = int(orfnum[0])
        else:
            orfnum = 0

        if orf.startswith('Q'):
            chrom = 0
        else:
            chrom = ord(orf[1]) - 64
            if orf[2] == 'L':
                orfnum = -orfnum

        if sgd_id not in genes:
            logger.debug(f"Parsing new ORF: {orf}")
            genes[sgd_id] = {
                'sgd_id': row["primaryIdentifier"],
                'feature_qualifier': row["qualifier"],
                'feature_type': row['featureType'],
                'orf': orf,
                'name': row["symbol"],
                'aliases': [],
                'chromosome': chrom,
                'chromosomal_location': orfnum,
                'start_coordinate': str(row["chromosomeLocation.start"]),
                'stop_coordinate': str(row["chromosomeLocation.end"]),
                'description': row["description"],
            }

        if row["synonyms.value"] not in (orf, row["symbol"]):
            genes[sgd_id]['aliases'].append(row["synonyms.value"])

    return genes


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Fetch Saccharomyces Cerevisiae\'s features')
    parser.add_argument('-o', '--output', dest='output', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()

    features = fetch_from_sgd()

    for sgdid, gene in sorted(features.items(), key=lambda x: (x[1]['chromosome'], x[1]['chromosomal_location'])):
        output_row = [
            sgdid,
            gene['feature_type'] or '',
            gene['feature_qualifier'] or '',
            gene['orf'],
            gene['name'] or '',
            str(gene['chromosome']),
            gene['start_coordinate'],
            gene['stop_coordinate'],
            gene['description'],
            '|'.join(gene['aliases'])
        ]

        args.output.write('\t'.join(output_row) + '\n')


if __name__ == '__main__':
    main()
