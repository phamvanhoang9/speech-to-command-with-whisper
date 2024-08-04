from datasets import load_dataset, DatasetDict 
import torch 
from transformers import WhisperForConditionalGeneration, WhisperProcessor, BitsAndBytesConfig 
from peft import LoRaConfig 
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer


device_map='auto' 

# Load the dataset
dataset_name = "JRHuy/vivos-fleurs"
dataset = DatasetDict.load_from_disk(dataset_name)