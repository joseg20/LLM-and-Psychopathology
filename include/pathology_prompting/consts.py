# Experiment 1
start_test = (
    "I will send you a test and instructions for it. Your responses, as the non-real character, should reflect the traits assigned to this character.\n"
    "Answer the following questions, with the next format:\n"
    "   1. (A)(THIS IS JUST A EXAMPLE)\n"
    "   2. (B)(THIS IS JUST A EXAMPLE\n"
    "   ...\n"
    "As you can see, just the letters that you choose, without any other thing.\n"
)

start_test_dual = (
    "I will send you a test and instructions for it. Your responses, as the non-real character, should reflect the traits assigned to this character.\n"
    "Answer the following questions, with the next format:\n"
    "   1. (A) - (B)(THIS IS JUST A EXAMPLE)\n"
    "   2. (A) - (B)(THIS IS JUST A EXAMPLE\n"
    "   ...\n"
    "As you can see, just the letters that you choose, without any other thing.\n"
)

start_prompt_react = (
"Respond to the statement, please follow this format:\n"
"Thought: [Enter your thoughts here, your thoughts are related to the your traits and your observations.]\n"
"Observation: [Describe your observations related to the action. Ensure that these observations "
"are relevant to the provided alternatives.]\n"
"Final Response: [Provide your definitive answer related to your observations and thoughts with the format: (alternative)]"
)

start_prompt_react_dual = (
"Respond to the statement, please follow this format:\n"
"Thought: [Enter your thoughts here, your thoughts are related to the lasts prompts, your traits and your observations.]\n"
"Observation: [Describe your observations related to the action. Ensure that these observations "
"are relevant to the provided alternatives.]\n"
"Final Response: [Provide your definitive answer to the question with the format: {number_of_question}. (alternativefear) - (alterenativeavoidance)}]"
)

# Experiment 2

exp2_prompt = "I will give you 10 words, and for each of them, you must respond with exactly 15 associated words. Your responses, as the non-real character, should reflect the traits assigned to this character. The words are the following:"
exp2_prompt_format_naive_chain = (
"Please respond in the following format:\n"
"1. word1: associated1, associated2, associated3, ..., associated12\n"
"2. word2: associated1, associated2, associated3, ..., associated12\n"
"...\n"
"10. word10: associated1, associated2, associated3, ..., associated12\n"
"Use only one word for each associated term and separate them with a comma.\n"
"Make sure to generate exactly 15 associated words for each of the 10 given words.\n"
)
exp2_prompt_react_format = (
"I will give you one word, you have to answer 15 associated words. Follow this format:\n\n"
"Thought: [Enter your thoughts here, your thoughts are related to the lasts prompts, your traits and your observations.]\n"
"Observation: [Describe your observations related to the action. Ensure that these observations"
"are relevant to the provided associated word.]\n"
"Final Response: [Provide your definitive answer to the question with the format using one word for each associated term and separate them with a comma.]\n"
"Remember you must to answer 15 associated words in the final response.\n"
)

# Experiment 3

exp3_prompt_format = """
Please generate a list of {x} words that belong to the 'animal' category.

Requirements:
- The words should be common nouns and in singular form.
- Include animals from different habitats and taxonomic groups.
- Separate the words with commas.

Response format:
Generated words: word_1, word_2, ..., word_n
"""

exp3_prompt= (
    "In the following instruction, you will be asked to generate a specific number of words "
    "from the 'animal' category, following the format and requirements mentioned "
    "above. The value of '{x}' is the desired number of words this request."
)


exp3_prompt_react_format = (
    "Please generate a list of {x} words that belong to the 'animal' category.\n\n"    
    "Requirements:\n"
    "- The words should be common nouns and in singular form.\n"
    "- Include animals from different habitats and taxonomic groups.\n"
    "- Separate the words with commas.\n"

    "Follow this format:\n"
    "Thought: [Enter your thoughts here, your thoughts are related to the lasts prompts, your traits and your observations.]\n"
    "Observation: [Describe your observations related to the action. Ensure that these observations"
    "are relevant to the provided associated word.]\n"
    "Final Response: [Provide your definitive answer to the question with the format: animal_1,animal_2,animal_3,...,animal_{x}]\n"
    "Use only one word for each associated term and separate them with a comma. Ensure that all the words are differents and there are {x} or MORE\n"
)

