"""
Breath/Voice Controller for Flappy Bird
Uses microphone input to control the bird's movement
"""

import numpy as np
import sounddevice as sd
import threading
import time
from collections import deque

class BreathController:
    """
    Real-time microphone audio controller for game input.
    Measures audio volume and converts it to game actions.
    """

    def __init__(self, sample_rate=44100, chunk_duration=0.05, smoothing_window=5, debug=False):
        """
        Initialize the breath controller

        Args:
            sample_rate: Audio sample rate (Hz)
            chunk_duration: Duration of each audio chunk (seconds)
            smoothing_window: Number of samples to smooth over
            debug: Enable debug mode
        """
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration)

        # Smoothing buffer to reduce jitter
        self.smoothing_window = smoothing_window
        self.volume_buffer = deque(maxlen=smoothing_window)

        # Current volume level (0.0 to 1.0)
        self.current_volume = 0.0
        self.smoothed_volume = 0.0

        # Control thresholds
        self.threshold_jump = 0.35      # Volume > this = jump/fly up
        self.threshold_hover_min = 0.15  # Volume in this range = hover/maintain height
        self.threshold_hover_max = 0.35

        # Threading control
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        # Calibration
        self.noise_floor = 0.0
        self.max_volume_seen = 0.0

        # Debug mode
        self.debug = debug

    def calibrate(self, duration=2.0):
        """
        Calibrate by measuring ambient noise for a few seconds

        Args:
            duration: Calibration duration in seconds
        """
        print("🎤 Calibrating microphone... Stay quiet for 2 seconds...")

        noise_samples = []
        def callback(indata, frames, time_info, status):
            if status:
                print(f"Status: {status}")
            # Calculate RMS volume
            volume = np.sqrt(np.mean(indata**2))
            noise_samples.append(volume)

        # Record noise floor
        with sd.InputStream(callback=callback, channels=1,
                           samplerate=self.sample_rate,
                           blocksize=self.chunk_size):
            time.sleep(duration)

        # Set noise floor to 90th percentile of ambient noise
        if noise_samples:
            self.noise_floor = np.percentile(noise_samples, 90)
            print(f"✅ Calibration complete! Noise floor: {self.noise_floor:.4f}")
        else:
            self.noise_floor = 0.01
            print("⚠️  Calibration failed, using default noise floor")

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function for audio stream"""
        if status:
            if self.debug:
                print(f"Audio status: {status}")

        # Calculate RMS (Root Mean Square) volume
        rms = np.sqrt(np.mean(indata**2))

        # Subtract noise floor and normalize
        volume = max(0.0, rms - self.noise_floor)

        # Track max volume for auto-scaling
        self.max_volume_seen = max(self.max_volume_seen, volume)

        # Normalize to 0-1 range
        if self.max_volume_seen > 0:
            volume = min(1.0, volume / (self.max_volume_seen * 1.5))

        # Update current volume
        with self.lock:
            self.current_volume = volume
            self.volume_buffer.append(volume)

            # Calculate smoothed volume (moving average)
            if len(self.volume_buffer) > 0:
                self.smoothed_volume = np.mean(self.volume_buffer)

    def start(self):
        """Start listening to microphone in background thread"""
        if self.running:
            print("⚠️  Controller already running!")
            return

        print("🎤 Starting microphone input...")
        self.running = True

        # Start audio stream
        try:
            self.stream = sd.InputStream(
                callback=self._audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size
            )
            self.stream.start()
            print("✅ Microphone active! Speak or blow to control the bird.")
        except Exception as e:
            print(f"❌ Failed to start microphone: {e}")
            print("💡 Make sure your microphone is connected and permissions are granted.")
            self.running = False

    def stop(self):
        """Stop listening to microphone"""
        if not self.running:
            return

        print("🛑 Stopping microphone input...")
        self.running = False

        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()

        print("✅ Microphone stopped.")

    def get_volume(self, smoothed=True):
        """
        Get current volume level

        Args:
            smoothed: If True, return smoothed volume; otherwise raw volume

        Returns:
            Volume level between 0.0 and 1.0
        """
        with self.lock:
            return self.smoothed_volume if smoothed else self.current_volume

    def should_jump(self):
        """
        Determine if bird should jump based on current volume

        Returns:
            True if volume exceeds jump threshold
        """
        volume = self.get_volume(smoothed=True)
        return volume >= self.threshold_jump

    def should_hover(self):
        """
        Determine if bird should hover (maintain altitude)

        Returns:
            True if volume is in hover range
        """
        volume = self.get_volume(smoothed=True)
        return self.threshold_hover_min <= volume < self.threshold_hover_max

    def get_action(self):
        """
        Get current action based on volume level

        Returns:
            String: 'jump', 'hover', or 'fall'
        """
        volume = self.get_volume(smoothed=True)

        if volume >= self.threshold_jump:
            return 'jump'
        elif self.threshold_hover_min <= volume < self.threshold_hover_max:
            return 'hover'
        else:
            return 'fall'

    def get_debug_info(self):
        """Get debug information"""
        volume = self.get_volume(smoothed=True)
        raw_volume = self.get_volume(smoothed=False)
        action = self.get_action()

        return {
            'volume': volume,
            'raw_volume': raw_volume,
            'action': action,
            'noise_floor': self.noise_floor,
            'max_seen': self.max_volume_seen,
            'buffer_size': len(self.volume_buffer)
        }

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


# Test function
if __name__ == "__main__":
    print("🎮 Testing Breath Controller")
    print("=" * 50)

    controller = BreathController(debug=True)
    controller.calibrate(duration=2.0)
    controller.start()

    print("\n🎤 Speak, blow, or make noise to test!")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            info = controller.get_debug_info()

            # Create visual volume bar
            bar_length = 30
            filled = int(info['volume'] * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\rVolume: [{bar}] {info['volume']:.2f} | Action: {info['action']:6s}", end='', flush=True)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping test...")
        controller.stop()
        print("✅ Test complete!")
