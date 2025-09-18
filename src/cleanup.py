import os
import re
from datetime import datetime


def cleanup_old_backups(db_name: str, backup_dir: str, keep: int):
    """
    Remove old backups and associated files, keeping only the newest 'keep' backups.
    Handles all extensions for the same base filename as one backup.
    """
    # Regex to match backup files and extract timestamp
    pattern = re.compile(rf"^{re.escape(db_name)}-backup-(\d{{8}}_\d{{6}})\.dump")
    # Set to collect unique base filenames and their timestamps
    bases = {}
    for fname in os.listdir(backup_dir):
        match = pattern.match(fname)
        if match:
            timestamp = match.group(1)
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            base = f"{db_name}-backup-{timestamp}"
            bases[base] = dt
    # Sort base names by datetime descending (newest first)
    sorted_bases = sorted(bases.items(), key=lambda x: x[1], reverse=True)
    # Keep only the newest 'keep' backups
    to_delete = [base for base, _ in sorted_bases[keep:]]
    # Delete all files with matching base name and known extensions
    extensions = [
        ".dump",
        ".dump.enc",
        ".dump.zip",
        ".dump.enc.zip",
        ".dump.log",
        ".dump.key",
    ]
    for base in to_delete:
        for ext in extensions:
            fpath = os.path.join(backup_dir, base + ext)
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception as e:
                    print(f"Erro ao remover {fpath}: {e}")
