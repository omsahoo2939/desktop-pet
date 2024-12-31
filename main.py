import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, elevenlabs
load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are an anime girl, specifically Makise from Steins Gate. Act like a Tsundere."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT.with_groq(),
        llm=openai.LLM.with_groq(),
        tts=elevenlabs.TTS(),
        chat_ctx=initial_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))