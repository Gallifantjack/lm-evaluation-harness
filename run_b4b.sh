#!/bin/bash

# Define the base directory (use an absolute path if possible)
base_dir="/home/legionjgally/Desktop/mit/lm-evaluation-harness"

# List of models to evaluate
models=(
    "microsoft/phi-microsoft/phi-1_5"
    "microsoft/phi-2"
    "microsoft/Phi-3-mini-4k-instruct"
    # "meta-llama/Llama-2-7b-hf"
    # "meta-llama/Meta-Llama-3-8B"
    "mistralai/Mistral-7B-v0.1"
    "Qwen/Qwen1.5-7B"
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
    /home/legionjgally/miniconda3/envs/bnb_39_117/bin/python3 lm_eval --model hf \
                    --model_args pretrained=$model \
                    --tasks b4b \
                    --device cuda:0 \
                    --batch_size auto:64 \
                    --output_path $results_file
done

echo "All evaluations completed."


# List for future ref
# viii.    mistralai/Mistral-7B-vO.1
# ix. mistralai/Mixtral-8x22B-v0.1
# x. Llama-2-7B-hf
# xi. Llama-2-70B-hf
# xii. Llama-3-8B-hf
# xiii. Llama-3-70B-hf
# xiv. Qwen1.5-7b
# xv. Qwen/Qwen1.5-72B
# xvi. Qwen1.5-110b
# XVII. GPT-40
# xviii. GPT4-turbo
# xix. Claude-3.0-haiku
# xx. Claude-3.0-opus
# xxi. Claude-3.0-sonnet
