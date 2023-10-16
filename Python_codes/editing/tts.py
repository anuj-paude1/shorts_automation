from elevenlabs import generate, stream, set_api_key,play, RateLimitError,voices

def get_api_key():
    with open("api_key.txt", "r") as file:
        # Read the value from the file
        for i in range(1,3):
            api_key = file.readline()
            api_key=api_key.strip()
    return api_key

def get_audio(text,voice):
    
    api_key=get_api_key()
    set_api_key(api_key=api_key)

    generate_params = {
        "text": text,  # The text you want to convert to audio
        "voice": voice,  # The voice you want to use
        }

    try:
        audio = generate(
        **generate_params
        )
    except RateLimitError:
        with open("./api_key.txt", "r") as source_file:
            # Read the content of the file, excluding the first line
            lines = source_file.readlines()[1:]
        # Open the source file in write mode to overwrite it with the modified content
        with open("./api_key.txt", "w") as source_file:
            source_file.writelines(lines)

        api_key=get_api_key()
        set_api_key(api_key)
        audio = generate(
        **generate_params
        )
    name=text[:10]
    output_file_path = f"../temp/audios/{name}.wav"
    with open(output_file_path, "wb") as f:
        f.write(audio)
    return f"{name}.wav"
        

def main():
    # get_audio("test audio 123 my name is i am sorry elevenlabs is so fucking good","Adam")
    ...

if __name__=="__main__":
    main()

