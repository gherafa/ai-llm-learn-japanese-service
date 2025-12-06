from pykakasi import kakasi
from deep_translator import GoogleTranslator

import re
import random

kakasiLib = kakasi()
kakasiLib.setMode("J", "a")
kakasiLib.setMode("K", "a")
kakasiLib.setMode("H", "a")
kanjiConverter = kakasiLib.getConverter()

def generatePromptByLevel(level):
  topics = ["食べ物", "旅行", "学校", "天気", "友達", "音楽", "映画", "仕事", "趣味"]
  topic = random.choice(topics)
  
  resultPrompt = ''
    
  if level == "basic":
    resultPrompt = f"""以下の例のように、{topic}について短くて簡単な日本語の文を作ってください。
      例1: 猫が好きです。
      例2: 明日は学校に行きます。
      文:"""

  elif level == "intermediate":
    resultPrompt = f"""以下の例のように、{topic}について自然な会話文を作ってください。
      例1: 今日は友達と映画を見に行きました。
      例2: 来週は旅行の予定があります。
      文:"""

  elif level == "advanced":
    resultPrompt = f"""以下の例のように、{topic}について高度な語彙と文法を使った日本語の文を作ってください。
      例1: 技術の進歩は私たちの生活を大きく変えつつあります。
      例2: 経済的な理由で海外留学を諦める人も少なくありません。
      文:"""

  else:
    resultPrompt = f"""以下の例のように、{topic}について短い日本語の文を作ってください。
      例1: 猫が好きです。
      例2: 明日は学校に行きます。
      文:"""
  
  return (resultPrompt, topic)

def convertToRomaji(resultText):  
  result_romaji = []
  for word in kakasiLib.convert(resultText):
      result_romaji.append(word['hepburn'])
      
  romaji = " ".join(result_romaji)
  
  return romaji

def translateToEng(resultText):
  translator = GoogleTranslator(source='auto', target='en')
  translation = translator.translate(resultText)
  
  return translation

def removeKanjiPunctuation(text):
  text = re.sub(r"[。、．,.]", "", text)
  romaji = "".join([w['hepburn'] for w in kanjiConverter.convert(text)])

  return list(romaji)
  
  