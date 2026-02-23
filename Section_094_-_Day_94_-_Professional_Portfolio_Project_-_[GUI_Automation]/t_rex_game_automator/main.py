# =================================IMPORTS====================================

# Import the time module for timestamp tracking and sleep/delay functionality
import time
# Import threading module to run automation loop separately from GUI and listener
import threading
# Import pyautogui to simulate keyboard presses (spacebar) for jumping
import pyautogui
# Import ImageGrab from PIL to capture screenshots of specific screen regions
from PIL import ImageGrab
# Import mouse from pynput to detect and track mouse click events globally
from pynput import mouse
# Import tkinter as tk to create the monitoring panel GUI window
import tkinter as tk


# ===========================GLOBAL SHARED STATE===============================

# Variable to store the X coordinate where obstacles appear (set via triple-click)
# Initialized as None, meaning not calibrated yet
obstacle_position_x = None

# Variable to store the Y coordinate where obstacles appear (set via triple-click)
# Initialized as None, meaning not calibrated yet
obstacle_position_y = None

# Variable to store the baseline brightness of the detection region
# This is the reference brightness when no obstacle is present
baseline_brightness = None

# Flag to control whether automation should continue running
# Set to True initially, becomes False on shutdown
automation_running = True

# Variable to store the timestamp when the game actually starts (first space press)
# Used for runtime calculation in the monitoring panel
start_time = None

# Thread lock to safely access/modify coordinate variables across threads
# Prevents race conditions when updating and reading obstacle positions
coordinate_lock = threading.Lock()

# Width (in pixels) of the horizontal scan region in front of the dinosaur
# Larger values detect obstacles earlier but may include more noise
horizontal_scan_width = 80

# Half-height (in pixels) of the vertical scan region centered on the Y coordinate
# Total height = 2 * vertical_scan_half_height
vertical_scan_half_height = 20

# Threshold for brightness change that indicates an obstacle
# If brightness delta exceeds this value, trigger a jump
# Higher values = less sensitive, Lower values = more sensitive
brightness_change_threshold = 25


# =============================MONITORING PANEL================================

# Class representing the GUI panel that shows status, coordinates, and runtime
# This panel stays on top of other windows for easy monitoring
class MonitoringPanel:

    # Constructor method that initializes the monitoring panel window
    def __init__(self):

        # Create the main tkinter window object
        self.root = tk.Tk()
        # Set the window title that appears in the title bar
        self.root.title("T-Rex Automation Monitor")
        # Disable window resizing to maintain fixed layout
        self.root.resizable(False, False)
        # Set background color to dark gray (#1e1e1e) for better visual contrast
        self.root.configure(bg="#1e1e1e")

        # Set the window to always stay on top of other windows
        # This ensures the panel is always visible while gaming
        self.root.attributes("-topmost", True)

        # Define fixed width of the monitoring panel in pixels
        window_width = 420
        # Define fixed height of the monitoring panel in pixels
        window_height = 190

        # Get the width of the primary monitor screen
        screen_width = self.root.winfo_screenwidth()
        # Calculate X position to center the window horizontally
        position_x = int((screen_width - window_width) / 2)
        # Set Y position to 40 pixels from top of screen (near top)
        position_y = 40

        # Set window geometry: width x height + X_position + Y_position
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Call method to periodically reinforce topmost status
        # This ensures window stays on top despite other applications
        self._reinforce_topmost()

        # Create a label widget for displaying status messages
        self.status_label = tk.Label(
            self.root,                       # Parent container
            text="Waiting for calibration...", # Initial text
            fg="white",                       # Foreground (text) color
            bg="#1e1e1e",                     # Background color matching window
            font=("Segoe UI", 11)              # Font family and size
        )
        # Pack the label into window with 5px vertical padding
        self.status_label.pack(pady=5)

        # Create a label widget for displaying current obstacle coordinates
        self.coordinate_label = tk.Label(
            self.root,
            text="Coordinate: Not Set",       # Initial text
            fg="#4fc3f7",                     # Light blue text color
            bg="#1e1e1e",
            font=("Segoe UI", 11, "bold")      # Bold font for emphasis
        )
        self.coordinate_label.pack()

        # Create a label widget for displaying elapsed runtime
        self.runtime_label = tk.Label(
            self.root,
            text="Runtime: 0s",                # Initial runtime display
            fg="#ffb74d",                       # Orange text color
            bg="#1e1e1e",
            font=("Segoe UI", 10)
        )
        self.runtime_label.pack(pady=5)

        # Create a label widget for displaying instruction information
        self.info_label = tk.Label(
            self.root,
            text="Triple-click anywhere to recalibrate.", # Instruction text
            fg="#cccccc",                                   # Light gray text
            bg="#1e1e1e",
            font=("Segoe UI", 9)                            # Smaller font size
        )
        self.info_label.pack()

        # Set up protocol handler for window close button (X)
        # When window is closed, call the shutdown method
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

    # Method to periodically reinforce that window stays on top
    # Called every 2 seconds to override any other apps stealing focus
    def _reinforce_topmost(self):
        # Set window to always stay on top of other windows
        self.root.attributes("-topmost", True)
        # Schedule this method to run again after 2000ms (2 seconds)
        self.root.after(2000, self._reinforce_topmost)

    # Method to update the status label with a new message
    # Parameters: message - string to display in status label
    def update_status(self, message: str):
        self.status_label.config(text=message)

    # Method to update the coordinate label with new X,Y values
    # Parameters: x_value, y_value - integers representing screen coordinates
    def update_coordinate(self, x_value: int, y_value: int):
        self.coordinate_label.config(text=f"Coordinate: ({x_value}, {y_value})")

    # Method to update the runtime label based on elapsed time
    # Called every second to refresh the display
    def update_runtime(self):
        # Check if start_time has been set (game started)
        if start_time is not None:
            # Calculate elapsed seconds since game start
            elapsed = int(time.time() - start_time)
            # Update runtime label text
            self.runtime_label.config(text=f"Runtime: {elapsed}s")

        # If automation is still running, schedule another update in 1 second
        if automation_running:
            self.root.after(1000, self.update_runtime)

    # Method to handle clean shutdown when window is closed
    # Sets flags, stops threads, and destroys window
    def shutdown(self):
        # Access the global automation_running flag
        global automation_running
        # Set flag to False to stop automation loop
        automation_running = False

        # Try to stop the mouse listener thread
        try:
            # Stop listening for mouse events
            mouse_listener.stop()
        except:
            # Ignore any errors if listener is already stopped
            pass

        # Destroy the tkinter window (close it)
        self.root.destroy()

    # Method to start the GUI main loop and periodic updates
    def start(self):
        # Start the runtime update scheduler
        self.update_runtime()
        # Start tkinter main event loop (keeps window open and responsive)
        self.root.mainloop()


