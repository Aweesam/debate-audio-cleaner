import torch, torchaudio

print(torch.__version__, torch.version.cuda)
print("CUDA is_available:", torch.cuda.is_available())