#!/usr/bin/env python3
"""
Arduino Packet Protocol Visualizer
A professional GUI for demonstrating custom network packet structure
Author: Nile Jackson
"""

import tkinter as tk
from tkinter import ttk, messagebox
import struct
import random
import threading
import time
from datetime import datetime
import json

class PacketStructure:
    """Represents the C packet structure"""
    def __init__(self):
        self.start_byte = 0x02  # STX
        self.length = 0
        self.payload = bytearray(32)
        self.checksum = 0
        self.end_byte = 0x03  # ETX
    
    def calculate_checksum(self):
        """Calculate checksum for error detection"""
        checksum = self.start_byte + self.length
        checksum += sum(self.payload[:self.length])
        checksum += self.end_byte
        return checksum & 0xFF  # Keep only lower 8 bits
    
    def to_bytes(self):
        """Convert packet to bytes for transmission"""
        packet_bytes = struct.pack('B', self.start_byte)
        packet_bytes += struct.pack('B', self.length)
        packet_bytes += self.payload
        packet_bytes += struct.pack('B', self.checksum)
        packet_bytes += struct.pack('B', self.end_byte)
        return packet_bytes
    
    def validate(self):
        """Validate packet structure"""
        if self.start_byte != 0x02:
            return False, "Invalid start byte"
        if self.end_byte != 0x03:
            return False, "Invalid end byte"
        if self.length > 32:
            return False, "Payload length exceeds maximum"
        calculated_checksum = self.calculate_checksum()
        if self.checksum != calculated_checksum:
            return False, f"Checksum mismatch (expected: {calculated_checksum:02X}, got: {self.checksum:02X})"
        return True, "Valid packet"

class PacketVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Arduino Packet Protocol Visualizer")
        self.geometry("900x700")
        self.configure(bg='#1a1a2e')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Packet data
        self.packet = PacketStructure()
        self.transmission_active = False
        self.packet_history = []
        
        # Create UI
        self.create_widgets()
        self.update_display()
        
    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Dark theme colors
        bg_color = '#1a1a2e'
        fg_color = '#ffffff'
        accent_color = '#00d2d3'
        secondary_bg = '#16213e'
        
        self.style.configure('Title.TLabel', 
                           background=bg_color, 
                           foreground=fg_color,
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Heading.TLabel',
                           background=secondary_bg,
                           foreground=accent_color,
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('Value.TLabel',
                           background=secondary_bg,
                           foreground=fg_color,
                           font=('Consolas', 11))
        
        self.style.configure('Dark.TFrame',
                           background=secondary_bg,
                           relief='flat',
                           borderwidth=2)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self, bg='#1a1a2e')
        title_frame.pack(fill='x', pady=10)
        
        title = ttk.Label(title_frame, text="Arduino Packet Protocol Visualizer", 
                         style='Title.TLabel')
        title.pack()
        
        # Main container
        main_container = tk.Frame(self, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=20)
        
        # Left panel - Packet Structure
        left_panel = tk.Frame(main_container, bg='#1a1a2e')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_packet_structure_panel(left_panel)
        self.create_payload_panel(left_panel)
        self.create_control_panel(left_panel)
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_container, bg='#1a1a2e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_visualization_panel(right_panel)
        self.create_history_panel(right_panel)
    
    def create_packet_structure_panel(self, parent):
        """Create packet structure display"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame, text="Packet Structure", style='Heading.TLabel').pack(pady=5)
        
        # Create fields
        self.fields = {}
        field_info = [
            ("Start Byte", "start_byte", "0x{:02X}"),
            ("Length", "length", "{} bytes"),
            ("Checksum", "checksum", "0x{:02X}"),
            ("End Byte", "end_byte", "0x{:02X}")
        ]
        
        for label, attr, format_str in field_info:
            field_frame = tk.Frame(frame, bg='#16213e')
            field_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(field_frame, text=f"{label}:", width=15, anchor='w',
                    bg='#16213e', fg='#00d2d3', font=('Arial', 11)).pack(side='left')
            
            value_label = tk.Label(field_frame, text="", bg='#0f3460', fg='white',
                                 font=('Consolas', 11), width=20, anchor='w')
            value_label.pack(side='left', padx=5, fill='x', expand=True)
            
            self.fields[attr] = (value_label, format_str)
    
    def create_payload_panel(self, parent):
        """Create payload input panel"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame, text="Payload Data", style='Heading.TLabel').pack(pady=5)
        
        # Message input
        input_frame = tk.Frame(frame, bg='#16213e')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(input_frame, text="Message:", bg='#16213e', fg='#00d2d3',
                font=('Arial', 11)).pack(side='left', padx=5)
        
        self.message_var = tk.StringVar(value="Hello Arduino!")
        self.message_entry = tk.Entry(input_frame, textvariable=self.message_var,
                                    bg='#0f3460', fg='white', font=('Consolas', 11))
        self.message_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Hex display
        hex_frame = tk.Frame(frame, bg='#16213e')
        hex_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(hex_frame, text="Hex View:", bg='#16213e', fg='#00d2d3',
                font=('Arial', 11)).pack(anchor='w')
        
        self.hex_display = tk.Text(hex_frame, height=3, bg='#0f3460', fg='white',
                                 font=('Consolas', 9), wrap='word')
        self.hex_display.pack(fill='x', pady=5)
    
    def create_control_panel(self, parent):
        """Create control buttons"""
        frame = tk.Frame(parent, bg='#1a1a2e')
        frame.pack(fill='x', pady=10)
        
        buttons = [
            ("Generate Packet", self.generate_packet, '#00d2d3'),
            ("Validate", self.validate_packet, '#2ed573'),
            ("Transmit", self.transmit_packet, '#4a9eff'),
            ("Corrupt", self.corrupt_packet, '#ff6348')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(frame, text=text, command=command,
                          bg=color, fg='black' if color != '#ff6348' else 'white',
                          font=('Arial', 10, 'bold'), relief='flat',
                          padx=15, pady=8)
            btn.pack(side='left', padx=5, expand=True, fill='x')
    
    def create_visualization_panel(self, parent):
        """Create packet transmission visualization"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame, text="Transmission Visualization", style='Heading.TLabel').pack(pady=5)
        
        # Canvas for animation
        self.canvas = tk.Canvas(frame, bg='#0f3460', height=150)
        self.canvas.pack(fill='x', padx=10, pady=10)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(frame, textvariable=self.status_var,
                              bg='#16213e', fg='#00d2d3', font=('Arial', 12))
        status_label.pack(pady=5)
    
        def create_history_panel(self, parent):
         """Create packet history panel"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Transmission History", style='Heading.TLabel').pack(pady=5)
        
        # History listbox with scrollbar
        history_frame = tk.Frame(frame, bg='#16213e')
        history_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_frame, bg='#0f3460', fg='white',
                                        font=('Consolas', 9), selectmode='single',
                                        yscrollcommand=scrollbar.set)
        self.history_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)
    
    def generate_packet(self):
        """Generate a new packet from the message"""
        message = self.message_var.get()
        message_bytes = message.encode('utf-8')[:32]  # Limit to 32 bytes
        
        self.packet = PacketStructure()
        self.packet.length = len(message_bytes)
        self.packet.payload = bytearray(32)
        self.packet.payload[:len(message_bytes)] = message_bytes
        self.packet.checksum = self.packet.calculate_checksum()
        
        self.update_display()
        self.status_var.set("Packet generated successfully")
    
    def validate_packet(self):
        """Validate the current packet"""
        valid, message = self.packet.validate()
        
        if valid:
            self.status_var.set(f"✓ {message}")
            messagebox.showinfo("Validation", "Packet is valid!")
        else:
            self.status_var.set(f"✗ {message}")
            messagebox.showerror("Validation Error", message)
    
    def corrupt_packet(self):
        """Intentionally corrupt the packet for testing"""
        corruption_type = random.choice(['checksum', 'start_byte', 'end_byte'])
        
        if corruption_type == 'checksum':
            self.packet.checksum = (self.packet.checksum + 1) & 0xFF
            self.status_var.set("Corrupted: Checksum modified")
        elif corruption_type == 'start_byte':
            self.packet.start_byte = 0xFF
            self.status_var.set("Corrupted: Start byte modified")
        else:
            self.packet.end_byte = 0xFF
            self.status_var.set("Corrupted: End byte modified")
        
        self.update_display()
    
    def transmit_packet(self):
        """Animate packet transmission"""
        if self.transmission_active:
            return
        
        self.transmission_active = True
        thread = threading.Thread(target=self._animate_transmission)
        thread.daemon = True
        thread.start()
    
    def _animate_transmission(self):
        """Animation logic for packet transmission"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Draw sender and receiver
        self.canvas.create_text(50, height//2, text="SENDER", fill='#00d2d3', font=('Arial', 10, 'bold'))
        self.canvas.create_text(width-50, height//2, text="RECEIVER", fill='#00d2d3', font=('Arial', 10, 'bold'))
        
        # Animate packet
        packet_id = self.canvas.create_rectangle(60, height//2-10, 100, height//2+10, 
                                               fill='#4a9eff', outline='')
        
        for x in range(60, width-100, 5):
            self.canvas.coords(packet_id, x, height//2-10, x+40, height//2+10)
            self.canvas.update()
            time.sleep(0.02)
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        valid, status = self.packet.validate()
        history_entry = f"{timestamp} - Length: {self.packet.length}B - {status}"
        self.history_listbox.insert(0, history_entry)
        
        self.status_var.set("Transmission complete!")
        self.transmission_active = False
    
    def update_display(self):
        """Update all displays with current packet data"""
        # Update field displays
        for attr, (label, format_str) in self.fields.items():
            value = getattr(self.packet, attr)
            label.config(text=format_str.format(value))
        
        # Update hex display
        self.hex_display.delete(1.0, tk.END)
        hex_str = ""
        for i in range(0, self.packet.length, 8):
            hex_str += " ".join([f"{b:02X}" for b in self.packet.payload[i:i+8]])
            hex_str += "\n"
        self.hex_display.insert(1.0, hex_str.strip())
    
    def export_packet(self):
        """Export packet data as JSON"""
        packet_data = {
            "start_byte": self.packet.start_byte,
            "length": self.packet.length,
            "payload": list(self.packet.payload[:self.packet.length]),
            "checksum": self.packet.checksum,
            "end_byte": self.packet.end_byte,
            "timestamp": datetime.now().isoformat()
        }
        
        filename = f"packet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(packet_data, f, indent=2)
        
        self.status_var.set(f"Packet exported to {filename}")

def main():
    app = PacketVisualizer()
    
    # Add menu bar
    menubar = tk.Menu(app)
    app.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Export Packet", command=app.export_packet)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", 
        "Arduino Packet Protocol Visualizer\nDemonstrates custom network packet structure\nfor embedded systems communication"))
    
    app.mainloop()

if __name__ == "__main__":
    main()