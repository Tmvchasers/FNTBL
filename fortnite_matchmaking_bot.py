"""
Fortnite Matchmaking Bot GUI Application
A CustomTkinter-based desktop application for managing a Fortnite bot account.
Allows users to control bot login, party joining, and matchmaking detection.
"""

import customtkinter as ctk
import threading
import queue
import logging
from datetime import datetime
from typing import Optional, Callable
import traceback

# Fortnite bot imports (fortnitepy)
try:
    import fortnitepy
    from fortnitepy.ext import commands
except ImportError:
    print("ERROR: fortnitepy not installed. Install with: pip install fortnitepy")
    fortnitepy = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FortniteBot:
    """Handles Fortnite bot logic using fortnitepy"""
    
    def __init__(self, log_callback: Callable[[str], None]):
        """
        Initialize the Fortnite bot.
        
        Args:
            log_callback: Function to call for logging messages to GUI
        """
        self.client = None
        self.log_callback = log_callback
        self.running = False
        self.in_party = False
        self.matchmaking_mode = None
        
    def log(self, message: str):
        """Log a message to both console and GUI callback"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        logger.info(message)
        if self.log_callback:
            self.log_callback(formatted_msg)
    
    async def login(self, account_id: str, device_id: str, secret_key: str) -> bool:
        """
        Authenticate with Epic Games and initialize the bot.
        
        Args:
            account_id: The bot's account ID
            device_id: Device ID for authentication
            secret_key: Secret key for authentication
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            if fortnitepy is None:
                self.log("ERROR: fortnitepy not installed")
                return False
            
            self.log("Initializing Fortnite bot client...")
            
            # Create the bot client with launcher credentials
            self.client = fortnitepy.Client(
                email=account_id,
                password=secret_key,
                launcher_token=device_id,
            )
            
            # Register event handlers
            self.client.event(self.on_ready)
            self.client.event(self.on_friend_request)
            self.client.event(self.on_party_invite)
            self.client.event(self.on_party_member_join)
            self.client.event(self.on_matchmaking_found)
            self.client.event(self.on_party_member_update)
            
            self.log("Connecting to Epic Games servers...")
            await self.client.connect()
            self.running = True
            self.log("Bot connected successfully!")
            return True
            
        except Exception as e:
            self.log(f"Login failed: {str(e)}")
            logger.error(f"Login exception: {traceback.format_exc()}")
            return False
    
    async def on_ready(self):
        """Called when bot is ready and logged in"""
        self.log(f"Bot Online as {self.client.user.display_name}")
        self.log("Waiting for party invites...")
    
    async def on_friend_request(self, request):
        """Automatically accept friend requests"""
        try:
            await request.accept()
            self.log(f"Accepted friend request from {request.user.display_name}")
        except Exception as e:
            self.log(f"Failed to accept friend request: {str(e)}")
    
    async def on_party_invite(self, invite):
        """Automatically accept party invites"""
        try:
            await invite.accept()
            self.log(f"Joined party from {invite.sender.display_name}")
            self.in_party = True
        except Exception as e:
            self.log(f"Failed to accept party invite: {str(e)}")
    
    async def on_party_member_join(self, member):
        """Handle when party members join"""
        try:
            if member.id != self.client.user.id:
                self.log(f"Party member joined: {member.display_name}")
        except Exception as e:
            self.log(f"Error in member join handler: {str(e)}")
    
    async def on_matchmaking_found(self, party, match_found):
        """Called when matchmaking is found - bot leaves for unranked modes"""
        try:
            # Get the playlist info
            playlist_name = party.matchmaking_playlist or "Unknown"
            self.log(f"Matchmaking found: {playlist_name}")
            
            # Check if it's an unsupported mode (Ranked or Reload)
            if any(mode in str(playlist_name).lower() for mode in ['ranked', 'reload']):
                self.log("Mode not supported - leaving party")
                try:
                    await self.client.user.party.send_chat_message(
                        "Mode not supported"
                    )
                except:
                    pass
                await self.client.user.party.leave()
                self.in_party = False
            else:
                # For unranked modes (BR, Zero Build, OG), leave to stay level 1
                self.log("Unranked mode detected - leaving party to maintain Level 1")
                await self.client.user.party.leave()
                self.in_party = False
                
        except Exception as e:
            self.log(f"Error handling matchmaking: {str(e)}")
    
    async def on_party_member_update(self, member, updated, updated_members):
        """Monitor party member updates for gameplay status changes"""
        try:
            if member.id == self.client.user.id:
                # Check if we're leaving the party ourselves
                if 'member_revision' in updated:
                    pass
        except Exception as e:
            logger.debug(f"Party member update error: {str(e)}")
    
    async def disconnect(self):
        """Cleanly disconnect the bot from Epic Games servers"""
        try:
            if self.client and self.client.is_connected():
                self.log("Disconnecting bot...")
                
                # Leave party if in one
                if self.client.user and self.client.user.party:
                    try:
                        await self.client.user.party.leave()
                        self.log("Left party")
                    except:
                        pass
                
                # Close the client connection
                await self.client.close()
                self.log("Bot disconnected")
            
            self.running = False
            self.in_party = False
            
        except Exception as e:
            self.log(f"Error during disconnect: {str(e)}")
            self.running = False


