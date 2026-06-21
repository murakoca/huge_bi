import random

def detect_emotion():
    """Rastgele duygu döndürür (simülasyon). Gerçekte OpenCV + DeepFace kullanılabilir."""
    emotions = ['happy', 'surprised', 'neutral', 'confused']
    return random.choice(emotions)