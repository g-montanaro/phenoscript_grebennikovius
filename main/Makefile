# Define variables
PHS_FILE = grebennikovius_descriptions.phs
OUT_DIR_OWL = output
OUT_FILE_OWL = grebennikovius
PHENOSPY = phenospy
CONFIG_FILE = phenotypes/phs-config.yaml
ONTOS_DIR = source_ontologies

# Default target
all: check-fetch-merge-ontos phs2owl merge-reason-phs


# Target to check if source_ontologies directory is empty or noexistent  and then fetch ontologies from yaml
check-fetch-merge-ontos:
	@echo "STEP: check-fetch-merge-ontos";
	@if [ ! -d "$(ONTOS_DIR)" ] || [ -z "$$(ls $(ONTOS_DIR) 2>/dev/null)" ]; then \
		echo "Current directory: $$(pwd)"; \
		echo "Updating $(ONTOS_DIR) ..."; \
		$(PHENOSPY) fetch-ontos $(CONFIG_FILE) $(ONTOS_DIR); \
		echo "robot merge ..."; \
		robot merge --inputs "source_ontologies/*.owl" --output merged_ontologies/merged.owl; \
		echo "robot remove individuals ..."; \
		robot remove --input merged_ontologies/merged.owl --select individuals --output merged_ontologies/merged_clean.owl; \
		echo "robot reasoner ELK ..."; \
		if robot reason --reasoner ELK --input merged_ontologies/merged_clean.owl > merged_ontologies/ELK_merged_clean.owl.log; then \
			echo "ELK reasoning completed successfully."; \
		else \
			echo "ELK reasoning failed or produced errors. Check ELK_merged_clean.log for details."; \
		fi \
	else \
		echo "$(ONTOS_DIR) is not empty. Skipping update."; \
	fi


# Target to run the phs2owl command
phs2owl:
	@echo "STEP: phs2owl";
	cd phenotypes && $(PHENOSPY) phs2owl $(PHS_FILE) ../$(OUT_DIR_OWL)/$(OUT_FILE_OWL)
	cd ..;

merge-reason-phs:
	@echo "STEP: merge-reason-phs";
	robot merge --input merged_ontologies/merged_clean.owl --input $(OUT_DIR_OWL)/$(OUT_FILE_OWL).owl  --output $(OUT_DIR_OWL)/$(OUT_FILE_OWL)_merged.owl
	@echo "robot reason --reasoner WHELK ...";
	@if robot reason --reasoner whelk --input $(OUT_DIR_OWL)/$(OUT_FILE_OWL)_merged.owl > $(OUT_DIR_OWL)/WHELK_$(OUT_FILE_OWL)_merged.owl.log; then \
			echo "WHELK reasoning completed successfully."; \
	else \
			echo "WHELK reasoning failed or produced errors. Check log for details."; \
	fi
	@echo "robot reason --reasoner ELK ...";
	@if robot reason --reasoner ELK --input $(OUT_DIR_OWL)/$(OUT_FILE_OWL)_merged.owl > $(OUT_DIR_OWL)/ELK_$(OUT_FILE_OWL)_merged.owl.log; then \
			echo "ELK reasoning completed successfully."; \
	else \
			echo "ELK reasoning failed or produced errors. Check log for details."; \
	fi
	@echo "MAKE COMPLETED";