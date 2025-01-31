import re
from google.colab import drive
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling, TrainerCallback
from datasets import Dataset
import os
import shutil
import pandas as pd
from datasets import Dataset



# Define the lists of artists and words to remove
artists = ["Tupac Shakur", "Nas", "Jay-Z", "Eminem", "Rakim", "Kendrick Lamar", "Andre 3000", "J. Cole", "Lil Wayne",
           "Ice Cube", "Scarface", "Snoop Dogg", "Big Daddy Kane", "Lauryn Hill", "KRS-One", "Black Thought", "MF Doom", "Common", "Q-Tip",
           "Ghostface Killah", "RZA", "Mos Def", "Redman", "Big Pun", "Busta Rhymes", "Drake", "Missy Elliott", "LL Cool J", "Talib Kweli",
           "DMX", "Big L", "Chuck D", "Ludacris", "Lupe Fiasco", "Method Man", "Raekwon", "Slick Rick", "Jadakiss", "Future", "Fabolous",
           "Kid Cudi", "Travis Scott", "Rick Ross", "T.I.", "Nate Dogg", "JID", "Denzel Curry", "Earl Sweatshirt", "Joey Bada$$", "Nipsey Hussle",
           "GZA", "Kool G Rap", "MC Lyte", "Queen Latifah", "Pusha T", "Big Boi", "Juice WRLD", "Playboi Carti", "ASAP Rocky", "Lil Uzi Vert",
           "Tyler, The Creator", "Meek Mill", "Saweetie", "Lil Kim", "Cardi B", "Nicki Minaj", "2 Chainz", "J. Cole", "YBN Cordae", "Joyner Lucas",
           "Lil Dicky", "Wale", "Freddie Gibbs", "Chance the Rapper", "Vic Mensa", "Chief Keef", "21 Savage", "Lil Baby", "Gunna", "Young Thug",
           "Megan Thee Stallion", "Doja Cat", "Saweetie", "Rapsody", "Migos", "Ski Mask the Slump God", "Brockhampton", "Flatbush Zombies", "Run the Jewels",
           "Logic", "Tech N9ne", "Yelawolf", "Action Bronson", "Danny Brown", "Vince Staples", "Azealia Banks", "Rico Nasty", "Cupcakke"]

words_to_remove = ["embed", "nigger", "nigga", "kill", "gun", "intro", "chorus", "verse", "bridge", "refrain", "bitch", "murder", "drugs", "cocaine", "pills",
                   "ass", "titties", "cum", "fuck", "shit", "whore", "ho", "motherfucker", "cunt", "pussy", "bastard"]

def remove_unk_and_words(input_file, output_file, artists, words_to_remove):
    words_to_remove = set(word.lower() for word in artists + words_to_remove)

    def remove_words(line, words):
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, words)) + r')\b', re.IGNORECASE)
        return pattern.sub('', line)

    def remove_special_patterns(line):
        line = re.sub(r'\b\d*embed\d*\b', '', line)  
        line = re.sub(r'\d+', '', line) 
        line = re.sub(r'[^\w\s]', '', line)  
        return line

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []

    for line in lines:
        line = line.replace('<UNK>', '').strip()
        line = remove_special_patterns(line)
        cleaned_line = remove_words(line, words_to_remove)
        cleaned_line = re.sub(r'\s+', ' ', cleaned_line).strip()
        cleaned_lines.append(cleaned_line)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

    print(f"Words, special characters, and numbers removed, and cleaned text saved to {output_file}")

input_file_path = '/content/drive/My Drive/final_rap_lyrics.txt'  # Path to your input text file on Google Drive
output_file_path = '/content/clean_lyrics.txt'  # Path where the cleaned text will be saved on Colab

remove_unk_and_words(input_file_path, output_file_path, artists, words_to_remove)



#Lyric Model Training
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

model_name = "gpt2-large"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.add_special_tokens({'pad_token': '[PAD]', 'sep_token': '<SEP>', 'eos_token': '[EOS]'})

model = GPT2LMHeadModel.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))
model.to(device)

# Load the cleaned lyrics file
file_path = '/content/clean_lyrics.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
subset_lines = lines[:len(lines)]  # Use first 25% of the lines


dataset = Dataset.from_dict({"text": subset_lines})

def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding="max_length", max_length=128)

tokenized_subset = dataset.map(tokenize_function, batched=True)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

for param in model.transformer.h[:24].parameters():
    param.requires_grad = False

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=8, 
    learning_rate=5e-5,
    fp16=True if device == 'cuda' else False,
    logging_steps=2000,
)

