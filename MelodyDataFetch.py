import os
import yt_dlp

def download_wav(youtube_links, base_folder="./dataset/rapper_songs", new_output_folder="./new_rapper_songs"):
    if not os.path.exists(new_output_folder):
        os.makedirs(new_output_folder)

    ffmpeg_path = "./ffmpeg/bin/ffmpeg.exe"
    song_details = {}

    for rapper_index, (rapper, links) in enumerate(youtube_links.items(), start=1):
        for song_index, link in enumerate(links, start=1):
            song_key = f"rapper{rapper_index}_song{song_index}"
            base_file_path = os.path.join(base_folder, f"rapper{rapper_index}", f"{song_key}.wav")
            new_output_file = os.path.join(new_output_folder, f"{song_key}.wav")

            if os.path.exists(base_file_path):
                print(f"{base_file_path} already exists, skipping download.")
                continue

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg_path,
                'outtmpl': new_output_file,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    video_title = info_dict.get('title', 'Unknown')
                    channel_name = info_dict.get('uploader', rapper)
                    song_details[song_key] = f"{channel_name} - {video_title}"
                    ydl.download([link])
                    print(f"Downloaded and converted {song_details[song_key]} to {new_output_file}")
            except Exception as e:
                print(f"Failed to download {song_details[song_key]}. Error: {e}")

    return song_details

