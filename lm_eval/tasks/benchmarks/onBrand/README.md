# On Brand
### Paper

Title: 

Abstract:

A benchmark 

### Citation

```

```

### Tasks

* [PubMedQA](https://pubmedqa.github.io/) - 1,000 expert-labeled Q&A pairs where a question and corresponding PubMed abstract as context is given and the a yes/maybe/no answer must be produced. Unlike the rest of the tasks in this suite, PubMedQA is a closed-domain Q&A task.
* [MedQA](https://github.com/jind11/MedQA) - US Medical License Exam (USMLE) questions with 4 or 5 possible answers. Typically, only the 4-option questions are used.
* [MedMCQA](https://medmcqa.github.io/) - 4-option multiple choice questions from Indian medical entrance examinations, >191k total questions.
* [MMLU](https://arxiv.org/abs/2009.03300) - 4-option multiple choice exam questions from a variety of domains. The following 6 domains are utilized here:
	* Anatomy
	* Clinical Knowledge
	* College Medicine
	* Medical Genetics
	* Professional Medicine
	* College Biology

Note that MultiMedQA also includes some short-form and long-form Q&A tasks (LiveQA, MedicationQA, HealthSearchQA). Evaluation on these tasks is usually done by experts and is not typically performed automatically, and therefore is ignored here.s

## Key word replacement
We downloaded xx drugs from RxNorm. drug_names.csv
Generic to brand is one to many mapping so we use a fixed random seed of 42 to ensure consistency in the replacement.
Brand to generic is many to many to one mapping so there is no need to fix the random seed.

yaml files contain replace_keyword variable. if none then no replacment is done. if brand_to_generic then brand to generic replacement is done. if generic_to_brand then generic to brand replacement is done. 
This is done during the doc_to_text function in the task class. You can find the exact mapping in the preprocessing files unique to each task.

## Todo
- add all drugs to drug_names


#### Future
- Look into LiveQA, MedicationQA, HealthSearchQA
- Do we want to download on_brand as a separate dataset/task or just add options to the existing tasks?
- Sort better task saving for mmlu subtasks replacements- currently using dates to reload replacement tracker 