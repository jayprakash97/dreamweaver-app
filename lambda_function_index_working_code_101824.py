import json
import boto3
import pprint
import base64
import langchain
from langchain.llms.bedrock import Bedrock
from botocore.client import Config
from langchain.prompts import PromptTemplate
import re

# pp = pprint.PrettyPrinter(indent=2)
session = boto3.session.Session()
region = session.region_name
bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_client = boto3.client('bedrock-runtime', region_name = region)
bedrock_agent_client = boto3.client("bedrock-agent-runtime",config=bedrock_config, region_name = region)
 
def getStory(event):
    # event = json.loads(event['body'])
    # story_theme = 'children'
    # story_type = 'children'
    # main_character  = 'Laila'
    # story_theme = 'Brushing the tooth'
    # moral_lesson = 'develop hygiene practices'
    # setting  = 'megical kingdom'
    # word_count = '300'
    # story_lang = 'English'
    story_type = event['story_type']
    main_character = event['main_character']
    story_theme = event['story_theme']
    moral_lesson = event['moral_lesson']
    setting = event['setting']
    word_count = event['word_count']
    story_lang = event['story_lang']
    try:
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
        print("Story Theme --> ",story_theme)
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
        
        # parts = '0'
        # if word_count == '500':
        #   parts = '7'
        # elif word_count == '400':
        #   parts = '6'
        # else:
        #   parts = '5'
        
        # print("before prompt....", parts)
           
        # prompt = f"""
        #         You are a story creator.  You have been asked to generate a {story_type} story with one of the character name as {main_character} who lives in {setting}. 
        #         The story should focus on {story_theme} and teach the moral lesson that {moral_lesson}. The language should be simple, engaging, and suitable 
        #         for {story_type}. Make the story imaginative, with playful elements, and include a happy ending where the {main_character} learns 
        #         a valuable lesson. Please create the story with {word_count} words Story theme is inclosed in the <question> tag.
        #         <context> 
        #         {contexts} 
        #         </context> 
                
        #         <question> 
        #         {query} 
        #         </question> 
                      
        #         Give response in Json format by following below instruction,
        #             1) Devide the story in 5 euqal parts and use following instruction to generate response.
        #             2) Each object in json shoud contians two keys, stroy_text and caption. Don't give object any name or number.
        #             3) story_text should contain story text.
        #             4) caption should contains caption based on story text and that can be used as prompt for stable diffusion model. Remove the filtered word from the caption. Main charator should be same and animated images should be generated without text in image.
        #             5) Inclose the json only with Curly Brackets.
        #             6) Only return JSON not any additional text & new line in response.
                    
        # \n\nAssistant:"""
        
        prompt = f""" 
                You are a story creator.  You have been asked to generate a {story_type} story with one of the character name as {main_character} who lives in {setting}. 
                The story should focus on {story_theme} and teach the moral lesson that {moral_lesson}. The language should be simple, engaging, and suitable 
                for {story_type}. Make the story imaginative, with playful elements, and include a happy ending where the {main_character} learns 
                a valuable lesson. Please create the story with {word_count} words Story theme is inclosed in the <question> tag. Story should be in the language as {story_lang}.
                
                <context> 
                {contexts} 
                </context> 
                
                <question> 
                {query} 
                </question> 

                Give response in Json format by following below instruction ,
                    1) Devide the story in 5 euqal parts and use following instruction to generate response.
                    2) Each object in json shoud contians two keys, stroy_text and caption. Don't give object any name or number.
                    3) story_text should contain story text.
                    4) caption should contains caption based on story text and that can be used as prompt for stable diffusion model. Remove the filtered word from the caption. Main charator should be same and animated images should be generated without text in imag.
                    5) Inclose the json only with Curly Brackets.
                    6) Only return JSON not any additional text & new line in response.
        \n\nAssistant:"""
 
        print("after prompt....", prompt)
        # payload with model paramters
        
        # Creating a message with prompt to invoke LLM
        messages=[{ "role":'user', "content":[{'type':'text','text': prompt.format(contexts, query)}]}]
        sonnet_payload = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2500,
            "messages": messages,
            "temperature": 0.5,
            "top_p": 1
                }  )
        modelId = 'anthropic.claude-3-haiku-20240307-v1:0' 
        accept = 'application/json'
        contentType = 'application/json'
        
        # Invoke LLM which is returing the response
        response = bedrock_client.invoke_model(body=sonnet_payload, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get('body').read())
        response_text = response_body.get('content')[0]['text']
        #print("response_text----",response_text)


        # Creating a json object by adding square bracket
        json_string = "[" + response_text + "]"
        
        # creating a json object
        objects_list = json.loads(json_string)
        
        story_texts = [obj['story_text'] for obj in objects_list]
        captions = [obj['caption'] for obj in objects_list]
        
        data = {}
        data['story_texts'] = story_texts
        data['captions'] = captions
        # print("after data list creations............")
        json_data = json.dumps(data)
        #print("json data -- ", json_data)
        
    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""
    return {
        "statusCode": 200,
        "body": json_data
    }
 
def getImage(story_prompt, previous_prompt):
    try:
        stability_model_id = "stability.stable-diffusion-xl-v1"
        base64_image_data1=""
        # base64_image_data2=""
 
        # prompt = "Create an animated image based on prompt. " +  story_prompt 
        
        # prompt1 = prompt + ". Ensure that the character image is algined between " prompt + "and" + previous_prompt
        prompt =  story_prompt 
        prompt1 = "Create an animated image based on prompt " + prompt + ". Ensure that the character image is algined between " + prompt + "and" + previous_prompt
        
     
        
        native_request1 = {"text_prompts":[{"text":prompt1,"weight":1}],"cfg_scale":10,"steps":50,"seed":0,"width":1024,"height":1024,"samples":1}
        request1 = json.dumps(native_request1)
        response1 = bedrock_client.invoke_model(modelId=stability_model_id, body=request1)
        model_response1 = json.loads(response1.get("body").read())
        base64_image_data1 = model_response1["artifacts"][0].get("base64")
       
        data = {}
        data['image_data_decode1']  =  base64_image_data1
        # data['image_data_decode2']  =  base64_image_data2

        # print("after data list creations............")
        json_data = json.dumps(data)
        #print("json data -- ", json_data)
    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""
    return {
        "statusCode": 200,
        "body": json_data
    }

def lambda_handler(event, context):
    print("############# In API Call")
    print("event -----> ",event)
    event = json.loads(event['body'])
    api_path = event['api_Path']
 
    #api_path = "getStory"
    print("API Call")
 
    if api_path == 'getStory':
        print("###### Get Story API Call Responce -")
        response = getStory(event)
        print("response....", response)
        return response
    elif api_path == 'getImage':
        
        story_prompt = event['storyPrompt']
        previous_prompt  = event['previousPrompt']
        print("###### Get Image API Call Responce -")
        response = getImage(story_prompt, previous_prompt)
        print("response image ....", response)
        return response
