#!/usr/bin/env python3
"""
Arduino Dual-Protocol Network Parser
Demonstrates both text-based (<COMMAND>) and binary packet protocols
Author: [Your Name]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import struct
import threading
import time
from datetime import datetime
import json


START_BYTE = 0xAA
END_BYTE = 0xBB
MAX_PAYLOAD = 32

class TextProtocol:
    """Handles text-based protocol: <COMMAND>"""
    @staticmethod
    def validate(data):
        """Validate text protocol format"""
        if len(data) < 2:
            return False, "Too short for valid protocol"
        if not (data.startswith('<') and data.endswith('>')):
            return False, "Missing < > markers"
        return True, "Valid text protocol"
    
    @staticmethod
    def extract_command(data):
        """Extract command from <COMMAND> format"""
        if data.startswith('<') and data.endswith('>'):
            return data[1:-1]
        return None

class BinaryPacket:
    """Represents the binary packet structure from protocol.h"""
    def __init__(self):
        self.start_byte = START_BYTE
        self.length = 0
        self.payload = bytearray(MAX_PAYLOAD)
        self.checksum = 0
        self.end_byte = END_BYTE
    
    def from_text_command(self, text_command):
        """Convert text command to binary packet"""
        command = text_command.strip('<>')
        command_bytes = command.encode('utf-8')[:MAX_PAYLOAD]
        
        self.length = len(command_bytes)
        self.payload = bytearray(MAX_PAYLOAD)
        self.payload[:self.length] = command_bytes
        self.checksum = self.calculate_checksum()
        
    def calculate_checksum(self):
        """Calculate checksum for packet validation"""
        checksum = self.length
        for i in range(self.length):
            checksum ^= self.payload[i]  # XOR checksum
        return checksum & 0xFF
    
    def to_bytes(self):
        """Convert packet to bytes for transmission"""
        packet = bytearray()
        packet.append(self.start_byte)
        packet.append(self.length)
        packet.extend(self.payload)
        packet.append(self.checksum)
        packet.append(self.end_byte)
        return packet
    
    def validate(self):
        """Validate binary packet structure"""
        if self.start_byte != START_BYTE:
            return False, f"Invalid start byte: 0x{self.start_byte:02X}"
        if self.end_byte != END_BYTE:
            return False, f"Invalid end byte: 0x{self.end_byte:02X}"
        if self.length > MAX_PAYLOAD:
            return False, f"Payload length {self.length} exceeds maximum {MAX_PAYLOAD}"
        
        calculated_checksum = self.calculate_checksum()
        if self.checksum != calculated_checksum:
            return False, f"Checksum mismatch (expected: 0x{calculated_checksum:02X}, got: 0x{self.checksum:02X})"
        
        return True, "Valid binary packet"

class DualProtocolVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Arduino Dual-Protocol Network Parser")
        self.geometry("1100x800")
        self.configure(bg='#1a1a2e')
        
        # Protocol states
        self.text_protocol = TextProtocol()
        self.binary_packet = BinaryPacket()
        self.transmission_active = False
        self.history = []
        
        # Available commands
        self.commands = [
            "LED_ON",
            "LED_OFF", 
            "TEMP_READ",
            "STATUS",
            "RESET"
        ]
        
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
       
        title_frame = tk.Frame(self, bg='#1a1a2e')
        title_frame.pack(fill='x', pady=10)
        
        title = tk.Label(title_frame, text="Arduino Dual-Protocol Network Parser", 
                        font=('Arial', 24, 'bold'), bg='#1a1a2e', fg='#00d2d3')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Text Protocol (<COMMAND>) ↔ Binary Packet Conversion", 
                           font=('Arial', 12), bg='#1a1a2e', fg='#888')
        subtitle.pack()
        
        
        main_container = tk.Frame(self, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=20)
        
        
        left_panel = self.create_panel(main_container, "Text Protocol Input")
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.create_text_protocol_section(left_panel)
        
        
        middle_panel = self.create_panel(main_container, "Protocol Conversion")
        middle_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.create_conversion_section(middle_panel)
        
        
        right_panel = self.create_panel(main_container, "Binary Packet Output")
        right_panel.pack(side='left', fill='both', expand=True)
        self.create_binary_packet_section(right_panel)
        
        
        bottom_panel = self.create_panel(self, "Transmission History")
        bottom_panel.pack(fill='x', padx=20, pady=(10, 20))
        self.create_history_section(bottom_panel)
    
    def create_panel(self, parent, title):
        """Create a styled panel"""
        frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=2)
        
        
        title_label = tk.Label(frame, text=title, font=('Arial', 14, 'bold'),
                              bg='#16213e', fg='#00d2d3', pady=10)
        title_label.pack(fill='x')
        
        return frame
    
    def create_text_protocol_section(self, parent):
        """Create text protocol input section"""
        
        input_frame = tk.Frame(parent, bg='#16213e')
        input_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(input_frame, text="Enter Command:", bg='#16213e', fg='white',
                font=('Arial', 11)).pack(anchor='w', pady=5)
        
        self.command_var = tk.StringVar()
        self.command_entry = tk.Entry(input_frame, textvariable=self.command_var,
                                    bg='#0f3460', fg='white', font=('Consolas', 12),
                                    insertbackground='white')
        self.command_entry.pack(fill='x', pady=5)
        self.command_entry.bind('<Return>', lambda e: self.process_text_command())
        
       
        tk.Label(input_frame, text="Quick Commands:", bg='#16213e', fg='white',
                font=('Arial', 11)).pack(anchor='w', pady=(15, 5))
        
        button_frame = tk.Frame(input_frame, bg='#16213e')
        button_frame.pack(fill='x')
        
        for i, cmd in enumerate(self.commands):
            btn = tk.Button(button_frame, text=cmd, 
                          command=lambda c=cmd: self.set_command(c),
                          bg='#0f3460', fg='white', font=('Arial', 9),
                          relief='flat', padx=10, pady=5)
            btn.grid(row=i//2, column=i%2, padx=5, pady=2, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.text_status_var = tk.StringVar(value="Ready for input")
        status_label = tk.Label(input_frame, textvariable=self.text_status_var,
                              bg='#0f3460', fg='#00d2d3', font=('Arial', 10),
                              pady=5)
        status_label.pack(fill='x', pady=(15, 5))
        
        
        process_btn = tk.Button(input_frame, text="Process Command",
                              command=self.process_text_command,
                              bg='#00d2d3', fg='black', font=('Arial', 11, 'bold'),
                              relief='flat', pady=8)
        process_btn.pack(fill='x', pady=10)
    
    def create_conversion_section(self, parent):
        """Create conversion visualization section"""
        canvas_frame = tk.Frame(parent, bg='#16213e')
        canvas_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Conversion visualization
        self.conversion_canvas = tk.Canvas(canvas_frame, bg='#0f3460', height=300)
        self.conversion_canvas.pack(fill='both', expand=True)
        
        # Conversion details
        details_frame = tk.Frame(parent, bg='#16213e')
        details_frame.pack(fill='x', padx=15, pady=10)
        
        self.conversion_details = tk.Text(details_frame, height=8, bg='#0f3460',
                                        fg='white', font=('Consolas', 9),
                                        wrap='word', state='disabled')
        self.conversion_details.pack(fill='x')
    
    def create_binary_packet_section(self, parent):
        """Create binary packet display section"""
        # Packet structure display
        struct_frame = tk.Frame(parent, bg='#16213e')
        struct_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(struct_frame, text="Packet Structure:", bg='#16213e', fg='white',
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        # Create field displays
        self.packet_fields = {}
        fields = [
            ("Start Byte", "start_byte", "0x{:02X}"),
            ("Length", "length", "{} bytes"),
            ("Checksum", "checksum", "0x{:02X}"),
            ("End Byte", "end_byte", "0x{:02X}")
        ]
        
        for label, attr, fmt in fields:
            field_frame = tk.Frame(struct_frame, bg='#0f3460')
            field_frame.pack(fill='x', pady=2)
            
            tk.Label(field_frame, text=f"{label}:", width=15, anchor='w',
                    bg='#0f3460', fg='#00d2d3', font=('Arial', 10)).pack(side='left', padx=10)
            
            value_label = tk.Label(field_frame, text=fmt.format(0), 
                                 bg='#0f3460', fg='white', font=('Consolas', 10))
            value_label.pack(side='left')
            
            self.packet_fields[attr] = (value_label, fmt)
        
        # Payload hex view
        tk.Label(struct_frame, text="Payload (Hex):", bg='#16213e', fg='white',
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        
        self.hex_display = tk.Text(struct_frame, height=4, bg='#0f3460',
                                 fg='#4a9eff', font=('Consolas', 9),
                                 wrap='word', state='disabled')
        self.hex_display.pack(fill='x', pady=5)
        
        # Binary packet actions
        action_frame = tk.Frame(parent, bg='#16213e')
        action_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Button(action_frame, text="Validate Packet",
                 command=self.validate_binary_packet,
                 bg='#2ed573', fg='white', font=('Arial', 10),
                 relief='flat', pady=5).pack(fill='x', pady=2)
        
        tk.Button(action_frame, text="Corrupt Checksum",
                 command=self.corrupt_packet,
                 bg='#ff6348', fg='white', font=('Arial', 10),
                 relief='flat', pady=5).pack(fill='x', pady=2)
        
        tk.Button(action_frame, text="Transmit Packet",
                 command=self.transmit_packet,
                 bg='#4a9eff', fg='white', font=('Arial', 10),
                 relief='flat', pady=5).pack(fill='x', pady=2)
    
    def create_history_section(self, parent):
        """Create transmission history section"""
        history_frame = tk.Frame(parent, bg='#16213e')
        history_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # History listbox with scrollbar
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_frame, bg='#0f3460', fg='white',
                                        font=('Consolas', 9), selectmode='single',
                                        yscrollcommand=scrollbar.set, height=5)
        self.history_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)
    
    def set_command(self, cmd):
        """Set command in entry field"""
        self.command_var.set(f"<{cmd}>")
        self.command_entry.focus()
    
    def process_text_command(self):
        """Process text command and convert to binary"""
        text_input = self.command_var.get().strip()
        
        # Validate text protocol
        valid, message = self.text_protocol.validate(text_input)
        
        if not valid:
            self.text_status_var.set(f"❌ {message}")
            return
        
        self.text_status_var.set(f"✓ {message}")
        
        # Extract command
        command = self.text_protocol.extract_command(text_input)
        
        # Convert to binary packet
        self.binary_packet.from_text_command(text_input)
        
        # Update displays
        self.update_packet_display()
        self.animate_conversion(text_input, command)
    
    def update_packet_display(self):
        """Update binary packet field displays"""
        # Update field values
        for attr, (label, fmt) in self.packet_fields.items():
            value = getattr(self.binary_packet, attr)
            label.config(text=fmt.format(value))
        
        # Update hex display
        self.hex_display.config(state='normal')
        self.hex_display.delete(1.0, tk.END)
        
        hex_str = ""
        for i in range(0, self.binary_packet.length, 8):
            hex_bytes = self.binary_packet.payload[i:min(i+8, self.binary_packet.length)]
            hex_str += " ".join([f"{b:02X}" for b in hex_bytes]) + "\n"
        
        self.hex_display.insert(1.0, hex_str.strip())
        self.hex_display.config(state='disabled')
    
    def animate_conversion(self, text_input, command):
        """Animate the conversion process"""
        self.conversion_canvas.delete("all")
        
        # Show conversion steps
        self.conversion_details.config(state='normal')
        self.conversion_details.delete(1.0, tk.END)
        
        details = f"""Conversion Process:
