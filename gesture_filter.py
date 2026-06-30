import time

class GestureFilter:

    HOLD_TIME = 2.0 
    STABLE_THRESHOLD = 3
    LOST_THRESHOLD = 7
    MIN_CONFIDENCE = 0.5

    def __init__(self):
        self.current = None
        self.candidate = None
        self.stable = 0
        self.last_seen = 0
        self.lost = 0

    def update(self, prediction, confidence):

        now = time.time()

        # Valid prediction
        if confidence >= self.MIN_CONFIDENCE:

            self.current = prediction
            self.last_seen = now
            return self.current

        # Lost tracking / low confidence
        if self.current is not None:

            if now - self.last_seen < self.HOLD_TIME:
                return self.current

        # Lost for too long
        self.current = None
        return None

        # Ignore uncertain predictions
        if confidence < self.MIN_CONFIDENCE:
            prediction = None

        # No reliable prediction
        if prediction is None:
            self.lost += 1

            if self.lost >= self.LOST_THRESHOLD:
                self.current = None

            return self.current

        self.lost = 0

        # Same as current
        if prediction == self.current:
            self.candidate = None
            self.stable = 0
            return self.current

        # New candidate
        if prediction != self.candidate:
            self.candidate = prediction
            self.stable = 1
            return self.current

        # Candidate survived another frame
        self.stable += 1

        if self.stable >= self.STABLE_THRESHOLD:
            self.current = self.candidate
            self.candidate = None
            self.stable = 0

        return self.current