# ============================BRIGHTNESS HELPER================================

# Function to capture a screen region and calculate its average brightness
# Parameters: x, y - screen coordinates (center point of detection region)
# Returns: average brightness value (0-255) of the captured region
def capture_average_brightness(x, y):
    """
    Captures region in front of dinosaur and returns average brightness.
    """

    # Define the rectangle region to capture
    # Left: x (starting from obstacle position)
    # Top: y - vertical_scan_half_height (above the Y coordinate)
    # Right: x + horizontal_scan_width (scanning forward)
    # Bottom: y + vertical_scan_half_height (below the Y coordinate)
    detection_region = (
        x,                                    # left
        y - vertical_scan_half_height,        # top
        x + horizontal_scan_width,             # right
        y + vertical_scan_half_height          # bottom
    )

    # Capture screenshot of the specified region
    captured_image = ImageGrab.grab(bbox=detection_region)
    # Convert the captured image to grayscale (L mode = 8-bit grayscale)
    grayscale_image = captured_image.convert("L")

    # Get all pixel brightness values as a flat list
    pixel_values = list(grayscale_image.getdata())

    # Calculate and return the average brightness
    # Sum all pixel values and divide by number of pixels
    return sum(pixel_values) / len(pixel_values)


# =============================TRIPLE CLICK DETECTOR===========================

