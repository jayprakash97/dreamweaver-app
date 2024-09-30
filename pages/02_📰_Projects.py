import streamlit as st

validation_query_response = {
  0: {"query": "jay 300",
      "gold_response": "story about etc "},
  1: {"query": "Mike 400",
      "gold_response": " "}
}

# Function to evaluate RAG system using ROUGE
def rouge_scores(predicated_response, gold_response):
  import evaluate
  rouge = evaluate.load('rouge')
  rouge_scores = rouge.compute(predictions=predicated_response, references=gold_response)
  return rouge_scores

def bleu_scores(predicated_response, gold_response):
  import evaluate
  bleu = evaluate.load('bleu')
  bleu_scores = bleu.compute(predictions=predicated_response, references=gold_response)
  return bleu_scores

def bert_scores(predicated_response, gold_response):
  import evaluate
  bertscore = evaluate.load('bertscore')
  bert_scores = bertscore.compute(predictions=predicated_response, references=gold_response, lang= 'en')
  bert_scores['precision'] = sum(bert_scores['precision']) / len(bert_scores['precision'])
  bert_scores['recall'] = sum(bert_scores['recall']) / len(bert_scores['recall'])
  bert_scores['f1'] = sum(bert_scores['f1']) / len(bert_scores['f1'])
  return bert_scores


