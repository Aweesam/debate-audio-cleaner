from nemo.collections.asr.parts.models.hifigan_denoise import HifiGANUniversalDenoiserModel

import torch, soundfile as sf, torchaudio, os

wav_path = os.path.join('output', '0_01_1.wav')
wave, sr = torchaudio.load(wav_path)
model = HifiGANUniversalDenoiserModel.from_pretrained(model_name="denoiser_thor")
clean = model(wave.to(model.device))
sf.write('output/clean_nemo.wav', clean.cpu().squeeze().numpy(), sr)
print("✓ wrote output/clean_nemo.wav")