#! /usr/bin/env python

# Copyright (C) 2020 GMPG, MPI for History of Science

import json
import re
import urllib.parse
import pysolr
import pandas as pd
import numpy as np
import time
from collections import Counter


class GenerateCitationNet():
    """
    Generats a network of publications by citations or references using Crossref.

    For a given input DOI edges to future nodes are generated,
    if future publications cite the input DOI.
    For this case the source DOI is the citing paper,
    while the target DOI is the referenced paper.
    """
    def __init__(
        self,
        solrURL='http://gmpg-intern.mpiwg-berlin.mpg.de:18983/solr',
        solrCollection='crossref2'
    ):
        self.resultDF = ''
        self.startDoi = ''
        self.mainNode = ''
        self.solr_url = solrURL
        self.collection = solrCollection
        self.solr = pysolr.Solr(
                        '{0}/{1}'.format(self.solr_url, self.collection),
                        timeout=30
                        )

    def test():
        """Test import."""
        print('Import works.')

    def _nodeDict(self, nodeName, nodeTitle, refbyCount, nodeYear):
        """Create node entry."""
        if nodeName == self.startDoi:
            inputDOI = 'True'
        else:
            inputDOI = 'False'
        res = {
          "label": nodeName,
          "x": 0,
          "y": 0,
          "id": nodeName,
          "attributes": {
            "name": nodeName,
            "title": nodeTitle,
            "nodeyear": nodeYear,
            "ref-by-count": refbyCount,
            "is_input_DOI": inputDOI
          },
          "color": "rgb(0,0,0)",
          "size": 10
        }
        return res

    def _edgeDict(self, idx, source, target, year, linkType):
        """Create edge entry."""
        res = {
          "source": source,
          "target": target,
          "id": idx,
          "attributes": {
            "year": year,
            "type": linkType
          },
          "color": "rgb(0,0,0)",
          "size": 1
        }
        return res

    def getPubDate(self, resdata):
        dateKeys = [
            'published-print.date-parts',
            'issued.date-parts',
            'published-online.date-parts'
            ]
        years = [
            x[0] for x in [resdata[key] for key in dateKeys if key in resdata.keys()]
            ]
        try:
            return Counter(years).most_common(1)[0][0]
        except IndexError:
            return ''

    def findYear(self, row):
        year = re.findall(r'\(\d{4}\)|\s\d{4}\)', row)
        if year and len(year) == 1:
            year = year[0].strip().strip(')|(')
        elif year and len(year) > 1:
            year = 'No unique'
        else:
            year = ''
        return year

    def getNodeData(self, resData, direction='target'):
        dateKeys = [
            'published-print.date-parts',
            'issued.date-parts',
            'published-online.date-parts'
            ]
        years = [
            x[0] for x in [resData[key] for key in dateKeys if key in resData.keys()]
            ]
        try:
            foundYear = Counter(years).most_common(1)[0][0]
        except IndexError:
            foundYear = ''

        resDict = {f'{direction}Year': foundYear}
        keyPairs = [
            (f'{direction}DOI', 'DOI'),
            (f'{direction}refCount', 'reference-count'),
            (f'{direction}is_ref_byCount', 'is-referenced-by-count'),
            (f'{direction}titleStr', 'title'),
            (f'{direction}FirstAuthor', 'author.family'),
            (f'{direction}Journal', 'container-title')
        ]
        for key1, key2 in keyPairs:
            if key2 in resData.keys():
                resDict[key1] = resData[key2][0]
            else:
                resDict[key1] = ''
        return resDict

    def getMainNode(self, doi):
        flDict = {
            'rows': 1,
            'fl': 'DOI, reference-count, is-referenced-by-count, author.family,\
            title, published-print.date-parts, issued.date-parts,\
            published-online.date-parts, container-title, reference.DOI,\
            reference.unstructured'
            }
        search = self.solr.search(f'DOI:"{doi}"', **flDict)
        result = [x for x in search]
        if result:
            data = result[0]
            inyear = self.getPubDate(data)
            self.mainNode = (
                doi,
                data['title'],
                data['is-referenced-by-count'],
                inyear
            )
            return 'Done'
        else:
            return 'No data'

    def getCitationsDF(self, doi):
        flDict = {
            'rows': 1,
            'fl': 'DOI, reference-count, is-referenced-by-count, author.family,\
            title, published-print.date-parts, issued.date-parts,\
            published-online.date-parts, container-title, reference.DOI,\
            reference.unstructured'
            }
        start_time = time.time()
        search = self.solr.search(f'DOI:"{doi}"', **flDict)
        result = [x for x in search]
        if result:
            data = result[0]
            inyear = self.getPubDate(data)
            try:
                injournal = data['container-title'][0]
            except KeyError:
                injournal = 'No data'
        else:
            return pd.DataFrame(), (time.time() - start_time)
        flDict.update({'rows': 100000})
        searchStr = f'reference.DOI: "{doi}"'
        tmpSearch = self.solr.search(searchStr, **flDict)
        tmpResIN = [x for x in tmpSearch]
        tmpRes = []
        if tempResIN:
            for elem in tmpResIN:
                tmpRes.append(self.getNodeData(elem, direction='source'))
        else:
            return pd.DataFrame(), (time.time() - start_time)
        dfOut = pd.DataFrame(tmpRes)
        dfOut.insert(0, 'targetJournal', injournal)
        dfOut.insert(0, 'targetDOI', doi)
        dfOut.insert(0, 'targetYear', inyear)
        dfOut.insert(0, 'type', 'citation')
        return dfOut, (time.time() - start_time)

    def getReferenceDF(self, doi, debug=False):
        flDict = {
            'rows': 1,
            'fl': 'DOI, reference-count, is-referenced-by-count, author.family,\
            title, published-print.date-parts, issued.date-parts,\
            published-online.date-parts, container-title, reference.DOI,\
            reference.unstructured'
            }
        start_time = time.time()
        search = self.solr.search(f'DOI:"{doi}"', **flDict)
        result = [x for x in search]
        if result:
            data = result[0]
            inyear = self.getPubDate(data)
            try:
                injournal = data['container-title'][0]
            except KeyError:
                injournal = 'No data'
        else:
            return pd.DataFrame(), (time.time() - start_time)
        flDict.update({'rows': 100000})
        try:
            searchStr = ' OR '.join(
                [f'DOI: "{doi}"' for doi in data['reference.DOI']]
                )
        except KeyError:
            return pd.DataFrame(), (time.time() - start_time)
        tmpSearch = self.solr.search(searchStr, **flDict)
        tmpResIN = [x for x in tmpSearch]
        tmpRes = []
        for elem in tmpResIN:
            tmpRes.append(self.getNodeData(elem, direction='target'))
        ref_count = int(data['reference-count'][0])
        doi_count = len(data['reference.DOI'])
        if ref_count == doi_count:
            dfOut = pd.DataFrame(tmpRes)
        else:
            try:
                inputList = data['reference.unstructured']
                outputDict = {x: '' for x in inputList}
                for elem in tmpRes:
                    famName = elem['targetFirstAuthor']
                    boolList = list(famName in elem for elem in inputList)
                    try:
                        unstrIndex = inputList[boolList.index(True)]
                        outputDict.update({unstrIndex: elem})
                    except ValueError:
                        pass
                if debug:
                    print(outputDict)
                dfOut = pd.DataFrame([outputDict]).transpose()
                dfOut = dfOut.reset_index().rename(
                    columns={'index': 'targetFull'}
                    )
                if 'targetYear' in dfOut.columns:
                    dfOut.insert(
                        0,
                        'altTargetYear',
                        dfOut.targetFull.apply(lambda row: self.findYear(row))
                        )
                    dfOut.targetYear.replace(
                        r'^\s*$', np.nan, regex=True, inplace=True
                        )
                    dfOut.targetYear.fillna(
                        value=dfOut.altTargetYear, inplace=True
                        )
                    dfOut = dfOut.drop('altTargetYear', axis=1)
                else:
                    dfOut.insert(
                        0,
                        'targetYear',
                        dfOut.targetFull.apply(lambda row: self.findYear(row))
                        )
            except KeyError:
                print('Could not find data for {0} references.'.format(
                     ref_count - doi_count)
                     )
                dfOut = pd.DataFrame(tmpRes)
        dfOut.insert(0, 'sourceJournal', injournal)
        dfOut.insert(0, 'sourceDOI', doi)
        dfOut.insert(0, 'sourceYear', inyear)
        dfOut.insert(0, 'type', 'reference')
        return dfOut, (time.time() - start_time)

    def createJSON(self, outputPath='../data/Crossref/'):
        """Write JSON to disc in network format, i.e. nodes and edges list."""
        if isinstance(self.resultDF, str):
            self.run(self.startDoi, self.direct, self.level)

        citNodes = self.resultDF[
            self.resultDF.type == 'citation'][
                ['sourceDOI', 'sourcetitleStr', 'sourceis_ref_byCount', 'sourceYear']
            ].rename(columns={
                'sourceYear': 'nodeYear', 'sourceDOI': 'nodeDOI',
                'sourceis_ref_byCount': 'is_ref_byCount',
                'sourcetitleStr': 'titleStr'
                })
        refNodes = self.resultDF[
            self.resultDF.type == 'reference'][
                ['targetDOI', 'targettitleStr', 'targetis_ref_byCount', 'targetYear']
            ].rename(columns={
                'targetYear': 'nodeYear', 'targetDOI': 'nodeDOI',
                'targetis_ref_byCount': 'is_ref_byCount',
                'targettitleStr': 'titleStr'
                })

        allNodes = list(pd.concat([citNodes, refNodes]).values)
        allRows = [x for x in self.resultDF.iterrows()]

        with open(
                outputPath +
                f'CitationNet_{re.sub("/","slash",urllib.parse.quote(self.startDoi))}.json',
                'w'
                ) as outFile:

            # write nodes
            outFile.write('{\n  "nodes": [\n')

            # write input node
            outFile.write(
                json.dumps(
                    self._nodeDict(
                            self.mainNode[0],
                            self.mainNode[1],
                            self.mainNode[2],
                            self.mainNode[3]
                        )
                    ) + ',\n'
                )

            # write nodes from resultDF/allNodes
            while allNodes:
                node = allNodes.pop()
                if len(allNodes) == 0:
                    outFile.write(
                        json.dumps(
                            self._nodeDict(
                                node[0], node[1], node[2], node[3])
                                ) + '\n'
                        )
                else:
                    outFile.write(
                        json.dumps(
                            self._nodeDict(
                                node[0], node[1], node[2], node[3])
                                ) + ',\n'
                        )

            # write Edges
            outFile.write('  ],\n  "edges":[')
            while allRows:
                idx, edge = allRows.pop()
                if len(allRows) == 0:
                    outFile.write(
                        json.dumps(
                            self._edgeDict(
                                str(idx),
                                edge['sourceDOI'],
                                edge['targetDOI'],
                                edge['sourceYear'],
                                edge['type'])
                            ) + '\n'
                        )
                else:
                    outFile.write(
                        json.dumps(
                            self._edgeDict(
                                str(idx),
                                edge['sourceDOI'],
                                edge['targetDOI'],
                                edge['sourceYear'],
                                edge['type'])
                            ) + ',\n')
            outFile.write('  ]\n}')
        return f'Done writing {outputPath}' + \
            f'CitationNet_{re.sub("/","slash",urllib.parse.quote(self.startDoi))}.json'

    def run(self, doi, direct, level=2, debug=False):
        """Run routine for citing or referenced papers."""
        self.startDoi = doi
        retVal = self.getMainNode(doi)
        if retVal == 'No data':
            return 'DOI not found in dataset.'
        runtimeTotal = []
        if direct == 'cite':
            if debug:
                print('Looking for first level citations.')
            dfRes, runtime = self.getCitationsDF(doi)
            runtimeTotal.append(runtime)
            if level == 2 & len(dfRes) >= 0:
                if debug:
                    print(f'Got {dfRes.shape[0]} citations, looking for second level.')
                if 'sourceDOI' in dfRes.columns:
                    newDFs = [dfRes]
                    for elem in dfRes.sourceDOI.values:
                        dfResTemp, runtime = self.getCitationsDF(elem)
                        runtimeTotal.append(runtime)
                        newDFs.append(dfResTemp)
                    dfRes = pd.concat(newDFs, ignore_index=True)
                if debug:
                    print(f'Cite: Runtime {sum(runtimeTotal)} sec.')
        elif direct == 'ref':
            if debug:
                print('Looking for first level references.')
            dfRes, runtime = self.getReferenceDF(doi)
            runtimeTotal.append(runtime)
            if level == 2 & len(dfRes) >= 0:
                if debug:
                    print(f'Got {dfRes.shape[0]} references, looking for second level.')
                if 'targetDOI' in dfRes.columns:
                    newDFs = [dfRes]
                    for elem in dfRes.targetDOI.values:
                        dfResTemp, runtime = self.getReferenceDF(elem)
                        runtimeTotal.append(runtime)
                        newDFs.append(dfResTemp)
                    dfRes = pd.concat(newDFs, ignore_index=True)
                    dfRes.targetDOI.replace(
                        r'^\s*$', np.nan, regex=True, inplace=True
                        )
                    dfRes.targetDOI.fillna(
                        value=dfRes.targetFull, inplace=True
                        )
                else:
                    dfRes.insert(0, 'targetDOI', dfRes.targetFull)
                if debug:
                    print(f'Ref: Runtime {sum(runtimeTotal)} sec.')
        elif direct == 'both':
            if debug:
                start_time = time.time()
                print(f'Looking for references and citations in {level} level(s).')
            dfCite = self.run(doi, direct='cite', level=level, debug=debug)
            dfRef = self.run(doi, direct='ref', level=level, debug=debug)
            newDFs = [dfCite, dfRef]
            dfRes = pd.concat(newDFs, ignore_index=True)
            if debug:
                print(f'Total runtime {(time.time() - start_time)}')
                missingYears = dfRef[(dfRef.sourceYear == '') | (dfRef.targetYear == '')].shape[0]
                print(f'Found no year for {missingYears} entries, changed to main DOI year.')
            dfRes.targetYear.replace(
                r'^\s*$', self.mainNode[3], regex=True, inplace=True
                )
            dfRes.sourceYear.replace(
                r'^\s*$', self.mainNode[3], regex=True, inplace=True
                )
        self.resultDF = dfRes
        return dfRes
