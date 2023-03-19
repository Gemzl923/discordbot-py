import discord

import youtube_dl

import asyncio

import os

# 디스코드 클라이언트 초기화

client = discord.Client()

# 봇의 토큰 설정

TOKEN = "YOUR_BOT_TOKEN_HERE"

# 유튜브 동영상 정보를 가져오는 함수

def get_video_info(url):

    with youtube_dl.YoutubeDL({'outtmpl': 'temp.mp3'}) as ydl:

        video_info = ydl.extract_info(url, download=True)

        return {

            'title': video_info['title'],

            'url': video_info['url']

        }

# 디스코드 봇의 이벤트 핸들러

@client.event

async def on_message(message):

    if message.author == client.user:

        return

    if message.content.startswith('!play'):

        # 명령어에 포함된 URL에서 유튜브 동영상 정보 가져오기

        url = message.content.split(' ')[1]

        video_info = get_video_info(url)

        # 오디오 채널 확인

        voice_channel = message.author.voice.channel

        if not voice_channel:

            await message.channel.send("음성 채널에 연결되어 있지 않습니다.")

            return

        # 봇과 음성 채널 연결

        vc = await voice_channel.connect()

        # 오디오 재생

        vc.play(discord.FFmpegPCMAudio(video_info['url']))

        await message.channel.send(f"{video_info['title']}를 재생합니다.")

        # 오디오 재생 종료 대기

        while vc.is_playing():

            await asyncio.sleep(1)

        # 봇과 음성 채널 연결 해제

        await vc.disconnect()

# 디스코드 봇 실행

client.run(TOKEN)

