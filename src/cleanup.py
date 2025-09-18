import os
import re


def cleanup_old_backups(db_name: str, backup_dir: str, keep: int):
    """
    Remove old backups and associated files, keeping only the newest 'keep' backups.
    """
    # Regex to match backup files and extract timestamp
    pattern = re.compile(rf"^{re.escape(db_name)}-backup-(\d{{8}}_\d{{6}})\.dump")
    # Collect all matching base filenames and their timestamps
    backups = []
    for fname in os.listdir(backup_dir):
        match = pattern.match(fname)
        if match:
            timestamp = match.group(1)
            base = f"{db_name}-backup-{timestamp}"
            backups.append((timestamp, base))
    # Sort by timestamp descending (newest first)
    backups.sort(reverse=True)
    # Keep only the newest 'keep' backups
    to_delete = backups[keep:]
    # Delete all associated files for each old backup
    for _, base in to_delete:
        for ext in [".dump", ".dump.enc", ".dump.zip", ".dump.enc.zip", ".dump.log"]:
            fpath = os.path.join(backup_dir, base + ext)
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception as e:
                    print(f"Erro ao remover {fpath}: {e}")

