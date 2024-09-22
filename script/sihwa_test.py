# Copyright 2024. All Rights Reserved.
# Author: Sihwa Lee
#
# Description : Main code for 2024 Samsung CE Challenge 

import time
time_started = time.time()

import os, sys
#from multiprocessing import Process, Queue

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

import argparse
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s] - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger('[SHLEE] 2024 CE Challenge')

def main():

    logger.info(f'Loading Model')
    ######## Section 1. Set up #######
    torch.random.manual_seed(0)
    model_id = args.model_id
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map='auto',
        torch_dtype=torch.bfloat16,
        cache_dir='.',
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

    model.eval()
     
    pipe = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
    )

    generation_args = {
        'max_new_tokens': 20,
        'return_full_text': False,
        'do_sample': False,
        'batch_size': args.batch_size,
    }
    
    ####### Section 2. GPU Warm up #######
    if args.warm_up:
        messages = [
            {'role': 'user', 'content': 'Can you provide ways to eat combinations of bananas and dragonfruits?'},
            {'role': 'assistant', 'content': 'Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey.'},
            {'role': 'user', 'content': 'What about solving an 2x + 3 = 7 equation?'},
        ]
        output = pipe(messages, **generation_args)
        print(output[0]['generated_text'])
     
    torch.cuda.reset_peak_memory_stats()
    ####### Section 3. Load data and Inference -> Performance evaluation part #######
    logger.info(f'Loading Dataset...')
    start = time.time()

    data = load_dataset('json', data_files=args.data_dir)['train']
    logger.info(f'Loading Dataset Time : {time.time() - start:.3f}sec')
    outs = pipe(KeyDataset(data, 'message'), **generation_args)

    end = time.time()
    peak_memory = torch.cuda.max_memory_allocated() / 1024**3

    ####### Section 4. Accuracy (Just for leasderboard) #######
    correct = 0
    for i, out in enumerate(outs):
        correct_answer = data[i]['answer']
        answer = out[0]['generated_text'].lstrip().replace('\n','')
        if answer == correct_answer:
            correct += 1


    print(f'Batch Size: {args.batch_size} Completed')
     
    print('===== Perf result =====')
    print(f'Elapsed_time: {end-start}sec')
    print(f"Peak memory usage: {peak_memory:.2f} GB")
    print(f'Correctness: {correct}/{len(data)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model_id',
        type=str,
        default='/media/aiha/ssd/checkpoint'
    )
    parser.add_argument(
        '--data_dir',
        type=str,
        default='./test_dataset.jsonl'
    )
    parser.add_argument(
        '--profiling',
        action='store_true',
        help='activate profiling mode',
    )
    parser.add_argument(
        '--warm_up',
        action='store_true',
        help='do warm up',
    )
    parser.add_argument(
        '--batch_size',
        '-b',
        type=int,
        default=1,
    )

    args = parser.parse_args()
    main()