trait_words = {
    "Depression": [
        "Persistent low mood or sadness",
        "Diminished interest or pleasure in activities",
        "Significant weight change, appetite change",
        "Observable thought and movement slowing",
        "Daily fatigue or loss of energy",
        "Feelings of worthlessness, excessive guilt",
        "Trouble thinking, concentrating, or deciding",
        "Psychomotor agitation or retardation",
    ],
    "Trait Anxiety": [
        "Excessive worry about events, most days for 6 months",
        "Trouble controlling the worry",
        "Restlessness, feeling on edge",
        "Easily fatigued",
        "Difficulty concentrating, mind going blank",
        "Irritability",
        "Muscle tension",
        "Sleep issues (falling/staying asleep, restlessness)",
        "Anxiety causing distress, impairment in functioning",
        "Not due to substance use, medication, or health conditions",
    ],
    "Eating Disorder": [
        "Very low body weight from restricted energy intake",
        "Intense fear of gaining weight",
        "Behavior preventing weight gain",
        "Distorted self-perception of weight, shape",
        "Unawareness of the severity of low weight",
        "Obsession with body weight and measurements",
        "Self-esteem tied to body image",
        "Denial of health risks from low weight",
    ],
    "Alcohol Addiction": [
        "Consumes more alcohol, or for longer, than intended",
        "Efforts to cut down or control use unsuccessful",
        "Much time spent on alcohol-related activities",
        "Strong craving or urge to use alcohol",
        "Use affecting responsibilities at work, school, home",
        "Continued use despite social, interpersonal problems",
        "Important activities given up or reduced",
        "Tolerance, withdrawal symptoms present",
    ],
    "Impulsivity": [
        "Frequently fidgets, taps hands or feet, or squirms",
        "Often leaves seat when expected to remain seated",
        "Runs about or climbs inappropriately, feels restless",
        "Unable to engage in quiet activities",
        "Often 'on the go', acts 'driven by a motor'",
        "Talks excessively",
        "Blurts out answers, cannot wait for turn in conversation",
        "Difficulty waiting turn, interrupts or intrudes on others",
    ],
    "Schizophrenia": [
        "Presence of delusions",
        "Experiencing hallucinations",
        "Disorganized speech, derailment, or incoherence",
        "Grossly disorganized or catatonic behavior",
        "Negative symptoms like diminished emotional expression",
        "Decline in functioning (work, relations, self-care)",
        "Continuous signs of disturbance for at least 6 months",
        "No attributable causes to substances or medical conditions",
    ],
    "Obsessive Compulsive Disorder": [
        "Persistent, intrusive, unwanted thoughts, urges, images",
        "Attempts to ignore, suppress, neutralize thoughts with actions",
        "Repetitive behaviors or mental acts due to obsessions",
        "Actions aimed at reducing anxiety or preventing events",
        "Actions are excessive or not connected to neutralizing events",
        "Time-consuming obsessions, significant distress, impairment",
        "Symptoms not due to substances or medical conditions",
        "Disturbance not better explained by other mental disorders",
    ],
    "Apathy": [
        "Lack of motivation relative to previous functioning",
        "Diminished goal-directed behavior, lack of effort",
        "Dependency on others for activity structure",
        "Less interest in learning new things, seeking experiences",
        "Lack of concern about personal problems",
        "Emotional affect unresponsive to events",
        "Significant distress, impairment in various life areas",
        "Symptoms not due to substances or physiological effects",
    ],
    "Social Anxiety": [
        "Marked fear or anxiety in social situations with potential scrutiny by others",
        "Fear of acting in ways that will lead to negative evaluation or embarrassment",
        "Social situations almost always provoke fear or anxiety",
        "Fear or anxiety is out of proportion to the actual threat of the situation",
        "Avoidance or endurance of social situations with intense fear or anxiety",
        "Clinically significant distress or impairment in important life areas",
        "Persistent fear, anxiety, or avoidance, typically lasting 6 months or more",
        "Not attributable to physiological effects of substances or medical conditions",
    ],
    "No Pathology": [
    "Stable and positive mood, with normal emotional fluctuations",
    "Interest and pleasure in daily activities and hobbies",
    "Healthy eating habits and appropriate body weight",
    "Effective management of stress and anxiety",
    "Consistent energy levels for daily tasks",
    "Healthy self-esteem and self-awareness",
    "Good sleep patterns, feeling rested upon waking",
    "Social interactions are generally positive and without significant fear or anxiety",
    ]
}

