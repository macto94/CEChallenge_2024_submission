# Samsung CE Challenge 2024 submission

## 1. Pull Docker Image
```bash
docker pull macto94/ce_challenge_2024:latest

```
 - Replace `"your-image-name"` with the desired name for your Docker image.

---

## 2. Run the Docker Container and Prepare Model Checkpoint

### With Mounting Local Model Checkpoint

If you have the model checkpoint prepared locally, use the `-v` option to mount the directory:

```bash
docker run --privileged -it --memory=32g --memory-swap=34g -v ”local/path/to/model”:/workspace/checkpoint macto94/ce_challenge_2024:latest
```
- Replace `"/local/path/to/checkpoints"` with the path to your local model checkpoint directory.
- This command mounts your local checkpoints to the container's `"/workspace/checkpoint"` directory.
- It should be checked if swap memory is avaiable on your system.

---

## 3. Execute the Script

Inside the running container, execute the following command to run the script. Before running the script, make sure that you are in `'/workspace/script'` and the `MODEL_ID` is appropriate if mounted.
```bash
bash run.sh
```
**Note:** If you wand to use other test dataset, prepare it and specify the path in `--data` in `run.sh`. Please note that if the data format is not JSON, you may need to modify `load_dataset` accordingly. And please ensure that all necessary files and dependencies are in place before executing the script.

