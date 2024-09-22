# Samsung CE Challenge 2024 submission

## 1. Build the Docker Image

Clone this repository and build the Docker image with the following command:
```bash
git clone https://github.com/macto94/CEChallenge_2024_submission.git
cd CEChallenge_2024_submission
docker build -t your-image-name .
```
 - Replace `"your-image-name"` with the desired name for your Docker image.

---

## 2. Run the Docker Container and Prepare Model Checkpoint

### Case 1. With Mounting Local Model Checkpoint

If you have the model checkpoint prepared locally, use the `-v` option to mount the directory:

```bash
docker run --privileged -it -v /local/path/to/checkpoints:/workspace/checkpoint your-image-name
```

- Replace `"/local/path/to/checkpoints"` with the path to your local model checkpoint directory.
- This command mounts your local checkpoints to the container's `"/workspace/checkpoint"` directory.

Change `modeling_phi3.py` to custom one.
```bash
cp ./shlee_modeling_phi3.py /workspace/checkpoint/modeling_phi3.py
```

### Case 2. Without Mounting Local Model Checkpoint

If you **do not** have a local model checkpoint to mount, run:

```bash
docker run --privileged -it your-image-name
```

Download model and change `modeling_phi3.py` to custom one.
```bash
python3 download_model.py  # This will download phi3-medium-4k to "/workspace/checkpoint/"
cp ./shlee_modeling_phi3.py /workspace/checkpoint/modeling_phi3.py
```

---

## 3. Execute the Script

Inside the running container, execute the following command to run the script. Before running the script, make sure that you are in `'/workspace/script'` and the `MODEL_ID` is appropriate if mounted.
```bash
bash run.sh
```

**Note:** If you wand to use other test dataset, prepare it and specify the path in `DATA_DIR` in `run.sh`, and add the `--data_dir` argument to the python3 command. Please note that if the data format is not JSON, you may need to modify `load_dataset` accordingly. And please ensure that all necessary files and dependencies are in place before executing the script.

