import torch

from transformers import BitsAndBytesConfig
from guidance import models


def load_model_llamacpp(file_path, **model_kwargs):
    # chat_template=llama3
    # chat_template=gemma
    # chat_template=mistral_7b_instruct_template
    return models.LlamaCpp(file_path, **model_kwargs)


def load_model_hf(model_name, **model_kwargs):
    # quantization_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_compute_dtype=torch.float16,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_use_double_quant=True,
    # )
    return models.Transformers(model_name, echo=False, 
                               torch_dtype=torch.bfloat16,
                            #    load_in_8bit=True, 
                               **model_kwargs)