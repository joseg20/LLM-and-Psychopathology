from transformers import BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM
import torch
from vllm import LLM, SamplingParams

class Gemma:
    def __init__(self, model_name="google/gemma-7b-it"):
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
        self.template = """
<bos><start_of_turn>{role}
{question}<end_of_turn>
<start_of_turn>model
        """

    def query(self, context="", question="", max_tokens=2056, temperature=0.3):
        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
        formatted_prompt = self.template.format(role=context, question=question)
        generate_ids = self.model.generate(formatted_prompt,sampling_params)
    
        generated_text = generate_ids[0].outputs[0].text.replace('*', '')
        
        return generated_text

if __name__ == "__main__":
    generator = Gemma()

    context ="simulate that you are a depressed person"
    question = "hello, how you are?"
    response = generator.query(context, question)

    print(response)
