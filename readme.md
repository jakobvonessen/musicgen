
# AudioCraft Music Generation Script

This script demonstrates how to use the AudioCraft library to generate music based on prompts. It also integrates Pushbullet notifications to keep you updated on the progress.

## Dependencies
```
pip install -U audiocraft
pip install torchaudio
pip install pushbullet.py
```

## How the Script Works

1. **Pushbullet Integration**:
   The script begins by checking for PushBullet API key in a `pushbullet_key.txt` file. This key is used for sending notifications about the progress of the music generation, but is not needed (you'll get warnings that you can ignore).

2. **Reading Prompts**:
   The script reads prompts from a `prompts.txt` file. After reading a prompt, it's removed from the file. Previous prompts can be found in `prev_prompts.txt`.

3. **Music Generation**:
   Using the AudioCraft's `MusicGen` model, the script generates music for each prompt. The duration of the generated music is defined by the `clip_duration` variable (hard-coded for now).

4. **Saving the Generated Audio**:
   After generating the music, the script saves it as a `.wav` file with a name derived from the prompt and the current timestamp.

5. **Notifications**:
   If Pushbullet integration is set up, the script sends a notification for each generated audio clip, indicating how long it took to create.

6. **Completion**:
   After processing all prompts, the script sends a final "All done" notification if Pushbullet is integrated.

To run the script, ensure you have all the necessary dependencies installed and provide the appropriate `pushbullet_key.txt` (if you want Pushbullet notifications).