1. Text Input: {text_input}
2. Extract Command: {command}
3. Convert to Bytes: {command.encode('utf-8').hex()}
4. Calculate Length: {len(command)} bytes
5. Calculate Checksum: 0x{self.binary_packet.checksum:02X}
6. Build Binary Packet: {self.binary_packet.to_bytes().hex()}
"""
        self.conversion_details.insert(1.0, details)
        self.conversion_details.config(state='disabled')
        
        # Visual animation
        width = self.conversion_canvas.winfo_width()
        height = self.conversion_canvas.winfo_height()
        
        if width > 1:  # Canvas is rendered
            # Draw conversion arrow
            self.conversion_canvas.create_text(width//2, 50, text="Text → Binary",
                                             fill='#00d2d3', font=('Arial', 14, 'bold'))
            
            # Animate data flow
            y = 100
            steps = [
                f"Input: {text_input}",
                f"Command: {command}",
                f"Length: {self.binary_packet.length}",
                f"Checksum: 0x{self.binary_packet.checksum:02X}",
                "Packet Ready!"
            ]
            
            for i, step in enumerate(steps):
                self.conversion_canvas.create_text(width//2, y + i*30, text=step,
                                                 fill='white', font=('Consolas', 10))
    
    def validate_binary_packet(self):
        """Validate the binary packet"""
        valid, message = self.binary_packet.validate()
        
        if valid:
            messagebox.showinfo("Validation Result", f"✓ {message}")
        else:
            messagebox.showerror("Validation Failed", f"✗ {message}")
        
        # Add to history
        self.add_to_history(f"Validation: {message}", valid)
    
    def corrupt_packet(self):
        """Corrupt the packet checksum for testing"""
        self.binary_packet.checksum = (self.binary_packet.checksum + 1) & 0xFF
        self.update_packet_display()
        self.add_to_history("Packet corrupted (checksum modified)", False)
    
    def transmit_packet(self):
        """Simulate packet transmission"""
        if self.transmission_active:
            return
        
        self.transmission_active = True
        
        # Validate before transmission
        valid, status = self.binary_packet.validate()
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        packet_info = f"{timestamp} - TX: {self.command_var.get()} - Size: {self.binary_packet.length + 5}B - {status}"
        self.add_to_history(packet_info, valid)
        
        # Show success/failure message
        if valid:
            messagebox.showinfo("Transmission", "Packet transmitted successfully!")
        else:
            messagebox.showerror("Transmission Failed", f"Cannot transmit invalid packet: {status}")
        
        self.transmission_active = False
    
    def add_to_history(self, message, success=True):
        """Add entry to transmission history"""
        self.history_listbox.insert(0, message)
        
        # Color code based on success
        if success:
            self.history_listbox.itemconfig(0, fg='#2ed573')
        else:
            self.history_listbox.itemconfig(0, fg='#ff6348')
        
        # Limit history to 20 items
        if self.history_listbox.size() > 20:
            self.history_listbox.delete(20)

def main():
    app = DualProtocolVisualizer()
    
    # Add menu bar
    menubar = tk.Menu(app)
    app.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Clear History", 
                         command=lambda: app.history_listbox.delete(0, tk.END))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", 
                         command=lambda: messagebox.showinfo("About", 
                         "Arduino Dual-Protocol Network Parser\n\n"
                         "Demonstrates conversion between text-based\n"
                         "commands (<COMMAND>) and binary packet protocol\n\n"
                         "Perfect for Arduino serial communication!"))
    
    app.mainloop()

if __name__ == "__main__":
    main()