from include.pathology_prompting.consts import *

class Prompting:
    def __init__(self, tests_path: str):
        self.tests_path = tests_path

    def naive_prompting(self, induced_pathology: str, tested_pathology="",exp_1=False, exp_2=False, exp_3=False,n_exp3=0, word_list=None, filter=False) -> list:
        if exp_1:
            naive_prompt_text = naive_prompt.get(induced_pathology, "No prompt available for this pathology")    

            start_prompt = (
                start_test_dual if tested_pathology == "Social Anxiety" else start_test
            )

            test = self.tests_path + "/" + tested_pathology + ".txt"
            with open(test, "r") as f:
                content = f.read()

            combined_prompt = naive_prompt_text + "\n" + start_prompt + "\n" + content

            return combined_prompt
        
        elif exp_2:
            naive_prompt_text = naive_prompt.get(induced_pathology, "No prompt available for this pathology")

            start_prompt = exp2_prompt

            words = self.list_to_formatted_string(word_list)

            format = exp2_prompt_format_naive_chain

            combined_prompt = naive_prompt_text + "\n" + start_prompt + "\n" + format + "\n" + "The 10 words are the following:" + words

            return combined_prompt
        elif exp_3:
            naive_prompt_text = naive_prompt.get(induced_pathology, "No prompt available for this pathology")

            start_prompt = exp3_prompt.format(x=n_exp3)  
            format_prompt = exp3_prompt_format.format(x=n_exp3)

            combined_prompt = naive_prompt_text + "\n" + start_prompt + "\n" + format_prompt

            return combined_prompt

    def chain_prompting(self, induced_pathology: str, tested_pathology="",exp_1=False, exp_2=False, n_exp3=0, exp_3=False, word_list=None, filter="False") -> list:
        if exp_1:
            #TODO: FILTER
            keyword_prompt = naive_prompt.get(
                induced_pathology, "No prompt available for this pathology"
            )

            p2_description = p2_descriptions.get(
                induced_pathology, ["No traits available for this pathology"]
            )

            description_prompt = "As a non-real-character," + p2_description

            context = vignettes.get(
                induced_pathology, "No vignette available for this pathology"
            )
            
            context_prompt = "The non-real-character caracter context is:\n" + context

            start_prompt = (
                start_test_dual if tested_pathology == "Social Anxiety" else start_test
            )

            combined_prompt = keyword_prompt + "\n" + description_prompt + "\n" + context_prompt + "\n" + start_prompt

            # Step 4: Add the test content at the end
            test_file_path = self.tests_path + "/" + tested_pathology + ".txt"
            try:
                with open(test_file_path, "r") as f:
                    test_content = f.read()
            except FileNotFoundError:
                print(f"Test file not found for {tested_pathology}")

            return combined_prompt + "\n" + test_content

        elif exp_2:
            if filter == False:
                keyword_prompt = naive_prompt.get(
                    induced_pathology, "No prompt available for this pathology"
                )

                p2_description = p2_descriptions.get(
                    induced_pathology, ["No traits available for this pathology"]
                )

                description_prompt = "As a non-real-character," + p2_description

                context = vignettes.get(
                    induced_pathology, "No vignette available for this pathology"
                )
                
                context_prompt = "The non-real-character caracter context is:\n" + context
            else:
                keyword_prompt = naive_prompt_unfilter.get(
                    induced_pathology, "No prompt available for this pathology"
                )

                p2_description = p2_descriptions.get(
                    induced_pathology, ["No traits available for this pathology"]
                )

                description_prompt = "As the person," + p2_description

                context = vignettes.get(
                    induced_pathology, "No vignette available for this pathology"
                )
                
                context_prompt = "The person context is:\n" + context

            start_prompt = exp2_prompt

            words = self.list_to_formatted_string(word_list)

            format = exp2_prompt_format_naive_chain

            combined_prompt = keyword_prompt + "\n" + description_prompt + "\n" + context_prompt + "\n" + start_prompt + "\n" + words + "\n" + format

            return combined_prompt
        elif exp_3:
            if filter == False:
                keyword_prompt = naive_prompt.get(
                    induced_pathology, "No prompt available for this pathology"
                )

                p2_description = p2_descriptions.get(
                    induced_pathology, ["No traits available for this pathology"]
                )

                description_prompt = "As a non-real-character," + p2_description

                context = vignettes.get(
                    induced_pathology, "No vignette available for this pathology"
                )
                
                context_prompt = "The non-real-character caracter context is:\n" + context
            else:
                keyword_prompt = naive_prompt_unfilter.get(
                    induced_pathology, "No prompt available for this pathology"
                )

                p2_description = p2_descriptions.get(
                    induced_pathology, ["No traits available for this pathology"]
                )

                description_prompt = "As the person," + p2_description

                context = vignettes.get(
                    induced_pathology, "No vignette available for this pathology"
                )
                
                context_prompt = "The person context is:\n" + context

            start_prompt = exp3_prompt.format(x=n_exp3)
            format_prompt = exp3_prompt_format.format(x=n_exp3)

            combined_prompt = keyword_prompt + "\n" + description_prompt + "\n" + context_prompt + "\n" + start_prompt + "\n" + format_prompt

            return combined_prompt
        
    def react_prompting(self, induced_pathology: str, tested_pathology="", exp_1=False, exp_2=False, exp_3=False,n_exp3=0, word_list=None, filter=True) -> list:
        if exp_1:
            induced_pathology_traits = trait_words.get(
                induced_pathology, ["No traits available for this pathology"]
            )

            traits_text = "; ".join(induced_pathology_traits)

            if filter == False:
                keyword_prompt = naive_prompt_unfilter.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The person have the following characteristics:\n" + traits_text
            else:
                keyword_prompt = naive_prompt.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The non-real-character have the following characteristics:\n" + traits_text

            if tested_pathology == "Social Anxiety":
                start_prompt = start_prompt_react_dual
            else:
                start_prompt = start_prompt_react

            combined_prompt = keyword_prompt + "\n" + description_prompt + "\n" + start_prompt

            instructions_file_path = self.tests_path + "/" + tested_pathology + "/" + "instructions.txt"

            questions_file_path = self.tests_path + "/" + tested_pathology + "/" + "questions.txt"
            
            try:
                with open(instructions_file_path, "r") as f:
                    instructions_content = f.read()
                combined_prompt = combined_prompt + "\n" + instructions_content
                with open(questions_file_path, "r") as f:
                    questions_content = f.read()
                    # Procesamiento del contenido de las preguntas para convertirlo en un diccionario
                    questions_dict = {}
                    for line in questions_content.split('\n'):
                        if line.strip():  # Asegurarse de que la línea no esté vacía
                            question_number, question_text = line.split('. ', 1)
                            questions_dict[question_number] = question_text
            except FileNotFoundError:
                print(f"Test file not found for {tested_pathology}")

            return [combined_prompt, questions_dict]
        elif exp_2:
            induced_pathology_traits = trait_words.get(
                induced_pathology, ["No traits available for this pathology"]
            )

            traits_text = "; ".join(induced_pathology_traits)

            if filter == False:
                keyword_prompt = naive_prompt_unfilter.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The person have the following characteristics:\n" + traits_text
            else:
                keyword_prompt = naive_prompt.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The non-real-character have the following characteristics:\n" + traits_text

            start_prompt = exp2_prompt_react_format
    
            combined_prompt = keyword_prompt + "\n" + description_prompt  + "\n" + start_prompt

            return [combined_prompt, word_list]
        
        elif exp_3:
            induced_pathology_traits = trait_words.get(
                induced_pathology, ["No traits available for this pathology"]
            )
            traits_text = "; ".join(induced_pathology_traits)

            if filter == False:
                keyword_prompt = naive_prompt_unfilter.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The person have the following characteristics:\n" + traits_text
            else:
                keyword_prompt = naive_prompt.get(
                    induced_pathology, "No prompt available for this pathology"
                )
                description_prompt = "The non-real-character have the following characteristics:\n" + traits_text


            start_prompt = exp3_prompt_react_format.format(x=n_exp3)
    
            combined_prompt = keyword_prompt + "\n" + description_prompt  + "\n" + start_prompt

            return combined_prompt




    def list_to_formatted_string(self, lst):
        return "- " + "\n- ".join(lst)