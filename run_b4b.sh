#!/bin/bash

# Ensure the Hugging Face token is set as an environment variable
if [ -z "$HF_TOKEN" ]; then
    echo "Hugging Face token not found. Please set the HF_TOKEN environment variable by running 'export HF_TOKEN=your_token_here'."
    exit 1
fi

# Login to Hugging Face
echo $HF_TOKEN | huggingface-cli login --token

# Define the base directory (use an absolute path if possible)
# base_dir="/home/legionjgally/Desktop/mit/lm-evaluation-harness"
base_dir="/home/jgally/mit/lm-evaluation-harness"
python_env="/home/jgally/miniconda3/envs/b4b/bin/python"

# List of models to evaluate
models=(
    "microsoft/phi-1"
    "microsoft/phi-1_5"
    "microsoft/phi-2"
    "microsoft/Phi-3-medium-4k-instruct"
    "mistralai/Mistral-7B-v0.3"
    "Qwen/Qwen2-7B"
)

# Loop over each model
for model in "${models[@]}"; do
    # Create a model alias by replacing '/' with '-'
    model_alias=$(echo $model | tr '/' '-')

    # Define output path to include model alias and ensure it exists with correct permissions
    output_path="$base_dir/results/b4b"
    mkdir -p $output_path
    chmod -R u+rwx $output_path

    # Define the results file name
    results_file="$output_path/${model_alias}_results.json"

    # Run the evaluation command for the onBrand group task
    echo "Running evaluation for model $model"
    $python_env lm_eval --model hf \
                    --model_args pretrained=$model,load_in_4bit=True \
                    --tasks b4b \
                    --device cuda:0 \
                    --batch_size auto:64 \
                    --output_path $results_file
done

echo "All evaluations completed."
