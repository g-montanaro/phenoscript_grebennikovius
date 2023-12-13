# Define variables
PHS_FILE = grebennikovius_descriptions.phs
OUT_FILE_OWL = grebennikovius
CONFIG_FILE = phenotypes/phs-config.yaml

# Default target
all: phs2-owl-NL validate-phs make-tbox reason-owl


# Convert phs To OWL & NL 
phs2-owl-NL:
	@echo "\nSTEP: phs TO OWL";
	cd phenotypes && phenospy phs2owl $(PHS_FILE) ../output/$(OUT_FILE_OWL)
	cd ..;
	@echo "\nSTEP: phs TO NL";
	phenospy owl2text -f 'html' -s 'org_*' -o output/$(OUT_FILE_OWL).owl -d output/NL
	phenospy owl2text -f 'md' -s 'org_*' -o output/$(OUT_FILE_OWL).owl -d output/NL

# Validate phs using SHACL
validate-phs:
	@echo "\nSTEP: Validate using SHACL";
	shacl validate --data output/$(OUT_FILE_OWL).owl --shapes source_queries/phenoscript.shacl.ttl > output/shacl.log


# Make Tbox ontology file: 
# donwload source ontologies, merge them, remove individuals
# also adds source_queries/query.rdf that contains precooked classes for queries
make-tbox:
	@echo "\nSTEP: make Tbox file";
	@if [ ! -d "source_ontologies" ] || [ -z "$$(ls source_ontologies 2>/dev/null)" ]; then \
		echo "Current directory: $$(pwd)"; \
		echo "Downloading source_ontologies ..."; \
		phenospy fetch-ontos $(CONFIG_FILE) source_ontologies; \
		echo "robot merge ontologies ..."; \
		robot merge --inputs "source_ontologies/*.owl" --input source_queries/query.rdf --output merged_ontologies/tbox.owl; \
		echo "robot remove individuals ..."; \
		robot remove --input merged_ontologies/tbox.owl --select individuals --output merged_ontologies/tbox.owl; \
	else \
		echo "source_ontologies is not empty. Skipping update."; \
	fi

# resaon Abox using Tbox file with materializer
# annotate inffered axioms
# merge all ontologies into a single file
reason-owl:
	@echo "\nSTEP: reason using materializer";
	materializer file --ontology-file merged_ontologies/tbox.owl --input output/$(OUT_FILE_OWL).owl --output output/$(OUT_FILE_OWL)-reasoned.ttl --reasoner whelk
	@echo "\nSTEP: annotate inffered axioms";
	update --data output/$(OUT_FILE_OWL)-reasoned.ttl --update source_queries/annotate.ru --dump > output/$(OUT_FILE_OWL)-reasoned-annotated.ttl
	@echo "\nSTEP: merge all ontologies into a single file";
	riot output/$(OUT_FILE_OWL).owl output/$(OUT_FILE_OWL)-reasoned-annotated.ttl merged_ontologies/tbox.owl > output/$(OUT_FILE_OWL)-all.ttl
	@echo "\nMAKE COMPLETED";