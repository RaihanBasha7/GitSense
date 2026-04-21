print("Webhook test completed 🚀")
def add(a,b):return a+b
#testing phase-2
password="123456"
def pas():
    pass
def divide(a,b):
    return a/b
def add(a,b):return a+b

password="123456"

def divide(a,b):
    return a/b
import google.generativeai as genai

genai.configure(api_key="AIzaSyBnYdxKoKCSKfkzkHIKySmfqwmgMmi-lr4")

models = genai.list_models()

for model in models:
    print(model.name)