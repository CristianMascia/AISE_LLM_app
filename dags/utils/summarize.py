import ollama
from textwrap import dedent
import os
import pandas as pd


class LLMSummarizer:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def summarize(self) -> None:
        df = pd.read_json(os.path.join('./data/cdata', self.file_name))

        df_anomaly = df[df.label == -1].reset_index(drop=True)
        df_anomaly['summary'] = ''
        df_anomaly['prompt'] = df_anomaly.apply(lambda x: self.format_prompt(
            x['news'], x['weather'], x['traffic']), axis=1)

        df_anomaly.loc[:, 'summary'] = df_anomaly['prompt'].apply(
            lambda x: self.generate_summary(x))

        df_anomaly.to_json(path_or_buf=os.path.join(
            './data/reports/', self.file_name), orient='records')

    def format_prompt(self, news: str, weather: str, traffic: str) -> str:
        prompt = dedent(f'''
        <|system|>
        You are a helpful assistant.<|end|>
        <|user|>
        The following information describes conditions relevant to
        taxi journeys through a single day in Glasgow, Scotland.
        News: {news}
        Weather: {weather}
        Traffic: {traffic}
        Summarize the above information in 3 sentences or less.< |end | >
        <|assistant|>
        ''')
        return prompt

    def generate_summary(self, prompt: str) -> str:
        response = ollama.generate(model='phi3.5', prompt=prompt)
        return response['response']
