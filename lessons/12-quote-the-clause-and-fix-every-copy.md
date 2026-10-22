# Lesson 12: quote the clause, and fix every copy of a corrected sentence

Area: materials notes and knowledge hygiene

| What happened | Root cause | Rule now |
|---|---|---|
| A filed materials note said glue on PETG is used only to reduce adhesion. The sentence had been copied into a buying list and a design document. A later fact-check found the opposite: the Bambu wiki says glue improves adhesion, eases removal and protects the plate, and Bambu PETG data sheets list glue as recommended. An earlier review had said "no value in this note was contradicted", while checking only some rows. | The linked source was never quoted for that clause; a plausible inference was filed as a sourced fact. A partial re-check was reported as if it covered the whole note. Copies in other files had no pointer back to the note. | A fact with a source link must be something the linked page actually states: quote the clause or do not file it. A re-check that covers only some rows names those rows. When a note is corrected, search the whole knowledge base and project folders for the old sentence and fix or flag every copy. |
| A drying table summarised two cells of a wiki row as "not compatible" for two different dryer devices; the row actually gave a value for one of them. | Cells were read as columns without matching each cell to its header. The note's own preset values contradicted the summary and nobody compared them. | A table in a note quotes each device column separately, one value per column. When a note gives both a wiki table and preset values for the same thing, compare them before filing; a mismatch is a finding. |

How to check: for each fact you file, open the link and find the sentence that states it; after a correction, search for a distinctive phrase of the old sentence across the repository.

Sources: https://wiki.bambulab.com/en/filament-acc/filament/dry-filament and the Bambu wiki plate-adhesion / glue pages (https://wiki.bambulab.com/).
