import json
import boto3
import pprint
import base64
import langchain
from langchain.llms.bedrock import Bedrock
from botocore.client import Config
from langchain.prompts import PromptTemplate
import re

def lambda_handler(event, context):
    
    event = json.loads(event['body'])
    # story_theme = event['theme']
    # story_type = 'children'
    # main_character  = 'Laila'
    # story_theme = 'Brushing the tooth'
    # moral_lesson = ' develop hygiene practices'
    # setting  = 'megical kingdom'
    
    story_type = event['story_type']
    main_character = event['main_character']
    story_theme = event['story_theme']
    moral_lesson = event['moral_lesson']
    setting = event['setting']
    word_count = event['word_count']
  
    
    try:
        pp = pprint.PrettyPrinter(indent=2)
        session = boto3.session.Session()
        region = session.region_name
        bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
        bedrock_client = boto3.client('bedrock-runtime', region_name = region)
        bedrock_agent_client = boto3.client("bedrock-agent-runtime",config=bedrock_config, region_name = region)
        
        kbId = "V1XKME5RZW"
        
        def retrieve(query, kbId, numberOfResults=5):
            return bedrock_agent_client.retrieve(
                retrievalQuery= {
                    'text': query
                },
                knowledgeBaseId=kbId,
                retrievalConfiguration= {
                    'vectorSearchConfiguration': {
                        'numberOfResults': numberOfResults
                    }
                }
            )
        
            
        query = story_theme
        response = retrieve(query, kbId, 5)
        retrievalResults = response['retrievalResults']
        
        # fetch context from the response
        def get_contexts(retrievalResults):
            contexts = []
            for retrievedResult in retrievalResults: 
                contexts.append(retrievedResult['content']['text'])
            return contexts
        
        contexts = get_contexts(retrievalResults)
     
        prompt = f"""You are a question answering agent. You have been asked to generate a {story_type} story about {main_character} who lives in {setting}. 
                     The story should focus on {story_theme} and teach the moral lesson that {moral_lesson}. The language should be simple, engaging, and suitable 
                     for {story_type}. Make the story imaginative, with playful elements, and include a happy ending where the {main_character} learns 
                     a valuable lesson. Please create the story with {word_count} words Story theme is inclosed in the <question> tag. <context> {contexts} </context> <question> {query} </question> 
                     At the end create four captions from the generated story. Thes captions should be related to each other.
        \n\nAssistant:"""

        # At the end please generate four key points which are aligned with the generated story. 
    
        # payload with model paramters
        messages=[{ "role":'user', "content":[{'type':'text','text': prompt.format(contexts, query)}]}]
        sonnet_payload = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": messages,
            "temperature": 0.5,
            "top_p": 1
                }  )
                
        modelId = 'anthropic.claude-3-haiku-20240307-v1:0' 
        accept = 'application/json'
        contentType = 'application/json'
        response = bedrock_client.invoke_model(body=sonnet_payload, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get('body').read())
        response_text = response_body.get('content')[0]['text']
        # print("response_text----",response_text)
        # print("resonse --", response)
        # print("response_body --->",response_body)
        
   
        #==========
        # Step 1: Find the "Key Points:"/ Captions section
        key_points_section = response_text.split("Captions:")[1].strip()

        # print("key_points_section .... ",key_points_section)
        
        # Regex to match either numbered points (e.g., "1.", "2.") or bullet points
        points = re.split(r'\d\.\s+|•\s+|\n', key_points_section)

        # Step 3: Remove empty strings and strip extra spaces from each point
        points = [point.strip() for point in points if point.strip()]

        #print("before points ##### ", points)
        
        #==============
         
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        #client = boto3.client("bedrock-runtime", region_name="us-east-1")

         
        # Set the model ID, e.g., Titan Image Generator G1.
        stability_model_id = "stability.stable-diffusion-xl-v1"
         
        # Define the image generation prompt for the model.
        image_prompt1 = {story_theme}
        
        # Use regex to extract points based on numbering (1., 2., etc.)
        #points = re.split(r'\d\.\s', response_text)
        
 
        # Remove the first element which will be an empty string due to splitting
        #points = [point.strip() for point in points if point.strip()]
        
        #print("after points ##### ", points)
        base64_image_data1=""
        base64_image_data2=""
        base64_image_data3=""
        base64_image_data4=""
        
        # Print the extracted points one by one
        my_points = list(points)
        json_points = json.dumps(my_points)
        # print("json_points n888888888888", my_points[0])
        # print("json_points n888888888881", my_points[1])
        # print("json_points n888888888882", my_points[2])
        # print("json_points n888888888883", my_points[3])
        
        prompt1 = my_points[0]
        prompt2 = my_points[1]
        # prompt3 = my_points[2]
        # prompt4 = my_points[3]
           
        native_request1 = {"text_prompts":[{"text":prompt1,"weight":1}],"cfg_scale":10,"steps":50,"seed":0,"width":1024,"height":1024,"samples":1}
        request1 = json.dumps(native_request1)
        response1 = bedrock_client.invoke_model(modelId=stability_model_id, body=request1)
        model_response1 = json.loads(response1.get("body").read())
        base64_image_data1 = model_response1["artifacts"][0].get("base64")
        # print("native_request1............")
        
        native_request2 = {"text_prompts":[{"text":prompt2,"weight":1}],"cfg_scale":10,"steps":50,"seed":0,"width":1024,"height":1024,"samples":1}
        request2 = json.dumps(native_request2)
        response2 = bedrock_client.invoke_model(modelId=stability_model_id, body=request2)
        model_response2 = json.loads(response2.get("body").read())
        base64_image_data2 = model_response2["artifacts"][0].get("base64")
        # print("native_request2............")
         
        
        # native_request3 = {"text_prompts":[{"text":prompt3,"weight":1}],"cfg_scale":10,"steps":50,"seed":0,"width":1024,"height":1024,"samples":1}
        # request3 = json.dumps(native_request3)
        # response3 = bedrock_client.invoke_model(modelId=stability_model_id, body=request3)
        # model_response3 = json.loads(response3.get("body").read())
        # base64_image_data3 = model_response3["artifacts"][0].get("base64")
        # print("native_request3............")
         
        
        # native_request4 = {"text_prompts":[{"text":prompt4,"weight":1}],"cfg_scale":10,"steps":50,"seed":0,"width":1024,"height":1024,"samples":1}
        # request4 = json.dumps(native_request4)
        # response4 = bedrock_client.invoke_model(modelId=stability_model_id, body=request4)
        # model_response4 = json.loads(response4.get("body").read())
        # base64_image_data4 = model_response4["artifacts"][0].get("base64")
        # print("native_request4............")
        

        print("beore data dump............")
        data = {}
        data['text'] = response_text
        data['image_data_decode1']  =  base64_image_data1
        data['image_data_decode2']  =  base64_image_data2
        # data['image_data_decode3']  =  base64_image_data3
        # data['image_data_decode4']  =  base64_image_data4
        # print("after data list creations............")
        # json_data = json.dumps(data)
        # print("json_data1")
        # print("json data ...", json_data)
        # print("json_data2")
        
        #x = { "statusCode": 200, "body": json_data }

        # print("x............", x)
    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""
        
    # return x   
    return {
        "statusCode": 200,  # Correct key
        "body": json.dumps(data)  # Body should be JSON-encoded string
    }