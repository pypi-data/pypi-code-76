import json

if __name__ == '__main__':
    from API_requests import vsearch_species, vsearch_protein, vsearch_vog, \
    get_vsummary_species, get_vsummary_protein, get_vsummary_vog, post_vsummary_species, post_vsummary_protein, \
    post_vsummary_vog, post_vfetch_vog_msa, post_vfetch_vog_hmm, post_vfetch_protein_faa, post_vfetch_protein_fna, \
    get_vfetch_vog_msa, get_vfetch_vog_hmm, get_vfetch_protein_faa, get_vfetch_protein_fna
else:
    from .API_requests import vsearch_species, vsearch_protein, vsearch_vog, \
    get_vsummary_species, get_vsummary_protein, get_vsummary_vog, post_vsummary_species, post_vsummary_protein, \
    post_vsummary_vog, post_vfetch_vog_msa, post_vfetch_vog_hmm, post_vfetch_protein_faa, post_vfetch_protein_fna, \
    get_vfetch_vog_msa, get_vfetch_vog_hmm, get_vfetch_protein_faa, get_vfetch_protein_fna

import sys
import argparse

"""
This is the implementation of the Argument Parser, with several subparsers
Parsing Structure:
Parser      vsearch_parser      species_search_parser
                                protein_search_parser
                                vog_search_parser
                                
            vsummmary_parser    species_summary_parser
                                protein_summary_parser
                                vog_summary_parser
                                
            vfetch_parser       protein_fetch_parser
                                vog_fetch_parser
                                                            
"""


