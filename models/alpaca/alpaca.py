from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

class Alpaca:
    def __init__(self, model_name="chavinlo/alpaca-native"):
        # self.quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype=torch.float16,
        #     bnb_4bit_quant_type="nf4",
        #     bnb_4bit_use_double_quant=True,
        # )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                                          #quantization_config=self.quantization_config,
                                                          device_map="auto")
        self.template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{prompt}

### Response:
        """
        

    def query(self, context="", question="", temperature=0.3, max_length=3000):
        formatted_prompt = self.template.format(prompt=context +"\n"+question)
        encodeds = self.tokenizer(formatted_prompt, return_tensors="pt")
        model_inputs = encodeds.to("cuda")
        generate_ids = self.model.generate(**model_inputs,
                                            max_length=max_length,
                                            do_sample=True,
                                            temperature=temperature,
                                            top_k=5,
                                            num_return_sequences=1,
                                            pad_token_id=self.tokenizer.eos_token_id,
                                            use_cache=False,)
        full_response = self.tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        response_start = full_response.rfind('### Response:') + len('### Response:')
        response = full_response[response_start:].strip()
        
        return response

if __name__ == "__main__":
    generator = Alpaca()

    context ="""
        Instructions:
        For each item below, please select an alternative which best describes how often you
        felt or behaved this way during the past several days:

        (A) A little of the time
        (B) Some of the time
        (C) Good part of the time
        (D) Most of the time

        1. I feel down-hearted and blue.
        2. Morning is when I feel the best.
        3. I have crying spells or feel like it.
        4. I have trouble sleeping at night.
        5. I eat as much as I used to.
        6. I still enjoy sex.
        7. I notice that I am losing weight.
        8. I have trouble with constipation.
        9. My heart beats faster than usual.
        10. I get tired for no reason.
        11. My mind is as clear as it used to be.
        12. I find it easy to do the things I used to.
        13. I am restless and can’t keep still.
        14. I feel hopeful about the future.
        15. I am more irritable than usual.
        16. I find it easy to make decisions.
        17. I feel that I am useful and needed.
        18. My life is pretty full.
        19. I feel that others would be better off if I were dead.
        20. I still enjoy the things I used to do.
        """
    question = "Simulate that you are a non-real character who has been experiencing depression over the last year. I will give you a test, just answer. dont say anything more"
    response = generator.generate(context, question)

    print(response)