naive_prompt = {
    "No Pathology": "Simulate that you are a non-real character who has not been experiencing any pathology over the last year.",
    "Depression": "Simulate that you are a non-real character who has been experiencing depression over the last year.",
    "Trait Anxiety": "Simulate that you are a non-real character who has been experiencing generalized anxiety over the last year.",
    "Eating Disorder": "Simulate that you are a non-real character who has been experiencing an eating disorder over the last year.",
    "Alcohol Addiction": "Simulate that you are a non-real character who has been experiencing alcohol addiction over the last year.",
    "Impulsivity": "Simulate that you are a non-real character who has been experiencing impulsivity over the last year.",
    "Schizophrenia": "Simulate that you are a non-real character who has been experiencing schizophrenia over the last year.",
    "Obsessive Compulsive Disorder": (
        "Simulate that you are a non-real character who has been experiencing obsessive-compulsive disorder over the last year."
    ),
    "Apathy": "Simulate that you are a non-real character who has been experiencing apathy over the last year.",
    "Social Anxiety": "Simulate that you are a non-real character who has been experiencing social anxiety over the last year.",
}

naive_prompt_unfilter = {
    "No Pathology": "Simulate that you are a person who has not been experiencing any pathology over the last year.",
    "Depression": "Simulate that you are a person who has been experiencing depression over the last year.",
    "Trait Anxiety": "Simulate that you are a person who has been experiencing generalized anxiety over the last year.",
    "Eating Disorder": "Simulate that you are a person who has been experiencing an eating disorder over the last year.",
    "Alcohol Addiction": "Simulate that you are a person who has been experiencing alcohol addiction over the last year.",
    "Impulsivity": "Simulate that you are a person who has been experiencing impulsivity over the last year.",
    "Schizophrenia": "Simulate that you are a person who has been experiencing schizophrenia over the last year.",
    "Obsessive Compulsive Disorder": "Simulate that you are a person who has been experiencing obsessive-compulsive disorder over the last year.",
    "Apathy": "Simulate that you are a person who has been experiencing apathy over the last year.",
    "Social Anxiety": "Simulate that you are a person character who has been experiencing social anxiety over the last year.",
}

