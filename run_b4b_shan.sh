#!/bin/bash

# Ensure the Hugging Face token is set as an environment variable
if [ -z "$HF_TOKEN" ]; then
    echo "Hugging Face token not found. Please set the HF_TOKEN environment variable by running 'export HF_TOKEN=your_token_here'."
    exit 1
fi

# Login to Hugging Face
echo $HF_TOKEN | huggingface-cli login --token

# Define the base directory (use an absolute path if possible)
# base_dir="/home/shan/Desktop/lm-evaluation-harness"
base_dir="/home/ch225816/lm-evaluation-harness"
# python_env="/home/shan/miniconda3/envs/harness/bin/python"
python_env="/home/ch225816/miniconda3/envs/harness/bin/python"

# List of models to evaluate
models=(
   # "aaditya/Llama3-OpenBioLLM-70B"
   # "ProbeMedicalYonseiMAILab/medllama3-v20"
   # "johnsnowlabs/JSL-MedLlama-3-8B-v9"
   # "01-ai/Yi-1.5-34B"
   # "mistralai/Mixtral-8x22B-v0.1"
   # "Qwen/Qwen1.5-110B"
   # "meta-llama/Llama-2-7b-hf"
   # "meta-llama/Meta-Llama-3-8B"
   # "mistralai/Mixtral-8x7B-v0.1"
   #  # "mistralai/Mixtral-8x22B-v0.1"
   # "meta-llama/Llama-2-70B-hf"
   # "meta-llama/Meta-Llama-3-70B"
   # "Qwen/Qwen2-72B"
   # "CohereForAI/c4ai-command-r-plus"
   "CohereForAI/aya-23-35B"
   # "microsoft/phi-1"
   # "microsoft/phi-1_5"
   # "microsoft/phi-2"
   # "microsoft/Phi-3-medium-4k-instruct"
   # "mistralai/Mistral-7B-v0.3"
   # "Qwen/Qwen2-7B"
   )

# Loop over each model
for model in "${models[@]}"; do
    # Create a model alias by replacing '/' with '-'
    model_alias=$(echo $model | tr '/' '-')

    # Define output path to include model alias and ensure it exists with correct permissions
    output_path="$base_dir/results/b4bqa_new"
    mkdir -p $output_path
    chmod -R u+rwx $output_path

    # Define the results file name
    results_file="$output_path/${model_alias}_results.json"

    # Run the evaluation command for the onBrand group task
    echo "Running evaluation for model $model"
    $python_env lm_eval --model hf \
                    --model_args pretrained=$model,parallelize=True,load_in_4bit=True \
                    --tasks b4bqa \
                    --batch_size auto \
                    --output_path $results_file
done

echo "All evaluations completed."