class FortniteGUI:
    """Main GUI application class using CustomTkinter"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Fortnite Matchmaking Bot")
        self.root.geometry("700x850")
        self.root.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # State variables
        self.bot = FortniteBot(self.add_log)
        self.bot_thread: Optional[threading.Thread] = None
        self.message_queue: queue.Queue = queue.Queue()
        self.bot_running = False
        
        # Setup UI
        self.setup_ui()
        
        # Start message queue processor
        self.process_queue()
    
    def setup_ui(self):
        """Setup the main GUI components"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Fortnite Matchmaking Bot",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Credentials Frame
        creds_frame = ctk.CTkFrame(main_frame)
        creds_frame.pack(fill="x", pady=10)
        
        creds_title = ctk.CTkLabel(
            creds_frame,
            text="Bot Credentials",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        creds_title.pack(pady=5)
        
        # Account ID
        ctk.CTkLabel(creds_frame, text="Account ID:").pack(anchor="w", padx=10, pady=(5, 0))
        self.account_id_entry = ctk.CTkEntry(
            creds_frame,
            placeholder_text="Paste your bot account ID"
        )
        self.account_id_entry.pack(fill="x", padx=10, pady=(0, 5))
        
        # Device ID
        ctk.CTkLabel(creds_frame, text="Device ID:").pack(anchor="w", padx=10, pady=(5, 0))
        self.device_id_entry = ctk.CTkEntry(
            creds_frame,
            placeholder_text="Paste your device ID"
        )
        self.device_id_entry.pack(fill="x", padx=10, pady=(0, 5))
        
        # Secret Key
        ctk.CTkLabel(creds_frame, text="Secret Key:").pack(anchor="w", padx=10, pady=(5, 0))
        self.secret_key_entry = ctk.CTkEntry(
            creds_frame,
            placeholder_text="Paste your secret key",
            show="*"
        )
        self.secret_key_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Control Button Frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Start/Stop Toggle Button
        self.toggle_button = ctk.CTkButton(
            button_frame,
            text="START BOT",
            command=self.toggle_bot,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        self.toggle_button.pack(fill="x", padx=10, pady=5)
        self.update_button_state()
        
        # Status Indicator
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(status_frame, text="Status:").pack(side="left", padx=5)
        
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color="#808080"
        )
        self.status_indicator.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Bot Offline",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=5)
        
        # Log Console
        log_label = ctk.CTkLabel(
            main_frame,
            text="Bot Console Log",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        log_label.pack(anchor="w", padx=10, pady=(15, 5))
        
        # Log text box with scrollbar
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(size=10, family="Courier"),
            state="disabled"
        )
        self.log_textbox.pack(fill="both", expand=True)
        
        # Clear log button
        clear_button = ctk.CTkButton(
            main_frame,
            text="Clear Log",
            command=self.clear_log,
            width=100
        )
        clear_button.pack(pady=5)
    
    def toggle_bot(self):
        """Toggle bot on/off"""
        if self.bot_running:
            self.stop_bot()
        else:
            self.start_bot()
    
    def start_bot(self):
        """Start the bot in a background thread"""
        # Validate inputs
        account_id = self.account_id_entry.get().strip()
        device_id = self.device_id_entry.get().strip()
        secret_key = self.secret_key_entry.get().strip()
        
        if not all([account_id, device_id, secret_key]):
            self.add_log("ERROR: Please fill in all credential fields")
            return
        
        # Disable inputs during bot run
        self.account_id_entry.configure(state="disabled")
        self.device_id_entry.configure(state="disabled")
        self.secret_key_entry.configure(state="disabled")
        
        self.bot_running = True
        self.update_button_state()
        
        # Start bot in background thread
        self.bot_thread = threading.Thread(
            target=self.run_bot_async,
            args=(account_id, device_id, secret_key),
            daemon=True
        )
        self.bot_thread.start()
        self.add_log("Starting bot...")
    
    def run_bot_async(self, account_id: str, device_id: str, secret_key: str):
        """Run the bot's async event loop in a separate thread"""
        try:
            import asyncio
            
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Connect and run
            success = loop.run_until_complete(
                self.bot.login(account_id, device_id, secret_key)
            )
            
            if success:
                self.message_queue.put(("status", "online"))
                # Keep the event loop running
                loop.run_until_complete(self.keep_alive(loop))
            else:
                self.message_queue.put(("status", "offline"))
                self.bot_running = False
                
        except Exception as e:
            self.add_log(f"Bot thread error: {str(e)}")
            logger.error(f"Bot thread exception: {traceback.format_exc()}")
            self.message_queue.put(("status", "offline"))
            self.bot_running = False
    
    async def keep_alive(self, loop):
        """Keep the event loop alive while bot is running"""
        try:
            while self.bot_running and self.bot.client and self.bot.client.is_connected():
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Keep alive error: {str(e)}")
    
    def stop_bot(self):
        """Stop the bot gracefully"""
        self.bot_running = False
        self.add_log("Stopping bot...")
        
        # Disconnect bot
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.disconnect())
        except Exception as e:
            self.add_log(f"Error stopping bot: {str(e)}")
        
        # Wait for thread to finish
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join(timeout=5)
        
        # Re-enable inputs
        self.account_id_entry.configure(state="normal")
        self.device_id_entry.configure(state="normal")
        self.secret_key_entry.configure(state="normal")
        
        self.update_button_state()
        self.message_queue.put(("status", "offline"))
        self.add_log("Bot stopped")
    
    def add_log(self, message: str):
        """Add a message to the log console (thread-safe)"""
        self.message_queue.put(("log", message))
    
    def process_queue(self):
        """Process messages from the bot thread"""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    self.log_textbox.configure(state="normal")
                    self.log_textbox.insert("end", content + "\n")
                    self.log_textbox.see("end")  # Auto-scroll
                    self.log_textbox.configure(state="disabled")
                    
                elif msg_type == "status":
                    if content == "online":
                        self.status_indicator.configure(text_color="#00FF00")
                        self.status_label.configure(text="Bot Online")
                    else:
                        self.status_indicator.configure(text_color="#808080")
                        self.status_label.configure(text="Bot Offline")
                        
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)
    
    def update_button_state(self):
        """Update button appearance based on bot state"""
        if self.bot_running:
            self.toggle_button.configure(
                text="STOP BOT",
                fg_color="#FF4444"
            )
        else:
            self.toggle_button.configure(
                text="START BOT",
                fg_color="#44AA44"
            )
    
    def clear_log(self):
        """Clear the log console"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")


def main():
    """Main entry point"""
    root = ctk.CTk()
    app = FortniteGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
