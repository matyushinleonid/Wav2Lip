FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-runtime

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /workspace/Wav2Lip
