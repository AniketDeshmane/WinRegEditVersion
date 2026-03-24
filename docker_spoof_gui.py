import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import winreg
import subprocess
import json
import os
from profiles import WINDOWS_PROFILES, DEFAULT_PROFILE, get_profile_names, validate_profile

REGISTRY_ROOT = winreg.HKEY_LOCAL_MACHINE
REGISTRY_SUBKEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
BACKUP_FILE = "registry_backup_docker_spoof.json"

# Use the default profile from profiles.py
SPOOF_VALUES = WINDOWS_PROFILES.get(DEFAULT_PROFILE, {
    "CurrentBuild": "19045",
    "CurrentBuildNumber": "19045",
    "EditionID": "Professional",
    "DisplayVersion": "22H2",
})


def open_registry_key(access=winreg.KEY_READ):
    access |= winreg.KEY_WOW64_64KEY
    return winreg.OpenKey(REGISTRY_ROOT, REGISTRY_SUBKEY, 0, access)


def read_registry_values(keys=None):
    """
    Read registry values. If keys is None, read default set.
    """
    if keys is None:
        keys = ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]
    
    values = {}
    with open_registry_key(winreg.KEY_READ) as key:
        for name in keys:
            try:
                val, _ = winreg.QueryValueEx(key, name)
            except FileNotFoundError:
                val = "<not set>"
            values[name] = str(val)
    return values


def write_registry_value(name, value):
    with open_registry_key(winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))


def write_registry_values(values_dict):
    for name, value in values_dict.items():
        write_registry_value(name, value)


def save_backup(values_dict):
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(values_dict, f, indent=2)


def load_backup():
    if not os.path.exists(BACKUP_FILE):
        return None
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_running_as_admin():
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


class DockerSpoofApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows Version Spoof Helper")
        self.resizable(False, False)
        
        # Initialize current spoof values from default profile
        self.current_profile = DEFAULT_PROFILE
        self.current_spoof_values = WINDOWS_PROFILES.get(self.current_profile, {}).copy()

        container = ttk.Frame(self, padding=10)
        container.grid(row=0, column=0, sticky="nsew")

        self.installer_path_var = tk.StringVar(
            value=r"C:\Users\Aniket\Downloads\Docker Desktop Installer.exe"
        )
        self.installer_args_var = tk.StringVar(
            value="install --accept-license"
        )
        
        # Profile selection variable
        self.profile_var = tk.StringVar(value=self.current_profile)

        self._build_profile_selector(container)
        self._build_installer_path_ui(container)
        self._build_config_display(container)
        self._build_buttons(container)
        self._build_status(container)

        self.refresh_config_display()

        if not is_running_as_admin():
            messagebox.showwarning(
                "Administrator Required",
                "This tool must be run as Administrator to modify HKLM registry.\n\n"
                "Right-click the EXE and choose 'Run as administrator'.",
            )

    def _build_installer_path_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Installer Configuration", padding=10)
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Installer .exe path:").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(frame, textvariable=self.installer_path_var, width=60)
        entry.grid(row=0, column=1, sticky="ew", padx=(5, 5))

        browse_btn = ttk.Button(frame, text="Browse...", command=self.browse_installer)
        browse_btn.grid(row=0, column=2, sticky="e")

        ttk.Label(frame, text="Installer arguments (optional):").grid(row=1, column=0, sticky="w", pady=(5, 0))
        args_entry = ttk.Entry(frame, textvariable=self.installer_args_var, width=60)
        args_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(5, 5), pady=(5, 0))

    def _build_profile_selector(self, parent):
        """Build Windows profile selector frame"""
        frame = ttk.LabelFrame(parent, text="Windows Profile Selection", padding=10)
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Select Windows Version:").grid(row=0, column=0, sticky="w")
        
        profile_combo = ttk.Combobox(
            frame,
            textvariable=self.profile_var,
            values=get_profile_names(),
            state="readonly",
            width=40
        )
        profile_combo.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        profile_combo.bind("<<ComboboxSelected>>", self.on_profile_changed)

    def on_profile_changed(self, event=None):
        """Handle profile selection change"""
        profile_name = self.profile_var.get()
        profile = WINDOWS_PROFILES.get(profile_name)
        
        if profile:
            self.current_profile = profile_name
            self.current_spoof_values = profile.copy()
            
            # Convert integer values to strings for display
            for key, value in self.current_spoof_values.items():
                self.current_spoof_values[key] = str(value)
            
            self.refresh_config_display()
            self.status_var.set(f"Profile changed to: {profile_name}")

    def _build_config_display(self, parent):
        frame = ttk.LabelFrame(parent, text="Registry Configuration (HKLM)", padding=10)
        frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        header_current = ttk.Label(frame, text="Current value", font=("Segoe UI", 9, "bold"))
        header_target = ttk.Label(frame, text="Spoof target value", font=("Segoe UI", 9, "bold"))
        header_current.grid(row=0, column=1, sticky="w", padx=(5, 5))
        header_target.grid(row=0, column=3, sticky="w", padx=(5, 5))

        self.current_labels = {}
        self.target_labels = {}

        fields = [
            ("CurrentBuild", "Build"),
            ("CurrentBuildNumber", "BuildNumber"),
            ("EditionID", "Edition"),
            ("DisplayVersion", "DisplayVersion"),
        ]

        for i, (key, label_text) in enumerate(fields, start=1):
            ttk.Label(frame, text=f"{label_text}:").grid(row=i, column=0, sticky="w")

            cur_label = ttk.Label(frame, text="-")
            cur_label.grid(row=i, column=1, sticky="w", padx=(5, 5))
            self.current_labels[key] = cur_label

            ttk.Label(frame, text="→").grid(row=i, column=2, sticky="w")

            target_label = ttk.Label(frame, text=self.current_spoof_values.get(key, "-"))
            target_label.grid(row=i, column=3, sticky="w", padx=(5, 5))
            self.target_labels[key] = target_label

        self.description_label = ttk.Label(
            frame,
            text=(
                "This tool temporarily spoofs what Windows version your system reports\n"
                "(e.g. Windows 10 Pro 22H2) so installers that require a higher version\n"
                "can run, and then lets you restore the original values from backup."
            ),
            foreground="gray"
        )
        self.description_label.grid(row=len(fields) + 1, column=0, columnspan=4, sticky="w", pady=(8, 0))

    def _build_buttons(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        backup_install_btn = ttk.Button(
            frame,
            text="1) Backup + Spoof + Install",
            command=self.backup_spoof_install
        )
        backup_install_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        restore_btn = ttk.Button(
            frame,
            text="2) Restore from Backup",
            command=self.restore_from_backup
        )
        restore_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _build_status(self, parent):
        frame = ttk.LabelFrame(parent, text="Status", padding=10)
        frame.grid(row=4, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(frame, textvariable=self.status_var, foreground="blue")
        self.status_label.grid(row=0, column=0, sticky="w")

    def browse_installer(self):
        path = filedialog.askopenfilename(
            title="Select Installer Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.installer_path_var.set(path)

    def refresh_config_display(self):
        try:
            current = read_registry_values()
        except PermissionError:
            current = {
                k: "<Permission denied>"
                for k in ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]
            }

        for key, label in self.current_labels.items():
            label.config(text=current.get(key, "-"))
        
        # Update target labels with current profile values
        for key, label in self.target_labels.items():
            label.config(text=self.current_spoof_values.get(key, "-"))

    def backup_spoof_install(self):
        installer_path = self.installer_path_var.get().strip()
        if not installer_path or not os.path.isfile(installer_path):
            messagebox.showerror(
                "Installer not found",
                f"The installer path is invalid:\n\n{installer_path}"
            )
            return

        try:
            current_values = read_registry_values()
            save_backup(current_values)
        except PermissionError:
            messagebox.showerror(
                "Registry Permission Error",
                "Could not read/backup registry values.\n"
                "Make sure you are running this program as Administrator."
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Backup Error",
                f"Unexpected error while backing up registry:\n{e}"
            )
            return

        try:
            # Convert values to strings for registry writing
            spoof_values_to_write = {k: str(v) for k, v in self.current_spoof_values.items()}
            write_registry_values(spoof_values_to_write)
        except PermissionError:
            messagebox.showerror(
                "Registry Permission Error",
                "Could not write spoofed registry values.\n"
                "Make sure you are running this program as Administrator."
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Spoof Error",
                f"Unexpected error while writing spoofed values:\n{e}"
            )
            return

        self.status_var.set("Backup saved. Registry spoofed. Starting Docker installer...")
        self.refresh_config_display()
        self.update_idletasks()

        try:
            # Build command: installer path + optional arguments split by spaces
            args_text = self.installer_args_var.get().strip()
            if args_text:
                cmd = [installer_path] + args_text.split()
            else:
                cmd = [installer_path]

            subprocess.run(cmd, check=True)
            messagebox.showinfo(
                "Installer Finished",
                "Installer process has completed.\n\n"
                "You can now click 'Restore from Backup' to revert registry values."
            )
            self.status_var.set("Installer finished. Ready to restore if needed.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Installer Error",
                f"The installer returned a non-zero exit code:\n{e}"
            )
            self.status_var.set("Installer failed. You can still restore from backup.")
        except Exception as e:
            messagebox.showerror(
                "Installer Error",
                f"Unexpected error while running installer:\n{e}"
            )
            self.status_var.set("Installer error. You can still restore from backup.")

    def restore_from_backup(self):
        backup = load_backup()
        if backup is None:
            messagebox.showwarning(
                "No Backup Found",
                f"No backup file found.\n\nExpected: {os.path.abspath(BACKUP_FILE)}\n\n"
                "Use 'Backup + Spoof + Install' first, then restore."
            )
            return

        try:
            write_registry_values(backup)
        except PermissionError:
            messagebox.showerror(
                "Registry Permission Error",
                "Could not restore registry values from backup.\n"
                "Make sure you are running this program as Administrator."
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Restore Error",
                f"Unexpected error while restoring registry values:\n{e}"
            )
            return

        self.status_var.set("Registry restored from backup successfully.")
        self.refresh_config_display()
        messagebox.showinfo(
            "Restore Complete",
            "Original registry values have been restored from backup."
        )


def main():
    app = DockerSpoofApp()
    app.mainloop()


if __name__ == "__main__":
    main()

