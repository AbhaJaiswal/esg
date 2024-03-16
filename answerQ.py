
# importing required modules 
from PyPDF2 import PdfReader 
from openai import AzureOpenAI
from flask import Flask, request, jsonify
  
app = Flask(__name__)  

def getAnswersFromPDF(name, entity): 

                # creating a pdf reader object 
                reader = PdfReader(name) 

                # printing number of pages in pdf file 
                print(len(reader.pages)) 

                # getting a specific page from the pdf file 
                page = reader.pages[1] 

                # extracting text from page 
                text = page.extract_text() 
                #print(text) 




                client = AzureOpenAI(
                  azure_endpoint = "https://team-todo.openai.azure.com/openai/deployments/test-aj/chat/completions?api-version=2024-02-15-preview", 
                  api_key="e347916c17ca472cb05c1469a1fc5836",  
                  api_version="2024-02-15-preview"
                )
                

                message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":text},{"role":"user","content":"what is the adopted goal for reducing emission intensity? Answer only with number and timeframe."}]

                print("Question : what is the adopted goal for reducing emission intensity? Answer only with number.")

                completion = client.chat.completions.create(
                  model="test-aj", # model = "deployment_name"
                  messages = message_text,
                  temperature=0.7,
                  max_tokens=800,
                  top_p=0.95,
                  frequency_penalty=0,
                  presence_penalty=0,
                  stop=None
                )

                print()
                print(completion)

                emissionReductionQ = {
                    "question": "what is the interim emission reduction target",
                    "esgType": "Environment",
                    "esgIndicators": "InterimEmissionsReductionTarget",
                    "primaryDetails": completion.choices[0].message.content,
                    "secondaryDetails": "",
                    "citationDetails": "string",
                    "pageNumber": 1
                }


                message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":text},{"role":"user","content":"Is there a Diversity, Equity and Inclusion target? Answer should be 'yes' or 'no' or unclear' only."}]

                print()
                print("Is there a Diversity, Equity and Inclusion target? Answer in yes or no only.")
                completion = client.chat.completions.create(
                  model="test-aj", # model = "deployment_name"
                  messages = message_text,
                  temperature=0.7,
                  max_tokens=800,
                  top_p=0.95,
                  frequency_penalty=0,
                  presence_penalty=0,
                  stop=None
                )

                print(completion.choices[0].message.content)

                diversityQ = {
                    "question": "what is the Diversity, Equity and Inclusion target",
                    "esgType": "Social",
                    "esgIndicators": "DE&ITarget",
                    "primaryDetails": completion.choices[0].message.content,
                    "secondaryDetails": "",
                    "citationDetails": "",
                    "pageNumber": 1
                }

                esgResponse = {
                  "esgResponse": [
                    {
                      "entityName": entity,
                      "benchmarkDetails": [emissionReductionQ,diversityQ]
                    }
                  ]
                }
                 # Return user data as JSON object  
                return jsonify(esgResponse)



@app.route('/ESGReport')  
def hello():  
  name = request.args.get('pdf', 'spx.pdf')  
  entity = request.args.get('entity', 'spx') 
  return getAnswersFromPDF(name,entity)


if __name__ == '__main__':  
    app.run(debug=True)  