# Class to detect triple-click events for recalibration
# Monitors mouse clicks and identifies when three quick clicks occur in same area
class TripleClickDetector:

    # Constructor method to initialize the detector
    # Parameters: 
    #   panel - reference to monitoring panel for updates
    #   max_interval_seconds - max time between clicks (0.5 seconds)
    #   max_position_delta_pixels - max movement between clicks (5 pixels)
    def __init__(self,
                 panel: MonitoringPanel,
                 max_interval_seconds: float = 0.5,
                 max_position_delta_pixels: int = 5):

        # Store reference to monitoring panel for UI updates
        self.panel = panel
        # Store max allowed time between clicks (in seconds)
        self.max_interval_seconds = max_interval_seconds
        # Store max allowed pixel movement between clicks
        self.max_position_delta_pixels = max_position_delta_pixels
        # Initialize empty list to store recent click events
        # Each element: (timestamp, (x_position, y_position))
        self.click_events = []

    # Method called by pynput listener when mouse click occurs
    # Parameters:
    #   x, y - screen coordinates of click
    #   button - which mouse button was clicked
    #   pressed - True for press, False for release
    def on_click(self, x: int, y: int, button, pressed: bool):

        # Declare intent to modify global variables
        global obstacle_position_x
        global obstacle_position_y
        global baseline_brightness

        # Only process mouse press events (ignore releases)
        if not pressed:
            return

        # Get current timestamp in seconds since epoch
        current_timestamp = time.time()

        # Filter out click events older than max_interval_seconds
        # This maintains only recent clicks in the list
        self.click_events = [
            (timestamp, position)                # Keep each event
            for timestamp, position in self.click_events  # Iterate through stored events
            if current_timestamp - timestamp <= self.max_interval_seconds  # Condition: recent enough
        ]

        # Add the current click event to the list
        self.click_events.append((current_timestamp, (x, y)))

        # Check if we now have 3 clicks stored (potential triple-click)
        if len(self.click_events) == 3:
            # Verify that all 3 clicks are close together spatially
            if self._is_spatially_clustered():

                # Acquire lock before modifying shared coordinates
                with coordinate_lock:
                    # Set global obstacle X coordinate
                    obstacle_position_x = x
                    # Set global obstacle Y coordinate
                    obstacle_position_y = y

                # Immediately capture baseline brightness at new coordinates
                baseline_brightness = capture_average_brightness(x, y)

                # Update monitoring panel with new coordinates
                self.panel.update_coordinate(x, y)
                # Update status message to indicate monitoring is active
                self.panel.update_status("Monitoring Active")

                # Print confirmation to console for debugging
                print(f"Coordinate updated to ({x}, {y})")
                print(f"Baseline brightness set to {baseline_brightness}")

                # Clear click events to prepare for next triple-click detection
                self.click_events.clear()

    # Private method to check if stored clicks are spatially clustered
    # Returns: True if all clicks within max_position_delta_pixels, False otherwise
    def _is_spatially_clustered(self) -> bool:

        # Extract all X coordinates from click events
        x_values = [pos[0] for _, pos in self.click_events]
        # Extract all Y coordinates from click events
        y_values = [pos[1] for _, pos in self.click_events]

        # Check if X coordinate range is within allowed delta
        # AND Y coordinate range is within allowed delta
        return (
            max(x_values) - min(x_values) <= self.max_position_delta_pixels and
            max(y_values) - min(y_values) <= self.max_position_delta_pixels
        )


# =============================AUTOMATION LOOP=================================

# Main automation function running in separate thread
# Continuously monitors brightness and triggers jumps
# Parameters: panel - reference to monitoring panel for status updates
def automation_loop(panel: MonitoringPanel):

    # Declare intent to modify global variables
    global automation_running
    global start_time
    global baseline_brightness

    # Wait for calibration to complete (obstacle_position_x not None)
    # Loop until coordinates are set or automation stops
    while obstacle_position_x is None and automation_running:
        # Sleep briefly to prevent CPU hogging
        time.sleep(0.01)

    # Exit if automation was stopped during calibration wait
    if not automation_running:
        return

    # Press spacebar to start the game
    pyautogui.press("space")
    # Record the start time for runtime tracking
    start_time = time.time()
    # Update panel status to indicate game has started
    panel.update_status("Game Started")

    # Main monitoring loop - runs until automation_running becomes False
    while automation_running:

        # Safely copy coordinates with lock to prevent race conditions
        with coordinate_lock:
            current_x = obstacle_position_x
            current_y = obstacle_position_y

        # Skip loop iteration if coordinates not set (shouldn't happen here)
        # or baseline brightness not captured
        if current_x is None or baseline_brightness is None:
            continue

        # Capture current brightness at detection region
        current_brightness = capture_average_brightness(current_x, current_y)

        # Calculate absolute difference from baseline
        brightness_delta = abs(current_brightness - baseline_brightness)

        # If brightness change exceeds threshold, obstacle detected
        if brightness_delta > brightness_change_threshold:
            # Press spacebar to jump over obstacle
            pyautogui.press("space")

            # Reset baseline to current brightness after jumping
            # This prevents repeated triggers from the same obstacle
            baseline_brightness = current_brightness


# =============================MAIN EXECUTION==================================

# Standard Python idiom to ensure code runs only when script is executed directly
# (not when imported as a module)
if __name__ == "__main__":

    # Create an instance of the monitoring panel
    monitoring_panel = MonitoringPanel()

    # Create an instance of the triple-click detector, passing panel reference
    detector = TripleClickDetector(panel=monitoring_panel)

    # Declare mouse_listener as global so shutdown method can access it
    global mouse_listener
    # Create and start mouse listener thread with on_click callback
    mouse_listener = mouse.Listener(on_click=detector.on_click)
    mouse_listener.start()

    # Create and start automation thread
    # Target function: automation_loop
    # Arguments: monitoring_panel (as tuple with comma for single argument)
    # daemon=True means thread exits when main program exits
    automation_thread = threading.Thread(
        target=automation_loop,
        args=(monitoring_panel,),
        daemon=True
    )
    automation_thread.start()

    # Start the monitoring panel GUI (blocks until window closed)
    monitoring_panel.start()