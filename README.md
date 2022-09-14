# Wiretap

Detect and record voice automatically for supervisor.

## Installation

```bash
# install portaudio
sudo apt-get install libasound-dev
git clone git@github.com:PortAudio/portaudio
cd portaudio
./configure && make
sudo make install
# install pyaudio
pip3 install pyaudio
# clone wiretap
git clone git@github.com:qian-gu/wiretap
```

## Usage

```bash
cd wiretap
python ./src/wiretap.py
```
