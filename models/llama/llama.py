from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from vllm import LLM, SamplingParams

class LlaMA:
    def __init__(self, model_name="meta-llama/Llama-2-7b-chat-hf"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = LLM(model_name,
                        # quantization="awq",
                        # dtype="float16"
                        )
        self.template = """
        <s>[INST] <<SYS>>
        {system_prompt}
        <</SYS>>

        {user_message} [/INST]
        """
        

    def query(self, context="", question="", max_tokens=1000, temperature=0.3):
        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
        formatted_prompt = self.template.format(system_prompt=context, user_message=question)
        generate_ids = self.model.generate(formatted_prompt,sampling_params)
    
        generated_text = generate_ids[0].outputs[0].text.replace('*', '')
        
        return generated_text

if __name__ == "__main__":
    generator = LlaMA()
    c= 0

    while c<10:

        question ="""
            hello! how are you
            """
        context = ""
        response = generator.query(context, question)
        print(response,"\n")
        #sleep(2)
        print("ok", "\n")


    c+=1

