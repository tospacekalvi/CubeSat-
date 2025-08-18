# mq02.py

from machine import ADC, Pin
import sys

class MQ02:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        
        # Check if running on ESP32
        if hasattr(self.adc, "atten"):
            try:
                self.adc.atten(ADC.ATTN_11DB)  # Set full voltage range (0–3.3V)
            except:
                pass  # Just in case attenuation is unsupported

    def read_raw(self):
        # Return raw ADC value depending on board
        if hasattr(self.adc, "read_u16"):  # Pico-style
            return self.adc.read_u16()
        else:  # ESP32-style
            return self.adc.read()

    def read_scaled(self):
        if hasattr(self.adc, "read_u16"):  # Pico
            return self.adc.read_u16() / 65535
        else:  # ESP32
            return self.adc.read() / 4095

    def get_status(self, threshold=30000):  # Threshold adjusted for Pico
        value = self.read_raw()
        if value > threshold:
            return "⚠️ Smoke/Gas Detected"
        else:
            return "✅ Air is Clean"
