# niblit_voice.py - TTS/STT wrappers
try:
    from plyer import tts
    PLYER_AVAILABLE = True
except Exception:
    PLYER_AVAILABLE = False

class NiblitVoice:
    def __init__(self):
        print('[Niblit Voice] initialized (plyer:' + str(PLYER_AVAILABLE) + ')')

    def speak(self, text):
        try:
            if PLYER_AVAILABLE:
                tts.speak(text)
                return True
        except Exception as e:
            print('[Niblit Voice] TTS error:', e)
        return False

    def listen(self, timeout=5):
        print('[Niblit Voice] listen() placeholder; integrate Android speech intent for STT.')
        return ''