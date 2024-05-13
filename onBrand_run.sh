#!/bin/bash

# Define the base directory (use an absolute path if possible)
base_dir="/home/jgally/mit/lm-evaluation-harness/lm_eval/tasks"

# Ensure permissions for writing and creating directories recursively
chmod -R u+rwx "$base_dir"
chown -R $(whoami) "$base_dir"

# Optionally set the setgid bit to keep group ownership on new files and subdirectories
chmod g+s "$base_dir"

# Define the list of YAML configuration files
config_files=(
    "$base_dir/medmcqa/medmcqa.yaml"
    "$base_dir/medqa/medqa.yaml"
    "$base_dir/mmlu/default/_default_template_yaml"
    "$base_dir/pubmedqa/pubmedqa.yaml"
    "$base_dir/usmle_sa_step1/usmle_sa_step1.yaml"
    "$base_dir/usmle_sa_step2/usmle_sa_step2.yaml"
    "$base_dir/usmle_sa_step3/usmle_sa_step3.yaml"
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

        # Define output path to include model alias and ensure it exists with correct permissions
        output_path="$base_dir/benchmarks/onBrand/results/$model_alias/$replace"
        mkdir -p $output_path
        chmod -R u+rwx $output_path
        chown -R $(whoami) $output_path

        # Run the evaluation command for the onBrand group task
        echo "Running evaluation for model $model with keyword_replace: $replace"
        /home/jgally/miniconda3/envs/nlp_cuda118/bin/python3 lm_eval --model hf \
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
