import pathlib
import re

from clldutils.misc import slug
from pylexibank import FormSpec, Dataset as BaseDataset


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "lamanisoic"
    form_spec = FormSpec(
        missing_data=["---", "-----"],
        separators=",，/~;",
        first_form_only=True,
        # This replacement is needed as the normalization seems to fail
        replacements=[("\u04d5", "\u00e6"), (" ", "_")],  # `ӕ` to `æ`
    )

    def cmd_makecldf(self, args):
        # Read raw data; each element of the list is a language, with
        # concepts as keys (with the exception of `Language`, of course)
        raw_data = self.raw_dir.read_csv("lamayi-table.csv", dicts=True)

        # Write source
        args.writer.add_sources()

        # Write languages
        language_map = args.writer.add_languages(lookup_factory="Name")

        # Write concepts; the English part of the gloss is later obtained by
        # splitting at the last space, before the Chinese gloss
        concept_map = args.writer.add_concepts(
            id_factory=lambda x: x.id.split("-")[-1] + "_" + slug(x.english),
            lookup_factory="Name",
        )

        # Write lexemes
        for row in raw_data:
            language = row.pop("Language")
            for concept, value in row.items():
                # Obtain concept key and add entry
                match = re.match(r"\d\d\d (.+) \S+", concept)
                args.writer.add_lexemes(
                    Language_ID=language_map[language],
                    Parameter_ID=concept_map[match.group(1).strip()],
                    Value=value,
                    Source=["Lama:2012"],
                )
