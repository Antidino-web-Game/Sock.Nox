import subprocess
import sys
import os
import shutil

# Nom du script principal
script_name = "GUI.py"

# Fichiers à inclure
assets = ["logo.png"]
icon_file = "icon.ico"

# Nettoyage des anciens builds
for folder in ["build", "dist"]:
    if os.path.exists(folder):
        shutil.rmtree(folder)

# Construction de la commande PyInstaller
cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    f"--icon={icon_file}",
]

# Ajout des fichiers à inclure
for asset in assets:
    cmd.append(f"--add-data={asset};.")

# Ajout du script principal
cmd.append(script_name)

# Exécution
print("📦 Compilation en cours...")
subprocess.run(cmd)

print("\n✅ sock.Nox compilé avec succès !")
print("➡️ Fichier généré dans le dossier 'dist/'")