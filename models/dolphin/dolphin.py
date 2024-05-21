from transformers import BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM
import torch
from vllm import LLM, SamplingParams

class Dolphin:
    def __init__(self, model_name="cognitivecomputations/dolphin-2.2.1-mistral-7b"):
        # self.quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype=torch.float16,
        #     bnb_4bit_quant_type="nf4",
        #     bnb_4bit_use_double_quant=True,
        # )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = LLM(model_name,
                        #quantization_config=self.quantization_config,
                        )
        self.template = """<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
        """

    def query(self, context="", question="", max_tokens=4500, temperature=0.3):
        sampling_params = SamplingParams(temperature=temperature, top_p=0.95, max_tokens=max_tokens)
        formatted_prompt = self.template.format(system_message=context, prompt=question)
        generate_ids = self.model.generate(formatted_prompt,sampling_params)
    
        # Accede al texto generado en el primer elemento de la lista 'outputs'
        generated_text = generate_ids[0].outputs[0].text
        
        return generated_text

if __name__ == "__main__":
    # Uso de la clase
    generator = Dolphin()

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
    response = generator.query(context, question)

    print(response)