def main():
    parser = argparse.ArgumentParser(description='Welcome to vDirect!', epilog='Thank you for using vDirect!')

    parser.add_argument(type=str, action='store', nargs='?', dest='base_url', help="specify the base URL")

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    vsearch_parser = subparsers.add_parser('vsearch', help='vsearch subparser help')
    vsummary_parser = subparsers.add_parser('vsummary', help='vsummary subparser help')
    vfetch_parser = subparsers.add_parser('vfetch', help='vfetch subparser help')

    # add subparsers for vSearch:
    vsearch_sps = vsearch_parser.add_subparsers(dest='return_object', help='subparsers for vsearch_parser')
    vog_search_parser = vsearch_sps.add_parser('vog', help='vsearch subparser for vog search')
    species_search_parser = vsearch_sps.add_parser('species', help='vsearch subparser for species search')
    protein_search_parser = vsearch_sps.add_parser('protein', help='vsearch subparser for protein search')

    # add arguments for vog_search_parser:
    vog_search_parser.add_argument('-id', type=str, action='append', nargs='+', dest='id',
                                   help="VOG ID(s)")
    vog_search_parser.add_argument('-pmin', type=int, action='store', nargs='?', dest='pmin',
                                   help="minimum number of proteins in the VOG")
    vog_search_parser.add_argument('-pmax', type=int, action='store', nargs='?', dest='pmax',
                                   help="maximum number of proteins in the VOG")
    vog_search_parser.add_argument('-smin', type=int, action='store', nargs='?', dest='smin',
                                   help="minimum number of species in the VOG")
    vog_search_parser.add_argument('-smax', type=int, action='store', nargs='?', dest='smax',
                                   help="maximum number of species in the VOG")
    vog_search_parser.add_argument('-mingLCA', type=int, action='store', nargs='?', dest='mingLCA',
                                   help="minimum number of genomes in the Last common ancestor")
    vog_search_parser.add_argument('-maxgLCA', type=int, action='store', nargs='?', dest='maxgLCA',
                                   help="maximum number of genomes in the Last common ancestor")
    vog_search_parser.add_argument('-mingGLCA', type=int, action='store', nargs='?', dest='mingGLCA',
                                   help="minimum number of genomes in the Group of the Last common ancestor")
    vog_search_parser.add_argument('-maxgGLCA', type=int, action='store', nargs='?', dest='maxgGLCA',
                                   help="maximum number of genomes in the Group of the Last common ancestor")
    vog_search_parser.add_argument('-fctcat', type=str, action='append', nargs='+', dest='functional_category',
                                   choices=['Xu', 'Xh', 'Xp', 'Xr', 'Xs'],
                                   help="functional category: Xu, Xh, Xp, Xr, Xs. If providing more than one, separate"
                                        " them by a space.")
    vog_search_parser.add_argument('-confct', type=str, action='append', nargs='+', dest='consensus_function',
                                   help="Concensus function")
    vog_search_parser.add_argument('-anc', '-ancestors', type=str, action='append', nargs='+', dest='ancestors',
                                   help="Ancestors")
    vog_search_parser.add_argument('-hs', '-highstringency', type=int, action='store', nargs='?', dest='h_stringency',
                                   choices=[0, 1],
                                   help="High stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-ms', '-mediumstringency', type=int, action='store', nargs='?', dest='m_stringency',
                                   choices=[0, 1],
                                   help="Medium stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-ls', '-lowstringency', type=int, action='store', nargs='?', dest='l_stringency',
                                   choices=[0, 1],
                                   help="Low stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-vs', '-virusspecific', type=int, action='store', nargs='?', dest='virus_specific',
                                   choices=[0, 1],
                                   help="Virus specific? '1' for True and '0' for False")
    vog_search_parser.add_argument('-p', '-phage', type=str, action='store', nargs='?', dest='phages_nonphages',
                                   choices=['mixed', 'phages_only', 'np_only'],
                                   help="specify phages_only, nonphages only or mixed")
    vog_search_parser.add_argument('-prot', '-proteins', type=str, action='append', nargs='+', dest='proteins',
                                   help="Protein IDs")
    vog_search_parser.add_argument('-species', type=str, action='append', nargs='+', dest='species',
                                   help="Species Names, enclose names in quotes")
    vog_search_parser.add_argument('-tid', '-taxonid', type=int, action='append', nargs='+', dest='tax_id',
                                   help="Taxonomy ID(s)")
    vog_search_parser.add_argument('-u', '-union', action='store_true', dest='union',
                                   help="Do you want an (u)nion or an (i)ntersection search when searching VOGs by "
                                        "Species names or Taxonomy IDs? Default = False.")

    # add arguments for species_search_parser:
    species_search_parser.add_argument('-id', type=int, action='append', nargs='+', dest='taxon_id',
                                       help="species ID(s)")
    species_search_parser.add_argument('-n', '-name', type=str, action='store', nargs='?', dest='name',
                                       help="search for species name or part of a species name")
    species_search_parser.add_argument('-p', '-phage', type=int, action='store', nargs='?', dest='phage',
                                       help="Enter '1' for searching for phages only and '0' when wanting to search "
                                            "for nonphages only")
    species_search_parser.add_argument('-s', '-source', type=str, action='store', nargs='?', dest='source',
                                       help="search for species found in the specified source")

    # add arguments for protein_search_parser:
    protein_search_parser.add_argument('-tid', '-taxonid', type=int, action='append', nargs='+', dest='taxon_id',
                                       help="taxon ID(s) of the species")
    protein_search_parser.add_argument('-n', '-name', type=str, action='append', nargs='+', dest='species_name',
                                       help="search for species name or part of species name")
    protein_search_parser.add_argument('-vid', '-vogid', type=str, action='append', nargs='+', dest='VOG_id',
                                       help="search for VOG IDs")

    # add subparsers for vSummary:
    vsummary_sps = vsummary_parser.add_subparsers(dest='return_object', help='subparsers for vsummary_parser')
    vog_summary_parser = vsummary_sps.add_parser('vog', help='vsummary subparser for vog summary')
    species_summary_parser = vsummary_sps.add_parser('species', help='vsummary subparser for species summary')
    protein_summary_parser = vsummary_sps.add_parser('protein', help='vsummary subparser for protein summary')

    # add arguments for vog_summary_parser:
    vog_summary_parser.add_argument('-id', type=str, nargs='+', dest='id', default=None,
                                    help="VOG unique ID(s)")

    # add arguments for protein_summary_parser:
    protein_summary_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                        help="protein ID(s)")

    # add arguments for species_summary_parser:
    species_summary_parser.add_argument('-id', type=int, nargs='+', dest='id', default=sys.stdin,
                                        help="taxon ID(s)")

    # add subparsers for vFetch:
    vfetch_sps = vfetch_parser.add_subparsers(dest='return_object', help='subparsers for vfetch_parser')
    vog_fetch_parser = vfetch_sps.add_parser('vog', help='vfetch subparser for vog fetch')
    protein_fetch_parser = vfetch_sps.add_parser('protein', help='vfetch subparser for protein fetch')

    # add arguments for vog_fetch_parser:
    vog_fetch_parser.add_argument(type=str, action='store', choices=['hmm', 'msa'],
                                  dest='return_type', help="choose 'hmm' or 'msa'")
    vog_fetch_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                  help="VOG unique identifiers")

    # add arguments for protein_fetch_parser:
    protein_fetch_parser.add_argument(type=str, action='store', choices=['faa', 'fna'],
                                      dest='return_type', help="choose 'faa' or 'fna'")
    protein_fetch_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                      help="Protein identifiers")

    args = parser.parse_args()

    # FETCH:
    if args.command == 'vfetch':
        # if ID parameter given
        if args.id:
            if args.return_object == 'vog':
                if args.return_type == 'msa':
                    r = get_vfetch_vog_msa(base_url=args.base_url, id=args.id)
                elif args.return_type == 'hmm':
                    r = get_vfetch_vog_hmm(base_url=args.base_url, id=args.id)
                else:
                    raise Exception("Invalid return type")
            elif args.return_object == 'protein':
                if args.return_type == 'faa':
                    r = get_vfetch_protein_faa(base_url=args.base_url, id=args.id)
                elif args.return_type == 'fna':
                    r = get_vfetch_protein_fna(base_url=args.base_url, id=args.id)
                else:
                    raise Exception("Invalid return type")
            else:
                raise Exception("Invalid return object")

        # if no ids given as parameters -> read from stdin
        else:
            inp = sys.stdin.read()
            if args.return_object == 'protein':
                if args.return_type == 'faa':
                    r = post_vfetch_protein_faa(base_url=args.base_url, input=inp)
                elif args.return_type == 'fna':
                    r = post_vfetch_protein_fna(base_url=args.base_url, input=inp)
                else:
                    raise Exception("Invalid return type")
            elif args.return_object == 'vog':
                if args.return_type == 'msa':
                    r = post_vfetch_vog_msa(base_url=args.base_url, input=inp)
                elif args.return_type == 'hmm':
                    r = post_vfetch_vog_hmm(base_url=args.base_url, input=inp)
                else:
                    raise Exception("Invalid return type")
            else:
                raise Exception("Invalid return object")

        if r.status_code == 200:
            print(json.dumps(r.json()), file=sys.stdout)
        else:
            print(r.json().get('detail'), file=sys.stderr)
            sys.exit(1)


    # SUMMARY:
    elif args.command == 'vsummary':
        # if ID parameter given
        if args.id:
            if args.return_object == 'species':
                r = get_vsummary_species(taxon_id=args.id, base_url=args.base_url)

            elif args.return_object == 'protein':
                r = get_vsummary_protein(id=args.id, base_url=args.base_url)

            elif args.return_object == 'vog':
                r = get_vsummary_vog(id=args.id, base_url=args.base_url)
            else:
                raise Exception("Invalid return object")

        # if no ids given as parameters -> read from stdin
        else:
            inp = sys.stdin.read()
            if args.return_object == 'species':
                r = post_vsummary_species(base_url=args.base_url, input=inp)
            elif args.return_object == 'protein':
                r = post_vsummary_protein(base_url=args.base_url, input=inp)
            elif args.return_object == 'vog':
                print("VOG SUMMARy")
                r = post_vsummary_vog(base_url=args.base_url, input=inp)
            else:
                raise Exception("Invalid return object")

        if r.status_code == 200:
            print(json.dumps(r.json()), file=sys.stdout)
        else:
            print(r.json().get('detail'), file=sys.stderr)
            sys.exit(1)


    # SEARCHES:
    elif args.command == 'vsearch':
        if args.return_object == 'species':
            r = vsearch_species(base_url=args.base_url, taxon_id=args.taxon_id, name=args.name, phage=args.phage,
                                source=args.source)

        elif args.return_object == 'protein':
            r = vsearch_protein(base_url=args.base_url, species_name=args.species_name, taxon_id=args.taxon_id,
                                VOG_id=args.VOG_id)

        elif args.return_object == 'vog':
            r = vsearch_vog(base_url=args.base_url, id=args.id, pmin=args.pmin, pmax=args.pmax, smin=args.smin,
                            smax=args.smax, functional_category=args.functional_category, consensus_function=args.consensus_function,
                            mingLCA=args.mingLCA, maxgLCA=args.maxgLCA, mingGLCA=args.mingGLCA, maxgGLCA=args.maxgGLCA,
                            ancestors=args.ancestors, h_stringency=args.h_stringency, m_stringency=args.m_stringency,
                            l_stringency=args.l_stringency, virus_specific=args.virus_specific,
                            phages_nonphages=args.phages_nonphages, proteins=args.proteins, species=args.species,
                            tax_id=args.tax_id, union=args.union)
        else:
            raise ValueError("Invalid return object")

        if r.status_code == 200:
            if len(r.text) == 0:
                raise Exception("No matches for the search criteria.")
            else:
                print(r.text, file=sys.stdout)
        else:
            print(r.json().get('detail'), file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
