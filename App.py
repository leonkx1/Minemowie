import subprocess

def slow_down_video(input_file, output_file, slow_factor):
    """
    Spowalnia wideo i audio o podany slow_factor.
    
    :param input_file: ścieżka do oryginalnego pliku wideo
    :param output_file: ścieżka do wyjściowego pliku
    :param slow_factor: o ile razy spowolnić (np. 357)
    """
    
    # Przy spowolnieniu video musimy zmniejszyć fps, czyli przy slow_factor 357 fps zmniejszymy do fps/357
    # Alternatywnie możemy użyć filter setpts do video i atempo do audio
    
    # Ustawienie nowej prędkości wideo
    video_filter = f"setpts={slow_factor}*PTS"
    
    # Audio filter atempo obsługuje tylko 0.5x do 2.0x, więc dzielimy spowolnienie na kilka kroków
    # Przykładowo rozbijemy slow_factor na kilka mnożników audio, np. 0.5 x 0.5 x ... aż do slow_factor
    # Ponieważ 357 jest za duże, audio trzeba "powolnić" iteracyjnie
    
    # Rozbijamy slow_factor na wiele mnożników audio atempo (maks 2.0x na krok), ale dla spowolnienia >1 to odwrotnie: atempo=1/slow_factor
    # atempo obsługuje zakres 0.5-2, więc dla slow_factor=357 potrzebne jest wiele kroków
    
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
        "-preset", "fast",
        output_file
    ]
    
    print("Uruchamiam ffmpeg z komendą:")
    print(" ".join(command))
    
    subprocess.run(command, check=True)
    print(f"Zakończono spowalnianie. Plik zapisany jako {output_file}")

# Przykład użycia:
input_video = "minecraft.mp4"    # podmień na swój plik
output_video = "output_slow.mp4"
slow_factor = 357  # spowolnienie 17s do 101 min

slow_down_video(input_video, output_video, slow_factor)
