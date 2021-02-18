from tqdm import tqdm
from vocabs.models import (
    SkosConceptScheme, SkosCollection, SkosConcept, ConceptNote
)

from . config import GN_FTC_SCHEME, GN_FTC_COLLECTION


scheme, _ = SkosConceptScheme.objects.get_or_create(
    **GN_FTC_SCHEME
)

GN_FTC_COLLECTION['scheme'] = scheme
col, _ = SkosCollection.objects.get_or_create(**GN_FTC_COLLECTION)


def import_feature_codes(df):
    failed = []
    for group in df.groupby('group'):
        cur_df = group[1]
        top_concept, _ = SkosConcept.objects.get_or_create(
            pref_label=f"{group[0]}",
            scheme=scheme,
            top_concept=True
        )
        top_concept.collection.add(col)
        for i, row in tqdm(cur_df.iterrows(), total=len(cur_df)):
            item, _ = SkosConcept.objects.get_or_create(
                notation=f"{row['code']}",
                pref_label=f"{row['pref_label']}",
                scheme=scheme,
                top_concept=False
            )
            item.collection.add(col)
            item.broader_concept = top_concept
            try:
                item.save()
            except Exception as e:
                item.broader_concept = None
                item.save()
                failed.append([item, top_concept, e])
            notation, _ = ConceptNote.objects.get_or_create(
                concept=item,
                name=row['description'],
                note_type='definition',
                language="eng"
            )
    for x in failed:
        x[0].broader_concept = x[1]
        x[0].save()
    return scheme
