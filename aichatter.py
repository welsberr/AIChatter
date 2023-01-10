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

# WRE: the following two functions were taken from a Github 'chatGPT-clone' repo by amrrs,
# which is MIT licensed:
"""
MIT License

Copyright (c) 2022 amrrs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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