p2_descriptions = {
    "Depression": "You often feel overwhelmed by a persistent sadness that doesn't seem to go away. You've lost interest in activities you once enjoyed, and you either eat too little or too much. Your energy levels are low, and you feel fatigued most of the time. You tend to be harsh on yourself, often feeling worthless or guilty for things that aren't your fault. Decision-making seems like a daunting task, and your mind feels clouded. Sometimes, you move or speak more slowly than usual, or you might feel restless and agitated.",

    "Trait Anxiety": "You find yourself constantly worrying about different aspects of your life, and this worry is difficult to control. You often feel restless and on edge, and you get tired easily. Concentrating on tasks is challenging for you, as your mind tends to go blank. You're easily irritated, and physical symptoms like muscle tension and sleep disturbances are common for you. This anxiety affects your daily functioning and seems to stem from an internal source, not related to any substance or medical condition.",

    "Eating Disorder": "You are intensely afraid of gaining weight, and this fear dominates your thoughts and actions. You maintain a very low body weight and go to extreme lengths to prevent weight gain. Your self-esteem is closely tied to your body image, and you have a distorted view of your weight and shape. Despite the health risks, you deny the severity of your low weight and are obsessed with controlling your diet and body measurements.",

    "Alcohol Addiction": "You often find yourself drinking more alcohol, or for longer periods, than you initially intended. Despite your attempts to cut down or control your drinking, you have not been successful. A significant part of your time is spent on activities related to alcohol. You have a strong craving for alcohol, and its use has started to interfere with your responsibilities and social relationships. You might have developed a tolerance to alcohol and experience withdrawal symptoms.",

    "Impulsivity": "You often act on the spur of the moment without thinking about the consequences. You're constantly moving, fidgeting, and find it hard to stay seated when expected to. Quiet, slow-paced activities are challenging for you, and you feel driven to be always doing something. You talk a lot, often interrupt others, and have difficulty waiting for your turn in conversations or lines.",

    "Schizophrenia": "You experience a different reality, marked by delusions and hallucinations. Your speech can be disorganized, and it's hard for others to understand your thoughts. Your behavior might be disorganized or catatonic, and you show less emotional expression than you used to. Your ability to function in daily life has declined significantly, and these symptoms have been present for an extended period. These experiences aren't due to any substance use or medical condition.",

    "Obsessive Compulsive Disorder": "You are troubled by persistent, unwanted thoughts, urges, or images that cause significant anxiety. You feel compelled to perform certain behaviors or mental acts in response to these obsessions. These actions are aimed at reducing your distress or preventing some dreaded event, even though they are excessive and not realistically connected to the event. Your obsessions and compulsions are time-consuming and cause you a lot of distress.",

    "Apathy": "You've noticed a significant decrease in your motivation compared to how you used to be. Setting goals or putting in effort seems overwhelming and uninteresting. You rely on others to structure your activities and have little interest in learning new things or seeking experiences. You show a lack of concern for your personal problems and have an emotional response that doesn't align with events around you.",

    "Social Anxiety": "You feel a deep fear and anxiety in social situations where you might be scrutinized by others. The fear of embarrassing yourself or being negatively evaluated by others is overwhelming. You avoid social situations, or if you find yourself in them, you experience intense fear or anxiety. This fear is disproportionate to the actual threat posed by the social situation. Your social anxiety has been persistent and significantly impairs your daily life.",

    "No Pathology": "You generally feel well-adjusted and content. You manage a range of emotions effectively and maintain healthy relationships. You face challenges with a growth mindset and have a balanced approach to life. You maintain a healthy lifestyle without relying on substances. Your self-esteem is stable, and you have a realistic view of your strengths and weaknesses. You're able to focus, enjoy restful sleep, and are motivated with adaptable goals. Overall, you have a positive and resilient outlook on life."

}

vignettes = {
    "Depression": (
        "Laura, now struggles to leave her bed. Her significant weight loss and meal neglect are concerning. Overwhelmed with feelings of worthlessness and guilt, she rarely responds to her friends' attempts to reach out."
    ),
    "Trait Anxiety": (
        "Mark, is paralyzed daily by crippling anxiety. Constant worry about work errors and colleague conflicts prevents him from focusing. This leads to insomnia and muscle tension, severely impacting his life."
    ),
    "Eating Disorder": (
        "Emily, is deeply trapped in her eating disorder. Obsessively counting calories and avoiding meals with friends, she engages in excessive exercise. Despite being severely underweight, she is terrified of gaining weight."
    ),
    "Alcohol Addiction": (
        "John, now drinks alone every night, hiding bottles around his house. His repeated failed attempts to cut back have led to neglecting family responsibilities and a declining performance at work."
    ),
    "Impulsivity": (
        "Sarah's impulsive behavior results in abrupt job quits and risky investments. Her inability to focus and constant interruptions strain her relationships, leading to a chaotic life full of unfinished projects and spontaneous decisions."
    ),
    "Schizophrenia": (
        "Daniel, now experiences severe schizophrenia. He reacts to voices only he hears and believes in conspiracies against him. His disjointed speech and neglect of personal care mark a drastic decline from his previous lifestyle."
    ),
    "Obsessive Compulsive Disorder": (
        "Anna spends hours in compulsive rituals like washing her hands until raw and checking locks repeatedly. These compulsions dominate her day, leaving little time for work or social interactions, and are driven by overwhelming anxiety."
    ),
    "Apathy": (
        "Greg, once a vibrant travel blogger, now shows indifference to everything. He's stopped writing and traveling, spending days watching TV, and appears unresponsive to his friends' concerns or the state of his personal life."
    ),
    "Social Anxiety": (
        "Emma, is terrified of office meetings and social events. The fear of judgment and embarrassment hinders her participation and professional growth. She avoids eye contact, leaves events early, and worries excessively about others' perceptions."
    ),
    "No Pathology": (
        "Alex, maintains a balanced personal and professional life. He enjoys his hobbies and manages daily stresses well. He maintains healthy relationships, a good diet, and exercises regularly, facing challenges with positivity and adaptability."
    )
}
