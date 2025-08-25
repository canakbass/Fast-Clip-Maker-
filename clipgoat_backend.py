# clipgoat_backend.py dosyası

import tempfile
import os
import subprocess
import asyncio
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
import time
import sys
print(sys.executable)
def tts_to_wav(text, out_path, rate=180, voice_gender='female'): # 'rate' parametresi hala alınıyor ama kullanılmıyor
    voice = 'tr-TR-AhmetNeural' if voice_gender == 'male' else 'tr-TR-EmelNeural'
    
    # Hız ayarını tamamen devre dışı bırakıyoruz.
    # edge_tts kütüphanesi kendi varsayılan hızını kullanacaktır.
    # Bu, "Invalid rate" hatasından kesin olarak kurtulmanın en doğrudan yoludur.
    
    # Debug çıktısı için istersen yorum satırından çıkarabilirsin:
    # print(f"DEBUG: TTS Hızı ayarı devre dışı bırakıldı. Ses {voice} kullanılarak sentezleniyor.")

    async def gen():
        # 'rate' parametresi 'Communicate' fonksiyonundan kaldırıldı.
        communicate = edge_tts.Communicate(text, voice=voice) 
        await communicate.save(out_path)
    
    # asyncio.run() çağrısının ana thread'i bloklamaması için dikkatli olunmalı.
    # Ancak tkinter ile threading kullanıldığı için bu burada sorun yaratmamalı.
    asyncio.run(gen())
    return out_path

def add_audio_to_video(video_path, audio_path, out_path):
    max_retries = 100 
    retry_delay = 0.1 

    for i in range(max_retries):
        try:
            with open(audio_path, "rb") as f:
                f.read(1) 
            break
        except (PermissionError, OSError) as e:
            time.sleep(retry_delay)
    else:
        raise RuntimeError(f"Ses dosyası ({audio_path}) erişilemiyor veya kilitli kaldı. WINERROR 32 Hatası Muhtemel!")

    video_clip = None 
    audio_clip = None 
    final_video_clip = None
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        if video_clip.duration > audio_clip.duration:
            video_clip = video_clip.subclip(0, audio_clip.duration)

        final_video_clip = video_clip.set_audio(audio_clip)
        final_video_clip.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=video_clip.fps)
        return out_path
    finally:
        if video_clip:
            video_clip.close()
        if audio_clip:
            audio_clip.close()
        if final_video_clip:
            final_video_clip.close() 
    

def add_subtitles_to_video(video_path, text, out_path, font_size=32, font_color='white', box_color='black', box_opacity=0.6, position='bottom'):
    video_clip = None 
    txt_clip = None   
    final_composite_clip = None 
    try:
        video_clip = VideoFileClip(video_path)
        duration = video_clip.duration
        
        txt_clip = TextClip(text, fontsize=font_size, color=font_color, bg_color=box_color, 
                            size=(video_clip.w * 0.9, None), 
                            method='caption', 
                            align='center',
                            stroke_color='black', 
                            stroke_width=1 
                            )

        pos = {'bottom': ('center', 'bottom'), 'top': ('center', 'top'), 'center': ('center', 'center')}.get(position, ('center', 'bottom'))
        
        txt_clip = txt_clip.set_position(pos).set_duration(duration)
        
        final_composite_clip = CompositeVideoClip([video_clip, txt_clip])
        
        final_composite_clip.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=video_clip.fps)
        return out_path
    finally:
        if video_clip:
            video_clip.close()
        if txt_clip:
            txt_clip.close() 
        if final_composite_clip:
            final_composite_clip.close() 

def create_story_video(background_video, story_text, font_size=32, font_color='white', box_color='black', box_opacity=0.6, position='bottom', tts_rate=180, tts_gender='female'):
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, 'story.wav')
        # tts_rate parametresi artık tts_to_wav içinde kullanılmayacak
        tts_to_wav(story_text, wav_path, voice_gender=tts_gender) # rate parametresi kaldırıldı
        
        video_with_audio_path = os.path.join(tmpdir, 'video_with_audio.mp4')
        add_audio_to_video(background_video, wav_path, video_with_audio_path)
        
        base_name = os.path.splitext(os.path.basename(background_video))[0]
        output_dir = os.path.dirname(background_video)
        final_video_name = f'{base_name}_story.mp4'
        final_video_path = os.path.join(output_dir, final_video_name)

        add_subtitles_to_video(
            video_with_audio_path, story_text, final_video_path,
            font_size=font_size, font_color=font_color, box_color=box_color, box_opacity=box_opacity, position=position
        )
        return final_video_path