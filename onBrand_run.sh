#!/bin/bash

# Define the list of YAML configuration files
config_files=(
    "lm_eval/tasks/medmcqa/medmcqa.yaml"
    "lm_eval/tasks/medqa/medqa.yaml"
    "lm_eval/tasks/mmlu/default/_default_template_yaml"
    "lm_eval/tasks/pubmedqa/pubmedqa.yaml"
    "lm_eval/tasks/usmle_sa_step1/usmle_sa_step1.yaml"
    "lm_eval/tasks/usmle_sa_step2/usmle_sa_step2.yaml"
    "lm_eval/tasks/usmle_sa_step3/usmle_sa_step3.yaml"
)

# List of keyword_replace settings to apply
keyword_replacements=("none" "brand_to_generic" "generic_to_brand")

# Backup original configuration files to restore later
for file in "${config_files[@]}"; do
    cp $file "${file}.bak"
done

# Function to update the keyword_replace in the YAML files
update_config() {
    # Use sed to replace the keyword_replace line
    for file in "${config_files[@]}"; do
        sed -i "s/keyword_replace: .*/keyword_replace: $1/" $file
    done
}

# Loop over each keyword_replace setting
for replace in "${keyword_replacements[@]}"; do
    echo "Setting keyword_replace to $replace"
    update_config $replace

    # Run the evaluation command for the onBrand group task
    echo "Running evaluation for keyword_replace: $replace"
    python lm_eval --model hf \
                   --model_args pretrained=EleutherAI/pythia-160m,revision=step100000,dtype="float" \
                   --tasks onBrand \
                   --device cuda:0 \
                   --batch_size auto:64 \
                   --output_path lm_eval/tasks/benchmarks/onBrand/results/ \
                   --keyword_replace $replace
done

# Restore the original configuration files
for file in "${config_files[@]}"; do
    mv "${file}.bak" $file
done

echo "All evaluations completed."



