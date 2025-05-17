import subprocess
from google.colab import files

def slow_down_video(input_file, output_file, slow_factor):
    video_filter = f"setpts={slow_factor}*PTS"
    
    def atempo_filters(slow_factor):
        filters = []
        remain = 1/slow_factor
        while remain < 0.5:
            filters.append("atempo=0.5")
            remain /= 0.5
        filters.append(f"atempo={remain:.6f}")
        return ",".join(filters)
    
    audio_filter = atempo_filters(slow_factor)
    
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", f"[0:v] {video_filter} [v]; [0:a] {audio_filter} [a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "-preset", "fast",
        output_file
    ]
    
    print("Uruchamiam ffmpeg z komendą:")
    print(" ".join(command))
    
    subprocess.run(command, check=True)
    print(f"Zakończono spowalnianie. Plik zapisany jako {output_file}")

# --- Ustawienia ---
input_video = "ScreenRecording_05-17-2025 14-22-24_1.mov"
output_video = "output_slow.mov"
slow_factor = 606  # spowolnienie z 10s do 101 min

# --- WAŻNE! ---  
# Najpierw musisz wrzucić swój plik .mov do Colaba (po lewej stronie w panelu 'Files' kliknij "Upload" i wybierz plik)

slow_down_video(input_video, output_video, slow_factor)

# Po zakończeniu pobieramy plik
files.download(output_video)
