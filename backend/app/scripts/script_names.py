from pathlib import Path

assets_path = Path("/home/hersimmar/Documents/theoric-examen-app/frontend/public/assets/signals")

def get_signal_names(folder):
    
    return [file.stem for file in folder.glob('*.png')]

# Execute
signal_names = get_signal_names(assets_path)

print(f"Found {len(signal_names)} signals:")
print(signal_names)