import torch
print("CUDA available:", torch.cuda.is_available())
print("GPU count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))


import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.version())

