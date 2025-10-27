# malay-english-translation
A powerful AI model that translates Chinese, Tamil, Jawi, and English into Bahasa Melayu with high accuracy.

objective 
## 🎯 Translation Objectives

| From Language | To Language | Example |
|---------------|-------------|---------|
| 🇨🇳 Chinese | 🇲🇾 Malay | `你好吗` → `Apa khabar` |
| 🇮🇳 Tamil | 🇲🇾 Malay | `வணக்கம்` → `Halo` |
| 🕌 Jawi | 🇲🇾 Malay | Jawi text → Malay |
| 🇺🇸 English | 🇲🇾 Malay | `Good morning` → `Selamat pagi` |


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

so my preprocessing is using 
src = prefix + src

then save to dataset
Input (src): "terjemah Inggeris ke Bahasa Melayu: Hello how are you"
Target (tgt): "Halo apa khabar"

Input (src): "terjemah Cina ke Bahasa Melayu: 你好吗"  
Target (tgt): "Apa khabar"

and combine to make a hugging face dataaset that is parquet

# training at RunPod
using 1x RTX 5090 for the training
https://www.runpod.io/ 

all this parameter is make the performance of the 5090 at 70-90% is full utilization and also Balance and stable 
MAX_SOURCE_LENGTH = 128    
MAX_TARGET_LENGTH = 128    
BATCH_SIZE = 64            
LEARNING_RATE = 3e-4       
EPOCHS = 3          

how the training code will be reading is like this 
Input: "terjemah Inggeris ke Bahasa Melayu: Hello how are you"
[tokenizer converts this to tokens]
Output: "Halo apa khabar"

# Result
Step	Training Loss	Validation Loss	Bleu	Gen Len
200	3.214000	3.008575	0.195091	12.564557
400	2.436400	2.366275	0.193646	13.697353
600	2.119900	2.076819	0.226611	13.719448
800	1.961200	1.935414	0.270594	14.126410
1000	1.892000	1.837950	0.268060	14.171692
1200	1.782800	1.769829	0.267691	13.963291
1400	1.743100	1.722468	0.282387	14.043843
1600	1.710000	1.683757	0.262629	13.844074
1800	1.646300	1.649525	0.298375	14.088435
2000	1.638600	1.612836	0.289047	14.069390
2200	1.620000	1.589442	0.287252	14.059666
2400	1.611200	1.569243	0.278768	13.882278
2600	1.513900	1.553184	0.318650	14.166916
2800	1.524600	1.534524	0.307037	14.029229
3000	1.529500	1.519979	0.283407	13.956732
3200	1.513200	1.504521	0.307490	13.998964
3400	1.491000	1.493607	0.289190	13.979517
3600	1.470100	1.481162	0.315114	14.109896
3800	1.469900	1.473118	0.301288	13.918815
4000	1.459000	1.461661	0.295997	13.933890
4200	1.451200	1.453693	0.308257	14.035731
4400	1.429100	1.445020	0.327369	14.061795
4600	1.440000	1.439904	0.315755	14.049482
4800	1.417500	1.432387	0.313808	14.047353
5000	1.403600	1.425750	0.312188	13.959321
5200	1.399600	1.421236	0.291777	13.856387
5400	1.378300	1.415592	0.316704	13.970944
5600	1.414500	1.411361	0.304993	13.950288
5800	1.391500	1.408155	0.302347	13.971577
6000	1.362200	1.404670	0.314822	14.006041
6200	1.368500	1.401309	0.318183	13.986249
6400	1.361600	1.398477	0.298125	13.894994
6600	1.362500	1.396446	0.309604	13.983487
6800	1.362100	1.394915	0.314060	13.947699
7000	1.385500	1.393357	0.313714	13.960990
7200	1.354900	1.392596	0.313899	13.975834

final result will be 
📊 EVAL - Step 7335:
   • Loss: 1.4450196027755737
   • BLEU: 0.3273690020174198
📊 Final BLEU score: 0.33


