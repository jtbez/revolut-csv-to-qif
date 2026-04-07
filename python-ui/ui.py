#!/usr/bin/env python3
"""
Revolut CSV to QIF Converter - Modern GUI
Clean and modern interface with proper drag and drop support
"""

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path


class RevolutConverterApp:
    """Main application with drag and drop support."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Revolut CSV to QIF Converter")
        self.root.geometry("600x350")
        
        # Node script path
        self.node_script = Path(__file__).parent / "src" / "index.js"
        self.current_file = None
        
        # Create UI
        self._create_main_ui()
    
    def _create_main_ui(self):
        """Create the main user interface."""
        main_frame = ttk.Frame(self.root,
                              padding="20",
                              relief=tk.GROOVE,
                              borderwidth=1)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_icon = ttk.Label(header_frame, text="📊", font=('Segoe UI', 24))
        header_icon.pack(side=tk.LEFT, padx=10)
        
        header_title = ttk.Label(header_frame,
                                text="CSV to QIF Converter",
                                font=('Segoe UI', 16, 'bold'),
                                foreground='#333')
        header_title.pack(side=tk.LEFT, padx=10)
        
        # Info frame with drag and drop support
        info_frame = ttk.LabelFrame(main_frame,
                                   text="File Selection",
                                   padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # File path display
        self.file_path_frame = ttk.Frame(info_frame)
        self.file_path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_path_label = ttk.Label(self.file_path_frame,
                                        text="No file selected",
                                        font=('Segoe UI', 10),
                                        foreground='#999',
                                        wraplength=500,
                                        justify=tk.LEFT)
        self.file_path_label.pack(side=tk.LEFT, fill=tk.X)
        
        # Buttons
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame,
                  text="📁 Select File",
                  command=self._browse_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(button_frame,
                  text="📂 Select Folder with CSV files",
                  command=self._browse_folder).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Conversion section
        convert_frame = ttk.LabelFrame(main_frame,
                                       text="Conversion",
                                       padding="15")
        convert_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.convert_btn = ttk.Button(convert_frame,
                                     text="📄 Convert Selected File",
                                     command=self._convert_selected)
        self.convert_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.convert_all_btn = ttk.Button(convert_frame,
                                         text="🔄 Convert All CSV Files in Folder",
                                         command=self._convert_all)
        self.convert_all_btn.pack(fill=tk.X)
        
        # Progress bar
        ttk.Label(main_frame,
                 text="Conversion Progress",
                 font=('Segoe UI', 9),
                 foreground='#777').pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame)
        self.progress_bar.pack(fill=tk.X)
        
        # Status display
        self.status_label = ttk.Label(main_frame,
                                     text="Ready to convert",
                                     font=('Segoe UI', 9),
                                     foreground='#777')
        self.status_label.pack(anchor=tk.CENTER, pady=(10, 0))
    
    def _browse_file(self):
        """Browse for and select a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.set_current_file(file_path)
    
    def _browse_folder(self):
        """Browse for and select a folder with CSV files."""
        folder_path = filedialog.askdirectory(
            title="Select Folder with CSV Files"
        )
        
        if folder_path:
            # Find the first CSV file in the folder
            csv_files = list(Path(folder_path).glob('*.csv'))
            if csv_files:
                self.set_current_file(str(csv_files[0]))
            else:
                messagebox.showinfo("No CSV Files", "No CSV files found in the selected folder")
    
    def set_current_file(self, filepath):
        """Set the current file to convert."""
        self.current_file = str(filepath)
        path = Path(self.current_file)
        
        self.file_path_label.config(
            text=f"Selected: {path.name}",
            foreground='#333'
        )
        
        # Update buttons
        if path.suffix.lower() == '.csv':
            self.convert_btn.config(text="📄 Convert Selected File")
            self.status_label.config(text="File ready for conversion")
        else:
            self.convert_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Selected file is not a CSV")
    
    def _convert_selected(self):
        """Convert the currently selected file."""
        if not self.current_file:
            messagebox.showerror("No File Selected", "Please select a CSV file first")
            return
        
        success = self.convert_file(self.current_file)
        
        if success:
            messagebox.showinfo("Success", "File converted successfully!")
            self.status_label.config(text="Success", foreground='#27ae60')
            self.set_current_file(None)  # Clear selection
    
    def _convert_all(self):
        """Convert all CSV files in current directory."""
        if not self.current_file:
            messagebox.showerror("No File Selected", "Please select a folder with CSV files first")
            return
        
        try:
            # Verify we have a directory
            if not Path(self.current_file).is_dir():
                messagebox.showerror("Invalid Selection", "Please select a folder first")
                return
            
            current_dir = Path(self.current_file)
            csv_files = sorted(current_dir.glob('*.csv'))
            
            if not csv_files:
                messagebox.showinfo("No CSV Files", "Found no CSV files in this directory")
                return
            
            success_count = 0
            
            for i, filepath in enumerate(csv_files, 1):
                progress = (i / len(csv_files)) * 100
                self.progress_bar['value'] = progress
                self.status_label.config(text=f"Converting {filepath.name} ({i}/{len(csv_files)})", foreground='#e67e22')
                self.root.update()  # Update UI
                
                if self.convert_file(str(filepath)):
                    success_count += 1
                
            
            self.progress_bar['value'] = 100
            self.status_label.config(text=f"All {len(csv_files)} files processed", foreground='#27ae60')
            
            if success_count == len(csv_files):
                messagebox.showinfo("Success", f"All {len(csv_files)} files converted successfully!")
            else:
                messagebox.showwarning("Partial Success", f"Successfully converted {success_count} of {len(csv_files)} files")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def convert_file(self, filepath):
        """Convert a single file to QIF format."""
        if not filepath or not filepath.lower().endswith('.csv'):
            return False
        
        try:
            if not self.node_script.exists():
                messagebox.showerror("Error", f"Node script not found: {self.node_script}")
                return False
            
            self.status_label.config(text="Processing...", foreground='#e67e22')
            self.root.update()  # Update UI
            
            output_dir = Path(filepath).parent
            result = subprocess.run(
                ["node", str(self.node_script), str(filepath), str(output_dir)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                messagebox.showerror("Conversion Failed", f"Error: {error_msg[:200] if error_msg else 'Unknown error occurred'}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Conversion timed out. The file might be too large.")
            return False
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else e.stdout.strip()
            messagebox.showerror("Conversion Failed", f"Error: {error_msg[:200] if error_msg else 'Unknown error occurred'}")
            return False
        except FileNotFoundError:
            messagebox.showerror("Error", "Node.js is not installed or not in PATH")
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False


def main():
    """Main entry point."""
    root = tk.Tk()
    app = RevolutConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()