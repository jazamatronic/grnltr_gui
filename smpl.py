"""

from smpl import smpl
s = smpl()
s.set_input_file('/data/csound_jja/Toms_diner.wav')
s.set_bpm(s.estimate_bpm() / 2)
s.set_bars(s.estimate_bars())
s.set_export_filename('1.wav')
s.export_wav()
s.sample_info()

"""

# TODO: add bpm/bar estimation buttons/text entry fields
#       make adjustable start/stop points for the sample
class smpl:
    import sox
    import math
    import librosa
    import os
    import sounddevice as sd
    def __init__(self):
        self.export_rate = 48000
        self.export_channels = 1
        self.export_bitdepth = 16
        self.size_estimate = 0
        self.bpm = 0
        self.num_bars = 0
        self.start = 0
        self.end = 0
        self.loop = False

    def input_file_is_set(self):
        return hasattr(self, 'input_filename')

    def set_input_file(self, filename):
        self.input_filename = filename
        self.input_rate = self.sox.file_info.sample_rate(self.input_filename)
        self.input_channels = self.sox.file_info.channels(self.input_filename)
        self.input_bitdepth = self.sox.file_info.bitdepth(self.input_filename)
        self.input_duration = self.sox.file_info.duration(self.input_filename)
        self.size_estimate = self.math.ceil(self.input_duration * self.export_rate * (self.export_bitdepth / 8)) 
        self.num_samples = self.math.ceil(self.input_duration * self.export_rate)
        self.set_start(0)
        self.set_end(self.num_samples)
        if hasattr(self, 'wf_array'):
            del self.wf_array
        self.tfm = self.sox.Transformer()
        self.tfm.set_output_format(file_type='wav', rate=self.export_rate, channels=self.export_channels, bits=self.export_bitdepth, encoding='signed-integer')

    def set_export_filename(self, filename):
        self.export_filename = filename

    # TODO: make this play the transformed version destined for output
    #       make this play a selected range - probably from an array or something
    #       loopability
    def preview(self):
        if self.input_file_is_set():
            self.sd.play(self.get_waveform()[self.start:self.end], self.export_rate, loop=self.loop)

    def stop(self):
        self.sd.stop()

    def get_waveform(self):
        if not hasattr(self, 'wf_array'):
            self.wf_array = self.tfm.build_array(self.input_filename)
        return self.wf_array

    def export_wav(self):
        if hasattr(self, 'export_filename'):
            return self.tfm.build_file(self.input_filename, self.export_filename, return_output=True)
        else: 
            print('Export filename not defined - please set_export_filename')

    def estimate_bpm(self):
        if self.input_file_is_set():
            y, sr = self.librosa.load(self.input_filename)
            tempo, beat_frames = self.librosa.beat.beat_track(y=y, sr=sr)
            return tempo
        else:
            return 0

    def set_bpm(self, bpm):
        self.bpm = bpm

    def estimate_bars(self):
        if (self.bpm != 0):
            beats_per_second = self.bpm / 60
            seconds_per_bar = 4 / beats_per_second 
            num_bars = self.input_duration / seconds_per_bar
            return num_bars

    def set_bars(self, bars):
        self.num_bars = bars

    def sample_info(self):
        if hasattr(self, 'export_filename'):
            return "{},{},{:.2f},{:.2f},{}".format(self.os.path.basename(self.export_filename), self.os.path.basename(self.input_filename), self.bpm, self.num_bars, self.size_estimate)
        else: 
            print('Export filename not defined - please set_export_filename')

    def set_start(self, start):
        start = self.math.floor(start)
        if (start < 0):
            start = 0
        if (start > self.num_samples):
            start = self.num_samples 
        self.start = start

    def set_end(self, end):
        end = self.math.ceil(end)
        if (end < 0):
            end = self.num_samples
        if (end > self.num_samples):
            end = self.num_samples
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_loop(self, loop):
        self.loop = loop
