from app.models.member import Member

class SampleState:

    _current_sample = None

    @classmethod
    def set_sample(cls, sample: Member):
        print(f"Setting current sample: {sample}")
        cls._current_sample = sample

    @classmethod
    def get_sample(cls):
        if cls._current_sample is None:
            raise ValueError("No sample has been set.")
        return cls._current_sample
    
    @classmethod
    def clear_sample(cls):
        cls._current_sample = None