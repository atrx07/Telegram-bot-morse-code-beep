import telebot
import wave
import os

# Telegram bot token
BOT_TOKEN = "[Bot token]"
bot = telebot.TeleBot(BOT_TOKEN)

# Audio beep config
SAMPLE_RATE = 44100
BEEP_DURATION = 0.2  # seconds

# Frequencies for 1 and 0
FREQ_ONE = 1000
FREQ_ZERO = 500

# Output dir is current dir
output_dir = "."

def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def generate_beep_wav(binary_str, filename):
    print("Generating audio...")
    import numpy as np

    audio = []

    for bit in binary_str.replace(" ", ""):
        freq = FREQ_ONE if bit == '1' else FREQ_ZERO
        samples = (np.sin(2 * np.pi * freq * t / SAMPLE_RATE)
                   for t in range(int(SAMPLE_RATE * BEEP_DURATION)))
        audio.extend(samples)

    audio = np.array(audio)
    audio = (audio * 32767).astype(np.int16)

    filepath = os.path.join(output_dir, filename)
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())

    print(f"Saved audio to {filepath}")
    return filepath

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text.strip()
        print(f"\n[💬] Received: {text}")
        binary = text_to_binary(text)
        print(f"[🔢] Binary: {binary}")

        filename = f"{message.from_user.id}_beep.wav"
        wav_path = generate_beep_wav(binary, filename)

        bot.send_message(message.chat.id, f"📡 Binary of your message:\n`{binary}`", parse_mode="Markdown")
        bot.send_message(message.chat.id, f"Generating your audio.....")
        bot.send_audio(message.chat.id, open(wav_path, 'rb'))

        print("[✅] Audio sent.\n")

    except Exception as e:
        print(f"[❌] Error: {e}")
        bot.send_message(message.chat.id, "Something went wrong!")

print("[🚀] Bot is running...")
bot.polling()