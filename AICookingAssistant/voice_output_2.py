from together import Together

client = Together(api_key="tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8")

speech_file_path = "speech.mp3"

response = client.audio.speech.create(
    model="cartesia/sonic-2",
    input="Today is a wonderful day to build something people love!",
    voice="helpful woman",
)

response.stream_to_file(speech_file_path)