youtube_links = {
    "Eminem": [
        "https://www.youtube.com/watch?v=RSvEUOsq9P0", 
        "https://www.youtube.com/watch?v=XbGs_qK2PQA",  
        "https://www.youtube.com/watch?v=S9bCLPwzSC0", 
        "https://www.youtube.com/watch?v=Obim8BYGnOE",  
        "https://www.youtube.com/watch?v=SFH4tWd644g", 
        "https://www.youtube.com/watch?v=YVkUvmDQ3HY",  
        "https://www.youtube.com/watch?v=j5-yKhDd64s",  
        "https://www.youtube.com/watch?v=IaZReoUoDzU", 
        "https://www.youtube.com/watch?v=sthA7Q06Ar8",  
        "https://www.youtube.com/watch?v=soNLLPokjC4",   
        "https://www.youtube.com/watch?v=1-M4JrFcrNY",
        "https://www.youtube.com/watch?v=-qRTyVc3nAg",
        "https://www.youtube.com/watch?v=HnEwvZYdAlE",
        "https://www.youtube.com/watch?v=sthA7Q06Ar8",
        "https://www.youtube.com/watch?v=VnazSbbdYX8"
    ],
    "Lupe Fiasco": [
        "https://www.youtube.com/watch?v=cusyJRNX7YU",  
        "https://www.youtube.com/watch?v=vV86AnAZ0H8",  
        "https://www.youtube.com/watch?v=icCWdfNZ-hQ",  
        "https://www.youtube.com/watch?v=GBFfIdknRxE",  
        "https://www.youtube.com/watch?v=sG8DXQhNEGU",  
        "https://www.youtube.com/watch?v=RkS2s-G2ZQk",  
        "https://www.youtube.com/watch?v=r7YQ17GS_I4",  
        "https://www.youtube.com/watch?v=QVIk5pKYLJ0",  
        "https://www.youtube.com/watch?v=WHV5xkAZXiU",  
        "https://www.youtube.com/watch?v=LZRp9OCaM4s",  
        "https://www.youtube.com/watch?v=7XOAStfv-v0",
        "https://www.youtube.com/watch?v=ll9c1S3d_v4",
        "https://www.youtube.com/watch?v=T1aYM6NVXDo",
        "https://www.youtube.com/watch?v=AcoRc2ieFzE",
        "https://www.youtube.com/watch?v=sG8DXQhNEGU"
    ],
    "Jay Z": [
        "https://www.youtube.com/watch?v=gWzJNvbEa4s",  
        "https://www.youtube.com/watch?v=GjWsJlpkARo",  
        "https://www.youtube.com/watch?v=0YdLT0rL6L4",  
        "https://www.youtube.com/watch?v=jjCPc-47NmI",  
        "https://www.youtube.com/watch?v=9XEWVM1IhGY",  
        "https://www.youtube.com/watch?v=RW34u1KxGC4",  
        "https://www.youtube.com/watch?v=IHiFMW8s6zk",  
        "https://www.youtube.com/watch?v=Cn4alua9o2o",  
        "https://www.youtube.com/watch?v=UMqr0NjQprE",  
        "https://www.youtube.com/watch?v=9PSnZkWKv4k",  
        "https://www.youtube.com/watch?v=nG8o_9RliwU",
        "https://www.youtube.com/watch?v=kksewBACzNE",
        "https://www.youtube.com/watch?v=4O-IE7fdTS4",
        "https://www.youtube.com/watch?v=pVXMnNZiY84",
        "https://www.youtube.com/watch?v=hUPCzdIokps"
        
        
        
    ],
    "Biggie": [
        "https://www.youtube.com/watch?v=Uz5o4EjCNLg",  
        "https://www.youtube.com/watch?v=phaJXp_zMYM",  
        "https://www.youtube.com/watch?v=glEiPXAYE-U",  
        "https://www.youtube.com/watch?v=jqUC9_aF--s",  
        "https://www.youtube.com/watch?v=ot9NT9W0Fog",  
        "https://www.youtube.com/watch?v=rEaPDNgUPLE", 
        "https://www.youtube.com/watch?v=WiFm_tD9JIQ",  
        "https://www.youtube.com/watch?v=6TnsIGsyUyw",  
        "https://www.youtube.com/watch?v=qs565NWYByw",  
        "https://www.youtube.com/watch?v=fMayh7FhLGE", 
        "https://www.youtube.com/watch?v=7Y8VPQcPHhY",
        "https://www.youtube.com/watch?v=iK0soPQXLSM",
        "https://www.youtube.com/watch?v=v1mKGlYL9jg",
        "https://www.youtube.com/watch?v=7fh3yQ46TUw",
        "https://www.youtube.com/watch?v=94bNyh6BBB0"
        
    ],
    "Nas": [
        "https://www.youtube.com/watch?v=hI8A14Qcv68", 
        "https://www.youtube.com/watch?v=lOHGCk38NlM",  
        "https://www.youtube.com/watch?v=3hOZaTGnHU4",  
        "https://www.youtube.com/watch?v=sdmrlfQol7s",  
        "https://www.youtube.com/watch?v=VC4ORS5n9Hg",  
        "https://www.youtube.com/watch?v=_srvHOu75vM", 
        "https://www.youtube.com/watch?v=X3CGu0ezd68",  
        "https://www.youtube.com/watch?v=GhWIZDYGDrA", 
        "https://www.youtube.com/watch?v=zfyQ8muKLdc",  
        "https://www.youtube.com/watch?v=9KVuxllwGqE", 
        "https://www.youtube.com/watch?v=bXMtP5U-29s",
        "https://www.youtube.com/watch?v=Qjd7EbUUds8",
        "https://www.youtube.com/watch?v=sdmrlfQol7s",
        "https://www.youtube.com/watch?v=HCDYgZM5yq0",
        "https://www.youtube.com/watch?v=HGcWhJiIv1c"
        
    ],
    "Tupac": [
        "https://www.youtube.com/watch?v=fAJfDP3b5_U",  
        "https://www.youtube.com/watch?v=b0iIA5p8swk",  
        "https://www.youtube.com/watch?v=eXvBjCO19QY", 
        "https://www.youtube.com/watch?v=j007Uc65lQs",  
        "https://www.youtube.com/watch?v=Mb1ZvUDvLDY",  
        "https://www.youtube.com/watch?v=pFNDh4smb6k",  
        "https://www.youtube.com/watch?v=77nB_9uIcN4",  
        "https://www.youtube.com/watch?v=LiCjD5qVV_U", 
        "https://www.youtube.com/watch?v=9S96qfXKKRY", 
        "https://www.youtube.com/watch?v=dFuF8sWTRCY", 
        "https://www.youtube.com/watch?v=GTFo0VKnNZY",
        "https://www.youtube.com/watch?v=GH4jyEtueSQ",
        "https://www.youtube.com/watch?v=oheG-xc7j2Y",
        "https://www.youtube.com/watch?v=VQVRFH9XH1A",
        "https://www.youtube.com/watch?v=3HMRLEceXMM"
    ],
    "Kendrick Lamar": [
        "https://www.youtube.com/watch?v=Z-48u_uWMHY",  
        "https://www.youtube.com/watch?v=Wh-yg-rD-T4", 
        "https://www.youtube.com/watch?v=8-ejyHzz3XE", 
        "https://www.youtube.com/watch?v=GF8aaTu2kg0",  
        "https://www.youtube.com/watch?v=QjlFqgRbICY", 
        "https://www.youtube.com/watch?v=tvTRZJ-4EyI",  
        "https://www.youtube.com/watch?v=WgRJ2BtWn8g",  
        "https://www.youtube.com/watch?v=hRK7PVJFbS8",  
        "https://www.youtube.com/watch?v=uAPUkgeiFVY",  
        "https://www.youtube.com/watch?v=DBR_pogbp6g",  
        "https://www.youtube.com/watch?v=T6eK-2OQtew",
        "https://www.youtube.com/watch?v=2QiFl9Dc7D0",
        "https://www.youtube.com/watch?v=NPqDIwWMtxg",
        "https://www.youtube.com/watch?v=uX6uBHPGfSs",
        "https://www.youtube.com/watch?v=KKCSwOVudMo"
        
    ],
    "Drake": [
        "https://www.youtube.com/watch?v=Zfp3KfYH0xA",
        "https://www.youtube.com/watch?v=bZ8ntWZQUyg",
        "https://www.youtube.com/watch?v=uxpDa-c-4Mc",
        "https://www.youtube.com/watch?v=kAsoZc7MFCg",
        "https://www.youtube.com/watch?v=IV-XT27UOHo",
        "https://www.youtube.com/watch?v=RubBzkZzpUA",
        "https://www.youtube.com/watch?v=Yaid4y9g1NU",
        "https://www.youtube.com/watch?v=DMvaSqDnHl8",
        "https://www.youtube.com/watch?v=xpVfcZ0ZcFM",
        "https://www.youtube.com/watch?v=uxpDa-c-4Mc",
        "https://www.youtube.com/watch?v=PsW85VbSau0",
        "https://www.youtube.com/watch?v=fpXCtZ8johc",
        "https://www.youtube.com/watch?v=nSf3pBIX2RU",
        "https://www.youtube.com/watch?v=zcGjOC_LjoQ",
        "https://www.youtube.com/watch?v=CAzsA2OCZFs"
    ],
    "J. Cole": [
        "https://www.youtube.com/watch?v=eRaFMlZ1YHA",
        "https://www.youtube.com/watch?v=df44gpjzAFo",
        "https://www.youtube.com/watch?v=99f94NP_DJ4",
        "https://www.youtube.com/watch?v=g3mVwt0B6G4",
        "https://www.youtube.com/watch?v=0EnRK5YvBwU",
        "https://www.youtube.com/watch?v=xqFKSu-BvnU",
        "https://www.youtube.com/watch?v=ew7qhDBQcU4",
        "https://www.youtube.com/watch?v=bFewu1ATBFs",
        "https://www.youtube.com/watch?v=6tjlU4w4fSo",
        "https://www.youtube.com/watch?v=e8CLsYzE5wk",
        "https://www.youtube.com/watch?v=EF734jlr7TU",
        "https://www.youtube.com/watch?v=1qESHqhms_8",
        "https://www.youtube.com/watch?v=OZa3HyVLimQ",
        "https://www.youtube.com/watch?v=d15cxI5yx5c",
        "https://www.youtube.com/watch?v=-dyPeGDeS3o"
    ],
    "Pusha T": [
        "https://www.youtube.com/watch?v=l6C5XUU2Vtc",
        "https://www.youtube.com/watch?v=HLBXC760ZAI",
        "https://www.youtube.com/watch?v=RMhIC6195KU",
        "https://www.youtube.com/watch?v=TBZ-qca_99o",
        "https://www.youtube.com/watch?v=merQWEu-vck",
        "https://www.youtube.com/watch?v=7kiNsjeYsVs",
        "https://www.youtube.com/watch?v=kUK67HP8PvY",
        "https://www.youtube.com/watch?v=yxlK0Wuky0s",
        "https://www.youtube.com/watch?v=hGhC473BCIM",
        "https://www.youtube.com/watch?v=DawrlSwHUiM",
        "https://www.youtube.com/watch?v=M6apli5j43Q",
        "https://www.youtube.com/watch?v=Clo0U1BMR5I",
        "https://www.youtube.com/watch?v=qmD0fLMYAwk",
        "https://www.youtube.com/watch?v=ZIaRsy9_JeU",
        "https://www.youtube.com/watch?v=gXEuROJb_wI"
        
    ],
     "Lil Wayne": [
        "https://www.youtube.com/watch?v=NdgpcwqBSPg",
        "https://www.youtube.com/watch?v=tAaF00AL4i0",
        "https://www.youtube.com/watch?v=awDimZED_SA",
        "https://www.youtube.com/watch?v=es6goNuH0lY",
        "https://www.youtube.com/watch?v=srQuR4cfYSo",
        "https://www.youtube.com/watch?v=ujgCGofWjcY",
        "https://www.youtube.com/watch?v=sINGvrL61VY",
        "https://www.youtube.com/watch?v=Nfsm3EajFFI",
        "https://www.youtube.com/watch?v=nqdKsvyA1qo",
        "https://www.youtube.com/watch?v=w7NHVRDQ-As",
        "https://www.youtube.com/watch?v=Q74hkeu78TI",
        "https://www.youtube.com/watch?v=aFF4nZdmKXM",
        "https://www.youtube.com/watch?v=-bbLRrbnXSA",
         "https://www.youtube.com/watch?v=HE6-Oc76RFs",
         "https://www.youtube.com/watch?v=Acu5xHka6Wg"
        
         
    ],
    "50 Cent": [
        "https://www.youtube.com/watch?v=7CVGDPqnZj8",
        "https://www.youtube.com/watch?v=xIl4ZGd8MPc",
        "https://www.youtube.com/watch?v=5qm8PH4xAss",
        "https://www.youtube.com/watch?v=Jy1D6caG8nU",
        "https://www.youtube.com/watch?v=1XRa-DDsfsc",
        "https://www.youtube.com/watch?v=d9vtmV6oTbY",
        "https://www.youtube.com/watch?v=KQZnU4kjfV8",
        "https://www.youtube.com/watch?v=UsIh-M8oY18",
        "https://www.youtube.com/watch?v=yM8a8pZARIE",
        "https://www.youtube.com/watch?v=LrJAHaSUvkc",
        "https://www.youtube.com/watch?v=e5zAjDLy7L4",
        "https://www.youtube.com/watch?v=8wgwwJHwk_k",
        "https://www.youtube.com/watch?v=T2l-I-bTSs8",
        "https://www.youtube.com/watch?v=6TsAEHC-epA",
        "https://www.youtube.com/watch?v=1XDovrRnDN4"
        
    ],
    "JID": [
        "https://www.youtube.com/watch?v=k_TbOH8iE4U",
        "https://www.youtube.com/watch?v=MrytARdrZZQ",
        "https://www.youtube.com/watch?v=6qSijgO6n7Q",
        "https://www.youtube.com/watch?v=SEG92Z_NGJE",
        "https://www.youtube.com/watch?v=01vZrReuV84",
        "https://www.youtube.com/watch?v=Dmt7S66ulGc",
        "https://www.youtube.com/watch?v=L0NI2O790Zw",
        "https://www.youtube.com/watch?v=JHubi3JuosU",
        "https://www.youtube.com/watch?v=XZ4vKF6ueS8",
        "https://www.youtube.com/watch?v=AXeugCTXsNs",
        "https://www.youtube.com/watch?v=WdzoMl9t814",
        "https://www.youtube.com/watch?v=S3I6lrh1aWw",
        "https://www.youtube.com/watch?v=1EkLBJxUopY",
        "https://www.youtube.com/watch?v=zEW3RNefqFY",
        "https://www.youtube.com/watch?v=7lMBbVKpbzg"
    ],
    "Denzel Curry": [
        "https://www.youtube.com/watch?v=bbcjQromsiA",
        "https://www.youtube.com/watch?v=ibxqnEnOcEQ",
        "https://www.youtube.com/watch?v=K-41__7bzC0",
        "https://www.youtube.com/watch?v=qd68jAiz96Q",
        "https://www.youtube.com/watch?v=FFa-XE0eMqc",
        "https://www.youtube.com/watch?v=mw1X8gf9Erw",
        "https://www.youtube.com/watch?v=BWiLjc2z-iM",
        "https://www.youtube.com/watch?v=6T2j4HDXyl8",
        "https://www.youtube.com/watch?v=XivJqBtHzmk",
        "https://www.youtube.com/watch?v=-fL6hd9rc1Y",
        "https://www.youtube.com/watch?v=PlLLXchYuD4",
        "https://www.youtube.com/watch?v=B7PS4gJe5Y4",
        "https://www.youtube.com/watch?v=kpoh7jxj76A",
        "https://www.youtube.com/watch?v=QRjZn8SSrrs",
        "https://www.youtube.com/watch?v=s9dj_YkHQDE"
    ],
    "Mac Miller": [
        "https://www.youtube.com/watch?v=3ADKdqcdNqs",
        "https://www.youtube.com/watch?v=vuCyrtGQhAk",
        "https://www.youtube.com/watch?v=gOAO4y9Yu_k",
        "https://www.youtube.com/watch?v=Q7oO6LBA0Xg",
        "https://www.youtube.com/watch?v=wdaI7F3Jv5M",
        "https://www.youtube.com/watch?v=v2Q9kltRpbE",
        "https://www.youtube.com/watch?v=Wvm5GuDfAas",
        "https://www.youtube.com/watch?v=WGzhlLCdAVo",
        "https://www.youtube.com/watch?v=XbSuMV7ghm8",
        "https://www.youtube.com/watch?v=No7KJKx-yKY",
        "https://www.youtube.com/watch?v=-leEwgiNUoY",
        "https://www.youtube.com/watch?v=8RUbM_WSYTI",
        "https://www.youtube.com/watch?v=74TFS8r_SMI",
        "https://www.youtube.com/watch?v=T_Mt6Isew_0",
        "https://www.youtube.com/watch?v=NR8UDU57i_8"
        
    ] 
}

