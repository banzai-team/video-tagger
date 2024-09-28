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
    
def load_model_openrounter(model_name, tokenizer="neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8", **model_kwargs):
    """speedup eval"""
    # quantization_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_compute_dtype=torch.float16,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_use_double_quant=True,
    # )
    import os
    from transformers import AutoTokenizer
    
    from guidance.models.transformers._transformers import TransformersTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
                                   tokenizer, 
                                   use_fast=False, legacy=True
                                )
    tt = TransformersTokenizer(model_name, tokenizer, chat_template='llama3', ignore_bos_token=True)
    return models.OpenAI(model_name, echo=False, 
                               api_key=os.environ['OPENROUTER_API_KEY'],
                               base_url='https://openrouter.ai/api/v1/',
                               tokenizer = tt,
                               **model_kwargs)