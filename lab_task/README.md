
---

## 🧠 Model Details

- **Model Name:** DistilGPT2  
- **Model Type:** Causal Language Model  
- **Number of Parameters:** ~82 million  
- **Reason for Selection:**  
  - Lightweight  
  - Efficient for Google Colab  
  - Falls well under the 3B parameter constraint  

---

## 📊 Dataset Details

- **Dataset Name:** AG News  
- **Source:** Hugging Face Datasets  
- **Dataset Type:** News article text dataset  

### Dataset Splits
| Split | Number of Samples |
|------|------------------|
| Train | 120,000 |
| Test | 7,600 |

### Dataset Fields
- `title` – Headline of the news article  
- `description` – Short summary of the article  
- `label` – Category of the article (not used for language modeling)

For this task, the **title and description were combined into a single text field** to make the dataset suitable for language model fine-tuning.

---

## ⚙️ Methodology

1. Loaded the AG News dataset from Hugging Face  
2. Combined text fields into a single continuous text input  
3. Tokenized the dataset using the GPT-2 tokenizer  
4. Fine-tuned the DistilGPT2 model on a subset of the training data  
5. Evaluated the model using **evaluation loss** and **perplexity**  
6. Analyzed generated text and training behavior  

---

## 📈 Evaluation Metrics

- **Evaluation Loss:** 3.66  
- **Perplexity:** 38.91  

Perplexity is a standard metric for language models, where lower values indicate better prediction performance. The obtained results show that the model learned meaningful patterns from the dataset.

---

## 📝 Results & Observations

- The model successfully completed fine-tuning without overfitting  
- Evaluation loss decreased across epochs  
- Generated text became more structured and news-oriented  
- Small Language Models can be effectively fine-tuned using limited computational resources  

---

## ✅ Conclusion

This lab task demonstrates that Small Language Models with fewer than 3B parameters can be fine-tuned effectively on domain-specific text datasets. The experiment highlights the efficiency of transfer learning and the practicality of using lightweight models for language modeling tasks.

---



## 🛠 Requirements

- Python  
- torch  
- transformers  
- datasets  
- accelerate  

---

## 📎 Submission Details

- **Notebook Name:** `Fine_tuning_lab_task1.ipynb`  
- **Folder Name:** `lab_task`  
- **Platform Used:** Google Colab  

---

✅ **Task completed as per instructions.**
