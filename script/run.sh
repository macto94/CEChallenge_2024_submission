#!/bin/bash
# Team AIHA-HYU


#MODEL_ID=/media/aiha/ssd/phi3_checkpoint
MODEL_ID=/workspace/checkpoint
# DATA_DIR= put your dataset directory (e.g., /workspace/shlee/test_datset.jsonl)

for batch in 8
do
    sync && sysctl -w vm.drop_caches=3
    sleep 3
    python3 sihwa_test.py --model_id $MODEL_ID --warm_up -b $batch
#    python3 sihwa_test.py --model_id $MODEL_ID --data_dir $DATA_DIR --warm_up -b $batch
done

sync && sysctl -w vm.drop_caches=3
