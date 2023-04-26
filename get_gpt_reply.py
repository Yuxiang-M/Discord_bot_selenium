import openai

# openai.organization = 'org-nuoujL7o1bWpXExT4n9H9Xpy'
with open ('./auto_bot_discord/gpt_key.txt','r') as f:
    api_key = f.read()

# print(openai.Model.list())
def get_gpt_reply(api_key,query):
    openai.api_key = api_key
    model_engine = "text-davinci-001"
    prompt = query

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

if __name__ == '__main__':
    answer = get_gpt_reply(api_key=api_key,query='Hello ChatGPT!')
    print(answer)