song_details = download_wav(youtube_links)
for k, v in song_details.items():
    print(k, v)

artists_songs = {
    "Eminem": [
        "Lose Yourself", 
        "Rap God", 
        "Mockingbird", 
        "Till I Collapse", 
        "Stan", 
        "Without Me", 
        "Not Afraid", 
        "The Way I Am", 
        "Sing For The Moment", 
        "Houdini",
        "The Real Slim Shady",
        "White America",
        "When I'm Gone",
        "Soldier",
        "Superman"
    ],
    "Lupe Fiasco": [
        "Ms Mural", 
        "Kick Push 2", 
        "Adoration of the Magi", 
        "Hip-hop saved my life", 
        "Wav files", 
        "Little Death", 
        "Paris Tokyo", 
        "The Cool", 
        "King Nas", 
        "Hurt Me Soul",
        "Daydreamin",
        "The Coolest",
        "He Say She Say",
        "Samurai",
        "WAV Files"
        
    ],
    "Jay Z": [
        "where I'm from",
        "dead presidents ii",
        "99 problems",
        "u don't know",
        "public service announcement",
        "Hard Knock Life (Ghetto Anthem)",
        "takeover",
        "Heart of the city",
        "4:44",
        "can I live"
        "I Just Wanna Love U (Give It 2 Me)",
        "dirt of your shoulder",
        "D’Evils",
        "Friend or Foe",
        "Imaginary Player"
        
        
    ],
    "Biggie": [
        "Everyday Struggle",
        "big poppa",
        "hypnotize",
        "dead wrong",
        "ten crack commandments",
        "Party & Bullshit",
        "unbelievable",
        "I got a story to tell",
        "warning",
        "Gimme The Loot",
        "Juicy",
        "things done changed",
        "Suicidal Thoughts",
        "Ready to Die",
        "What’s Beef?"
    ],
    "Nas": [
        "ny state of mind",
        "made you look",
        "it ain't hard to tell",
        "doo rags",
        "Nas is like",
        "the world is yours",
        "the message",
        "one mic",
        "ether",
        "Memory Lane (Sittin’ in da Park)",
        "Nas is like",
        "one love",
        "Doo Rags",
        "Halftime",
        "Get Down"
    ],
    "Tupac": [
        "keep ya head up",
        "Hail Mary",
        "changes",
        "trapped",
        "dear mama",
        "so many tears",
        "ambitions as a ridah",
        "I ain't mad at cha",
        "to live and die in LA",
        "me and my girlfriend",
        "Can't C Me",
        "Holla At Me",
        "Do For Love",
        "Can U Get Away",
        "Life Goes On"
    ],
    "Kendrick Lamar": [
        "alright",
        "backseat freestyle",
        "Swimming Pools (Drank)",
        "bitch don't kill my vibe",
        "ADHD",
        "humble",
        "sing about me",
        "king kunta",
        "the heart part 5",
        "element",
        "not like us",
        "meet the grahams",
        "euphoria",
        "DNA",
        "m.A.A.d city"
    ],
    "Drake": [
        "Best I Ever Had",
        "5AM In Toronto",
        "hotline bling",
        "Tuscan leather",
        "Know yourself",
        "started from the bottom",
        "energy",
        "push ups",
        "God's plan",
        "hotline bling",
        "controlla",
        "back to back",
        "legend",
        "views",
        "6 God"
    ],
    "J Cole": [
        "apparently",
        "false prophets",
        "workout",
        "9 5 . s o u t h",
        "no role modelz",
        "born sinner",
        "atm",
        "A Tale of 2 Citiez",
        "love yourz",
        "middle child",
        "immortal",
        "miss america",
        "snow on tha bluff",
        "january 28th",
        "lights please"
    ],
    "Pusha T": [
        "king push",
        "doesn't matter",
        "santeria",
        "untouchable",
        "infrared",
        "the games we play",
        "if you know you know",
        "crutches, crosses, caskets",
        "what would meek do",
        "numbers on the boards",
        "brambleton",
        "my god",
        "intro",
        "just so you remember",
        "alone in vegas"
    ],
    "Lil Wayne": [
        "A milli",
        "Hustler Musik",
        "fireman",
        "Dr carter",
        "go dj",
        "this is the carter",
        "3peat",
        "problems",
        "I miss my dawgs",
        "Nightmares Of The Bottom",
        "how to love",
        "blunt blowing",
        "dedicate",
        "can't be broken",
        "let the beat build"
    ],
    "50 Cent": [
        "Many Men (Wish Death)",
        "what up gangsta",
        "in da club",
        "P.I.M.P.",
        "wanksta",
        "I get money",
        "window shopper",
        "Hustler's ambition",
        "just a lil bit",
        "disco inferno",
        "ski mask way",
        "talk about me",
        "best friend",
        "i get it in",
        "ryder music"
    ],
    "JID": [
        "151 Rum",
        "Raydar",
        "Kody Blu 31",
        "EdEddnEddy",
        "Never",
        "Workin Out",
        "Off Da Zoinkys",
        "Hereditary",
        "Slick Talk",
        "Crack Sandwich",
        "Sistanem",
        "Money",
        "Mounted Up",
        "Just Da Other Day",
        "Despacito Too"
    ],

    "Denzel Curry": [
        "speedboat",
        "zuu",
        "ricky",
        "walkin",
        "worst comes to worst",
        "x-wing",
        "the last",
        "the ills",
        "larger than life",
        "SUMO | ZUMO",
        "TABOO | TA13OO",
        "PERCS | PERCZ",
        "Gook",
        "CLOUT COBAIN | CLOUT CO13A1N",
        "this life"
    ],

    "Mac Miller": [
        "soulmate",
        "brand name",
        "rush hour",
        "objects in the mirror",
        "watching movies",
        "buttons",
        "programs",
        "hurt feelings",
        "perfecto",
        "frick pack market",
        "desperado",
        "ascension",
        "donald trump",
        "smile back",
        "best day ever"
    ]
}