def generate_lyrics(prefix=None, length=250):
    model.eval()
    if prefix:
        inputs = tokenizer(prefix, return_tensors="pt").to(device)
    else:
        inputs = None

    outputs = model.generate(
        input_ids=inputs.input_ids if inputs else None,
        max_length=length,
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id,
        repetition_penalty=1.2,  
        do_sample=True,  
        top_k=50,  
        top_p=0.95  
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Custom callback to generate text and save model during training
class TextGenerationCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % args.logging_steps == 0:
            print("\nGenerating text at step {}:".format(state.global_step))
            generated_lyrics = generate_lyrics(prefix="Never gonna give you up")
            print(generated_lyrics)


trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_subset,
    callbacks=[TextGenerationCallback]
)


trainer.train()

# Save final model and tokenizer
model.save_pretrained("fine_tuned_gpt2_lyrics")
tokenizer.save_pretrained("fine_tuned_gpt2_lyrics")

# Example generation
generated_lyrics = generate_lyrics(prefix="Never gonna give you up")
print("\nGenerated Lyrics:\n")
print(generated_lyrics)



#!cp -r /content/fine_tuned_gpt2_lyrics /content/drive/MyDrive/thesis
#!cp /content/fine_tuned_gpt2_lyrics/model.safetensors /content/drive/MyDrive/thesis



# Melody Model Training


model_name = "gpt2-xl"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.add_special_tokens({'pad_token': '[PAD]', 'sep_token': '<SEP>', 'eos_token': '[EOS]'})

model = GPT2LMHeadModel.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))
model.to(device)

def freeze_layers(model, freeze_fraction=0.5):
    total_layers = len(list(model.parameters()))
    freeze_layers = int(total_layers * freeze_fraction)

    for i, param in enumerate(model.parameters()):
        if i < freeze_layers:
            param.requires_grad = False
        else:
            param.requires_grad = True

# Apply freezing to the first 50% of the layers
freeze_layers(model, freeze_fraction=0.5)

detailed_file_path = '/content/drive/MyDrive/final_melody_data.csv'
concatenated_file_path = '/content/drive/MyDrive/concatenated_melody_data.csv'

df_detailed = pd.read_csv(detailed_file_path)
df_concatenated = pd.read_csv(concatenated_file_path)
detailed_data = [f"{phone} <SEP> {note}" for phone, note in zip(df_detailed['Phone'], df_detailed['Note'])]
concatenated_data = [f"{words} <SEP> {notes}" for words, notes in zip(df_concatenated['Concatenated Words'], df_concatenated['Concatenated Notes'])]
detailed_dataset = Dataset.from_dict({"text": detailed_data})

def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding="max_length", max_length=128)

tokenized_detailed_dataset = detailed_dataset.map(tokenize_function, batched=True)
concatenated_dataset = Dataset.from_dict({"text": concatenated_data})
tokenized_concatenated_dataset = concatenated_dataset.map(tokenize_function, batched=True)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=8,
    learning_rate=5e-5,
    save_steps=5000,
    save_total_limit=1,
    fp16=True if device == 'cuda' else False,
    logging_steps=1000,  s
    save_strategy="no",
)

# Custom callback to generate output during training
class TextGenerationCallback(TrainerCallback):
    def __init__(self, tokenizer, model, logging_steps=500):
        self.tokenizer = tokenizer
        self.model = model
        self.logging_steps = logging_steps

    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % self.logging_steps == 0:
            sample_input = "Look if you had one shot"  
            generated_melody = self.generate_melody(sample_input)
            print(f"\nGenerated text at step {state.global_step}:\n{generated_melody}\n")

    def generate_melody(self, input_text, max_length=100):
        self.model.eval()
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            input_ids=inputs.input_ids,
            max_length=max_length,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id,
            repetition_penalty=1.2,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


trainer_detailed = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_detailed_dataset,
    callbacks=[TextGenerationCallback(tokenizer, model, logging_steps=500)]
)

trainer_detailed.train()
trainer_concatenated = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_concatenated_dataset,
    callbacks=[TextGenerationCallback(tokenizer, model, logging_steps=500)]
)

trainer_concatenated.train()
final_output_dir = "fine_tuned_gpt2_melody_combined"
model.save_pretrained(final_output_dir)
tokenizer.save_pretrained(final_output_dir)
shutil.make_archive(final_output_dir, 'zip', final_output_dir)
print(f"Final fine-tuned model saved: {final_output_dir}")


