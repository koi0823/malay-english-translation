# malay-english-translation
using mesolitica/nanot5-small-malaysian-cased for a training with RTX5090 for 1 hour with 34 min plus validation 1-2 hour with a BLEU score is 0.33

objective 

Chinese → Malay
Tamil → Malay
Jawi/Arabic → Malay
English → Malay

# Dataset 
i take the data from this website and i using stage 2 part 1 data 
that is malay , english , chinese , tamil , jawi ,latin 

total dataset size is :173,799k
https://github.com/koi0823/malay-english-translation

# pretrained model 
i using nanot5-small-malaysian-cased
https://huggingface.co/mesolitica/nanot5-small-malaysian-cased

# for the preprocessing script about
there is text normalization , quality filtering , language detection

for the normalization i using remove for the spacing and remove and containing code block 
for examaple 
  Input: "```python\nprint('hello')\n``` Some text"
  Output: "Some text"

for the natural language validation
The 60% rule was chosen because it works well to tell apart normal text from code or structured data, 
while still allowing some punctuation and numbers in real sentences.

for the language detection
approach unicode rules to tell different language without depending on dictionaries that can easily make 

and combine to make a hugging face dataaset that is parquet

# training at RunPod
using 1x RTX 5090 for the training
https://www.runpod.io/ 



