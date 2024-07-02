# original from https://github.com/oskarvanderwal/grounded-bias-eval/blob/main/bias_benchmarks/custom_tasks/shadr.py
import ast
import numpy as np

def process_results_gen(doc, results):

    if doc["cop"] == results[0]:
        acc = 1
    else:
        acc = 0

    return {"acc": acc}