import requests
import lyricsgenius
from retry import retry
from requests.exceptions import Timeout

GENIUS_CLIENT_ID = 'YOUR_GENIUS_CLIENT_ID'
GENIUS_CLIENT_SECRET = 'YOUR_GENIUS_CLIENT_SECRET'
token_url = 'https://api.genius.com/oauth/token'

@retry(exceptions=Exception, tries=5, delay=2, backoff=2)
def get_access_token():
    data = {
        'client_id': GENIUS_CLIENT_ID,
        'client_secret': GENIUS_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to obtain access token. Status code: {response.status_code}")

access_token = get_access_token()
genius_api = lyricsgenius.Genius(access_token, timeout=15, retries=3)

lyrics_dir = "./new_rapper_songs"
os.makedirs(lyrics_dir, exist_ok=True)

@retry(exceptions=(Exception, Timeout), tries=5, delay=2, backoff=2)
def fetch_and_save_lyrics(artist_id, artist_name, songs):
    for song_index, song in enumerate(songs, start=1):
        filename = f"rapper{artist_id}_song{song_index}.txt"
        filepath = os.path.join(lyrics_dir, filename)
        old_path = "./dataset/rapper_songs"
        old = os.path.join(old_path, f"rapper{artist_id}", filename)
        
        if os.path.exists(old):
            print(f"Lyrics for {song} by {artist_name} already exist. Skipping...")
            continue
        
        try:
            song_lyrics = genius_api.search_song(song, artist_name)
            if song_lyrics:
                with open(old, 'w', encoding='utf-8') as file:
                    file.write(song_lyrics.lyrics)
                print(f"Lyrics for {song} by {artist_name} saved successfully.")
            else:
                print(f"Lyrics not found for {song} by {artist_name}")
        except Timeout:
            print(f"Request timed out for {song} by {artist_name}. Skipping...")

for artist_id, (artist_name, songs) in enumerate(artists_songs.items(), start=1):
    print(f"Fetching and saving lyrics for {artist_name}...")
    fetch_and_save_lyrics(artist_id, artist_name, songs)

def preprocess_text(text):
    text = re.sub(r'^.*?\[', '[', text, 1)
    text = re.sub(r'\[.*?\]', '', text)
    text = text.lower()
    text = re.sub(r'[^\w\s\n]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'(?<!\n)\s*\n\s*(?!\n)', '\n', text)
    
    processed_lines = []
    for line in text.split('\n'):
        if line.strip():
            processed_line = f"< SOS > {line.strip()} <EOS>"
            processed_lines.append(processed_line)
    
    return '\n'.join(processed_lines)

def process_text_files(main_dir):
    for subfolder in os.listdir(main_dir):
        subfolder_path = os.path.join(main_dir, subfolder)
        if os.path.isdir(subfolder_path):
            for file_name in os.listdir(subfolder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(subfolder_path, file_name)

                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()

                    processed_text = preprocess_text(text)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(processed_text)

                    print(f"Processed {file_path}")

main_dir = "./dataset/rapper_songs"
process_text_files(main_dir)