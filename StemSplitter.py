import torch
import onnxruntime as ort
import os
from audio_separator.separator import Separator
from requests.exceptions import Timeout

# Check if ONNX Runtime is installed and install if necessary
try:
    import onnxruntime as ort
except ImportError:
    os.system("pip install onnxruntime-gpu")

def check_onnxruntime_gpu():
    providers = ort.get_available_providers()
    if 'CUDAExecutionProvider' in providers:
        print("ONNX Runtime GPU is available.")
    else:
        print("ONNX Runtime GPU is not available, using CPU.")

check_onnxruntime_gpu()

if not torch.cuda.is_available():
    print("No GPU detected. Running in CPU mode.")
else:
    print("GPU detected. Running in GPU mode.")

separator = Separator()
model_to_load = 'UVR-MDX-NET_Main_406.onnx'
separator.load_model(model_filename=model_to_load)

vocals_dir = "vocals"
instrumentals_dir = "instrumentals"
audio_files_dir = "new_rapper_songs"

os.makedirs(vocals_dir, exist_ok=True)
os.makedirs(instrumentals_dir, exist_ok=True)

for file_name in os.listdir(audio_files_dir):
    file_path = os.path.join(audio_files_dir, file_name)
    
    if file_path.lower().endswith(('.wav', '.mp3', '.flac')):
        print(f"Processing {file_name}...")
        
        rapper_id = file_name.split('_')[0]  # Assumes file names are in the format "rapperX_songY..."
        rapper_vocals_folder = os.path.join(vocals_dir, rapper_id)
        os.makedirs(rapper_vocals_folder, exist_ok=True)
        
        vocals_path = os.path.join(rapper_vocals_folder, file_name)  # Correctly places the file within the rapper's folder
        instrumentals_path = os.path.join(instrumentals_dir, f"{rapper_id}_instrumental.wav")
        
        if os.path.exists(vocals_path) and os.path.exists(instrumentals_path):
            print(f"Files for {file_name} already exist. Skipping...")
            continue
        
        try:
            output_file_paths = separator.separate(file_path)
            print(f"Output file paths: {output_file_paths}")
            
            os.rename(output_file_paths[1], vocals_path)
            os.rename(output_file_paths[0], instrumentals_path)
            print(f"Saved vocals to {vocals_path}")
            print(f"Saved instrumentals to {instrumentals_path}")
        except Timeout:
            print(f"Request timed out for {file_name}. Skipping...")
        except Exception as e:
            print(f"An error occurred while processing {file_name}: {e}")

print("Processing complete.")

# Additional functionality for handling double .wav extensions
audio_files_dir = "dataset_for_mfa/rapper_songs"

for root, dirs, files in os.walk(audio_files_dir):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        
        if file_name.lower().endswith('.wav.wav'):
            print(f"Processing {file_name}...")
            
            try:
                output_file_paths = separator.separate(file_path)
                print(f"Output file paths: {output_file_paths}")
                
                os.replace(output_file_paths[1], file_path)
                print(f"Replaced original file with vocal stem: {file_path}")
            except Timeout:
                print(f"Request timed out for {file_name}. Skipping...")
            except Exception as e:
                print(f"An error occurred while processing {file_name}: {e}")

print("Processing complete.")