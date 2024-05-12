#!/bin/bash

# Define the list of YAML configuration files
config_files=(
    "lm_eval/tasks/medmcqa/medmcqa.yaml"
    "lm_eval/tasks/medqa/medqa.yaml"
    "lm_eval/tasks/mmlu/default/_default_template.yaml"
    "lm_eval/tasks/pubmedqa/pubmedqa.yaml"
    "lm_eval/tasks/usmle_sa_step1/usmle_sa_step1.yaml"
    "lm_eval/tasks/usmle_sa_step2/usmle_sa_step2.yaml"
    "lm_eval/tasks/usmle_sa_step3/usmle_sa_step3.yaml"
)

# List of models to evaluate
models=(
    "unsloth/gemma-7b"
    "mistralai/Mistral-7B-v0.1"
    "medalpaca/medalpaca-7b"
    "BioMistral/BioMistral-7B"
    "openai-community/gpt2-xl"
    "EleutherAI/gpt-neo-2.7B"
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

# Loop over each model and keyword_replace setting
for model in "${models[@]}"; do
    model_alias=$(echo $model | tr '/' '-')
    for replace in "${keyword_replacements[@]}"; do
        echo "Setting keyword_replace to $replace for model $model"
        update_config $replace

        # Define output path to include model alias
        output_path="lm_eval/tasks/benchmarks/onBrand/results/$model_alias/$replace"

        # Create output directory if it does not exist
        mkdir -p $output_path

        # Run the evaluation command for the onBrand group task
        echo "Running evaluation for model $model with keyword_replace: $replace"
        python lm_eval --model hf \
                       --model_args pretrained=$model \
                       --tasks onBrand \
                       --device cuda:0 \
                       --batch_size auto:64 \
                       --output_path $output_path \
                       --keyword_replace $replace
    done
done

# Restore the original configuration files
for file in "${config_files[@]}"; do
    mv "${file}.bak" $file
done

echo "All evaluations completed."
