import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from datetime import datetime, timedelta
from time import time, sleep
from pushbullet import Pushbullet
import os


pb_key = None
try:
    with open("pushbullet_key.txt", "r") as file:
        pb_key = file.read().replace("\n", "").strip()
except Exception:
    print("You need a Pushbullet acount")

if pb_key:
    try:
        pb = Pushbullet(pb_key)
    except Exception:
        print("Oh well, Pushbullet is down.")

def get_prompt_and_remove_it_from_the_file():
    with open("prompts.txt", "r") as file:
        lines = file.read().split("\n")
    if len(lines) > 1:
        contents_to_write = "\n".join(lines[1:])
    else:
        contents_to_write = ""
    with open("prompts.txt", "w") as file:
        file.write(contents_to_write)
    if len(lines) > 0:
        prompt = lines[0]
    else:
        prompt = None
    return prompt

def create_current_prompt_file(prompt, path):
    with open(path, "w") as file:
        file.write(prompt)

def remove_current_prompt_file(path):
    if os.path.exists(file):
        os.remove(path)

def get_next_prompt():
    prompt = get_prompt_and_remove_it_from_the_file()
    return prompt

def get_finish_time(seconds):
    now = datetime.now()
    finish_time = now + timedelta(seconds=seconds)
    return finish_time.strftime("%H:%M")

duration_per_s = 105
clip_duration = 15
done_time = get_finish_time(clip_duration*duration_per_s)
print(f"Starting, will be done with first prompt at {done_time}...")
next_prompt = get_next_prompt()

model = MusicGen.get_pretrained('medium')
model.set_generation_params(duration=clip_duration)

while next_prompt:
    start_time = time()
    next_prompt = next_prompt.replace(",", "")
    done_time = get_finish_time(clip_duration*duration_per_s)
    temp_file_path = f"{next_prompt}-{done_time}.txt"
    create_current_prompt_file(next_prompt, temp_file_path)
    print(f"Generating {next_prompt}, will be done at {done_time}...")
    now = datetime.now()
    date_time_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    wavs = model.generate([next_prompt])
    path = next_prompt.replace(" ","-")+"-"+date_time_string+".wav"
    print(f"Saving {path}...")
    audio_write(f'{path}', wavs[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    process_duration = int(time() - start_time)
    duration_per_s = process_duration // clip_duration
    if pb_key:
        try:
            pb.push_note(f"{next_prompt}", f"Took {process_duration} seconds ({duration_per_s} seconds per second of audio clip).")
        except Exception as e:
            print(f"Couldn't push note:\n{e}")
    remove_current_prompt_file(temp_file_path)
    next_prompt = get_next_prompt()
print("fun")
sleep(5)
if pb_key:
    pb.push_note("All done", f"")