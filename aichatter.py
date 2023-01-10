import sys
import os
import traceback
import pickle
import datetime
import openai
#import docopt

# Nota bene: You must provide a valid OpenAI API in the following line or 
# the program will fail. The placeholder here is not a valid key.
openai.api_key = 'YOUR-OPENAI-API-KEY-GOES-HERE'

class Holder(object):
    def __init__(self):
        pass

def get_now_iso_date():
    current_date = datetime.datetime.now()
    return current_date.isoformat()

def openai_create(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

def init_chat(ctx):
    ctx.pr = []
    ctx.prompt = ""
    ctx.state = None
    return ctx

def chat(ctx, DEBUG=0):
    done = False
    datestr = get_now_iso_date()
    safedatestr = datestr
    safedatestr = safedatestr.replace(" ", "_")
    safedatestr = safedatestr.replace(",", "_")
    safedatestr = safedatestr.replace(":", "_")

    savefn = f"chatgpt_{safedatestr}.pkl"

    print("You enter a prompt, it is sent to ChatGPT using your API key (can cost you $$$).")
    print("The ChatGPT completion (or partial completion) is displayed.")
    print("All prompt/completion cycles in this chat session comprise the state")
    print("passed back to ChatGPT. Therefore, your token usage rises with more ")
    print("history in the chat. Consider whether you should quit and start a new chat.\n")
          
    print("Enter any of 'quit', 'exit', or '__end__' to terminate the chat.\n")

    while not done:
        try:
            # Ask for input
            newprompt = input("Prompt?: ")
            if newprompt.lower() in [None, 'quit', 'exit', '__end__']:
                break
            ctx.prompt = newprompt
            ctx.timestamp = get_now_iso_date()
            ctx.response, ctx.state = chatgpt_clone(ctx.prompt, ctx.state)

            print("prompt", ctx.prompt)
            print("response:")
            print(ctx.response[-1][1])

            ctx.pr.append([ctx.response, ctx.state, ctx.timestamp])

            pickle.dump(ctx, open(savefn, "wb"))
            if 0 < DEBUG: print(f"Chat saved as {savefn}.")
        except:
            estr = f"Error: {traceback.format_exc()}"
            print(estr)
            done = True

    pickle.dump(ctx, open(savefn, "wb"))
    print(f"Chat saved as {savefn}.")

if __name__ == "__main__":

    ctx = Holder()
    ctx = init_chat(ctx)
    chat(ctx)

    print("AIChatter.py done.")
