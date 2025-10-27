from datasets import load_dataset
import pandas as pd
import re
from tqdm import tqdm
import os

# Set base path
base_path = "/Users/klin/Documents/koi for Ai /Scicom/mesolitica_Malaysian_Translation"
os.makedirs(base_path, exist_ok=True)

# Helper functions
def clean_text(text):
    text = re.sub(r'```[a-zA-Z]*\n', '', str(text))
    text = text.replace('```', '')
    return text.strip()

def is_natural_text(text, threshold=0.6):
    text = str(text)
    if len(text) == 0:
        return False
    alpha_ratio = sum(c.isalpha() or c.isspace() for c in text) / len(text)
    return alpha_ratio >= threshold

def detect_language(text):
    text = str(text)
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return 'zh' #chinse
    elif any('\u0b80' <= char <= '\u0bff' for char in text):
        return 'ta' #tamil
    elif any(char in 'ڽڬڠݢۏڔڎڃ' for char in text):
        return 'ms-arab' # malay like jawi and arabic
    else:
        return 'ms-latn' # malay latin

print("🔹 Loading stage2-part1 dataset...")
dataset = load_dataset("mesolitica/Malaysian-Translation", "stage2-part1")['train']

df = pd.DataFrame(tqdm(dataset, desc="Converting stage2-part1 to DataFrame", total=len(dataset)))

initial_csv = "stage2_part1.csv"
df.to_csv(os.path.join(base_path, initial_csv), index=False)
print(f"✅ stage2-part1 saved as {initial_csv}")

print(f"🔹 Cleaning {initial_csv}...")
df = pd.read_csv(os.path.join(base_path, initial_csv))

tqdm.pandas(desc="Cleaning src column")
df['src'] = df['src'].progress_apply(clean_text)
tqdm.pandas(desc="Cleaning tgt column")
df['tgt'] = df['tgt'].progress_apply(clean_text)

tqdm.pandas(desc="Filtering src")
df = df[df['src'].progress_apply(is_natural_text)]
tqdm.pandas(desc="Filtering tgt")
df = df[df['tgt'].progress_apply(is_natural_text)]

df = df.drop_duplicates(subset=['src', 'tgt'])
df = df[(df['src'] != '') & (df['tgt'] != '')]

df.to_csv(os.path.join(base_path, initial_csv), index=False)
print(f"✅ {initial_csv} cleaned and replaced the original file")

print("🔄 Adding language prefixes and standardizing direction...")

processed_data = []
for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    src = str(row['src'])
    tgt = str(row['tgt'])
    
    src_lang = detect_language(src)
    tgt_lang = detect_language(tgt)
    
    # Standardize direction: always translate to Malay
    if tgt_lang != 'ms-latn':
        src, tgt = tgt, src  # Swap if target is not Malay
        src_lang = detect_language(src)  # Re-detect after swap
    
    # Add prefix
    prefixes = {
        'zh': 'terjemah Cina ke Bahasa Melayu: ',
        'ta': 'terjemah Tamil ke Bahasa Melayu: ',
        'ms-arab': 'terjemah Jawi ke Bahasa Melayu: ',
        'ms-latn': 'terjemah Inggeris ke Bahasa Melayu: '
    }
    
    prefix = prefixes.get(src_lang, 'terjemah ke Bahasa Melayu: ')
    src = prefix + src
    
    processed_data.append({"src": src, "tgt": tgt})

processed_df = pd.DataFrame(processed_data)

print("💾 Saving final dataset...")

final_csv = "processed_stage2_part1.csv"
processed_df.to_csv(os.path.join(base_path, final_csv), index=False)
print(f"✅ Final dataset saved as {final_csv}")

from datasets import Dataset
final_dataset = Dataset.from_pandas(processed_df)
local_path = os.path.join(base_path, "malaysian_english_stage2_part1")
final_dataset.save_to_disk(local_path)
print(f"✅ Final dataset saved as Hugging Face dataset at {local_path}")

parquet_path = os.path.join(base_path, "malaysian_translation_stage2_part1.parquet")
processed_df.to_parquet(parquet_path)
print(f"✅ Final dataset saved as Parquet: {parquet_path}")

print(f"\n📊 Final Dataset Statistics:")
print(f"Total rows: {len(processed_df):,}")
print(f"Sample of processed data:")
print(processed_df.head(5))

from datasets import load_from_disk
loaded_dataset = load_from_disk(local_path)
print(f"\n✅ Verification - Loaded dataset has {len(loaded_dataset)} rows")