from huggingface_hub import snapshot_download
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--model_local_dir', 
    type=str,
    default='/workspace/checkpoint'
    )
parser.add_argument(
    '--repo_id',
    type=str,
    default='microsoft/Phi-3-medium-4k-instruct')
args = parser.parse_args()

if __name__ == "__main__":
    snapshot_download(repo_id=args.repo_id,
                      repo_type="model",
                      local_dir=args.model_local_dir,
                      local_dir_use_symlinks=False,
                      ignore_patterns=["*.msgpack", "*.h5"]
                     )
