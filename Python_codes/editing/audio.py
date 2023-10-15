

def get_audio_timestamp(audio_path="../temp",audio_name="test_audio_1.wav"):
    import os
    import wave
    from vosk import Model, KaldiRecognizer
    import json

    # Specify the path to the Vosk model and set the model and recognizer
    model_path = "./vosk-model-en-us-0.22-lgraph"
    model = Model(model_path)
    

    # Load an audio file

    if(audio_name.split('.')[0]!="wav"):
       audio_name=convert_wav(audio_path,audio_name)
    
    # Open and read the audio file
    wf = wave.open(f"{audio_path}/{audio_name}", "rb")
    rec = KaldiRecognizer(model,  wf.getframerate())
    rec.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(json.loads(rec.Result()))

    data=json.loads(rec.FinalResult())
    print(data['result'])
    return (data['result'])
    



def convert_wav(path,name):
    from pydub import AudioSegment

    wav_name=f"{name.split('.')[0]}.wav"
    audio = AudioSegment.from_mp3(f"{path}/{name}")
    audio.export(f"{path}/{wav_name}", format="wav")
    return wav_name




def main():
    ...




if __name__=="__main__":
    main()