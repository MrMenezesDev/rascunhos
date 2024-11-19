import os
import imageio
import py5_tools


def save_frames(seed, limit=50, start=0):
    frames_dir = f"./tmp/frames_{seed}/"
    py5_tools.save_frames(frames_dir, limit=limit, start=start)
    return frames_dir


def create_gif(frames_dir, seed, infinite_loop=True):
    # Lista todos os arquivos na pasta e filtra apenas os arquivos PNG
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    print(f"Creating GIF with {len(frame_files)} frames.")
    print(f"Frames dir: {frames_dir}")
    print(f"Seed: {seed}")  
    # Lê as imagens e as adiciona à lista
    images = []
    for frame_file in frame_files:
        filename = os.path.join(frames_dir, frame_file)
        images.append(imageio.imread(filename))

    if infinite_loop:
        # Adiciona as imagens em ordem reversa para criar um loop infinito
        images += images[::-1]
    
    # Verifica se há imagens antes de criar o GIF
    if images:
        # Cria o GIF com o nome da pasta incluído
        gif_filename = f"./tmp/animation_{seed}.gif"
        imageio.mimsave(gif_filename, images, duration=0.1, loop=0)
    else:
        print("No images found to create GIF.")
    print(f"Animation saved as {gif_filename}")
