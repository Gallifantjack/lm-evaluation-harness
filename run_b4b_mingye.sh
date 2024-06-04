#!/bin/bash

# Ensure the Hugging Face token is set as an environment variable
if [ -z "$HF_TOKEN" ]; then
    echo "Hugging Face token not found. Please set the HF_TOKEN environment variable by running 'export HF_TOKEN=your_token_here'."
    exit 1
fi

# Login to Hugging Face
echo $HF_TOKEN | huggingface-cli login --token
echo $TRANSFORMERS_CACHE 

# Define the base directory (use an absolute path if possible)
# base_dir="/home/legionjgally/Desktop/mit/lm-evaluation-harness"
base_dir="/clinical_nlp/lm-evaluation-harness"
python_env="/home/inbar214/anaconda3/envs/b4b/bin/python"

# List of models to evaluate
models=(
    # "meta-llama/Llama-2-7b-hf"
    # "meta-llama/Meta-Llama-3-8B"
    # "mistralai/Mixtral-8x7B-v0.1"
    # "mistralai/Mixtral-8x22B-v0.1"
    # "meta-llama/Llama-2-70B-hf"
    # "meta-llama/Meta-Llama-3-70B"
    "Qwen/Qwen1.5-72B"
    "CohereForAI/c4ai-command-r-plus"
    # "CohereForAI/aya-23-35B"
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
                    --batch_size 4 \
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
