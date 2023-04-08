from transformers import PegasusTokenizer, PegasusForConditionalGeneration

model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)


def summarize(summarize_text):
    input_ids = tokenizer.encode("summarize: " + summarize_text, return_tensors="pt", max_length=2048, truncation=True)
    summary_ids = model.generate(input_ids, num_beams=4, max_length=100, early_stopping=True, temperature=1.0)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
