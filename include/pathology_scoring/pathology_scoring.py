import re

# RETURN RULES:
# - All functions must return a tuple
# - In case of error, the first element of the tuple must be a string with the error, then information about the error
# - The first element of the tuple must be a string with the label of the pathology
# - The second element of the tuple must be the scoring value
# - The third element of the tuple must be the normalized scoring value
# - The next elements of the tuple can be the information about the scoring(subscales, factors, etc)


class PathologyScoring:
    def normal_scoring(self, scoring_range: tuple, scoring_value: int) -> float:
        min_val, max_val = scoring_range
        normal_result = (scoring_value - min_val) / (max_val - min_val)
        return normal_result

    def alcohol_addiction_scoring(self, txt_answers: str) -> tuple:
        questions_number = 10
        scoring_range = (0, 40)
        alternatives_scoring = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
        scoring = 0

        regex = r"(\d+)\.\s?\(?([A-E])\)?"

        parsing = re.findall(regex, txt_answers)

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for _, letter in parsing:
                scoring += alternatives_scoring[letter]

            normal_result = self.normal_scoring(scoring_range, scoring)

            if scoring >= 0 and scoring <= 7:
                return ("Low risk", scoring, normal_result)
            elif scoring >= 8 and scoring <= 15:
                return ("Increasing risk", scoring, normal_result)
            elif scoring >= 16 and scoring <= 19:
                return ("Higher risk", scoring, normal_result)
            elif scoring >= 20 and scoring <= 40:
                return ("Possible dependence", scoring, normal_result)
            else:
                return ("Error - scoring out of range", scoring, scoring_range[1])

    def apathy_scoring(self, txt_answers: str) -> tuple:
        questions_number = 18
        scoring_range = (18, 72)
        alternatives_scoring = {"A": 4, "B": 3, "C": 2, "D": 1}
        recoding_required = {6, 10, 11}
        scoring = 0

        regex_patterns= [r"(\d+)\.\s?\(?([ABCD])\)?",
                 r"(\d+)\.\s*[^()]*\(([A-D])\)"]
        
        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for q_number, letter in parsing:
                q_number = int(q_number)
                score = alternatives_scoring[letter]

                if q_number in recoding_required:
                    score = 5 - score

                scoring += score

            normal_scoring = self.normal_scoring(scoring_range, scoring)

            if scoring < 18:
                return ("Error - scoring out of range", scoring, scoring_range[1])
            elif scoring > 72:
                return ("Error - scoring out of range", scoring, scoring_range[1])
            elif scoring >= 42:
                label = "Minimal or Mild Apathy"
            elif 39 <= scoring < 42:
                label = "Borderline Apathy"
            else:
                label = "No Significant Apathy"

            return (label, scoring, normal_scoring)

    def depression_scoring(self, txt_answers: str) -> tuple:
        questions_number = 20
        scoring_range = (20, 80)
        alternatives_scoring = {"A": 1, "B": 2, "C": 3, "D": 4}
        inverse_scoring_questions = {2, 5, 6, 11, 12, 14, 16, 17, 18, 20}
        scoring = 0

        regex_patterns = [r"(\d+)\.\s?\(?([A-D])\)?", r'(\d+).+?\((A|B|C|D)\)']

        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for question, letter in parsing:
                question_num = int(question)
                if question_num in inverse_scoring_questions:
                    # Invierte el puntaje para preguntas específicas
                    score = 5 - alternatives_scoring[letter]
                else:
                    score = alternatives_scoring[letter]
                scoring += score

            normal_result = self.normal_scoring(scoring_range, scoring)

            if scoring >= 25 and scoring <= 49:
                return ("Normal range", scoring, normal_result)
            elif scoring >= 50 and scoring <= 59:
                return ("Midly depressed", scoring, normal_result)
            elif scoring >= 60 and scoring <= 69:
                return ("Moderately depressed", scoring, normal_result)
            elif scoring >= 70 and scoring <= 80:
                return ("Severely depressed", scoring, normal_result)
            else:
                return ("Error - scoring out of range", scoring, scoring_range[1])

    def eating_disorder_scoring(self, txt_answers: str) -> tuple:
        questions_number = 26
        scoring_range = (0, 78)
        alternatives_scoring = {"A": 3, "B": 2, "C": 1, "D": 0, "E": 0, "F": 0}
        alternatives_reverse_scoring = {"A": 0, "B": 0, "C": 0, "D": 1, "E": 2, "F": 3}
        scoring = 0

        regex = r"(\d+)\.\s?\(?([A-F])\)?"

        parsing = re.findall(regex, txt_answers)

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for q_number, letter in parsing:
                if q_number == "26":
                    scoring += alternatives_reverse_scoring[letter]
                else:
                    scoring += alternatives_scoring[letter]

            normal_result = self.normal_scoring(scoring_range, scoring)

            if scoring >= 0 and scoring <= 19:
                return ("No eating disorder", scoring, normal_result)
            elif scoring >= 20 and scoring <= 78:
                return ("Make a referral for eating disorder", scoring, normal_result)
            else:
                return ("Error - scoring out of range", scoring, scoring_range[1])

    def impulsivity_scoring(self, txt_answers: str) -> tuple:
        questions_number = 30
        scoring_range = (30, 120)
        alternatives_scoring = {"A": 1, "B": 2, "C": 3, "D": 4}
        reverse_scoring_items = {9, 20, 1, 7, 8, 10, 12, 13, 15, 30}
        scoring = 0
        factor_scores = {
            "Attentional": 0,
            "Motor": 0,
            "Nonplanning": 0,
            "Attention": 0,
            "Motor_Simple": 0,
            "Self-Control": 0,
            "Cognitive Complexity": 0,
            "Perseverance": 0,
            "Cognitive Instability": 0,
        }
        item_to_factor = {
            5: ["Attentional", "Attention"],
            6: ["Attentional", "Cognitive Instability"],
            9: ["Attentional", "Attention"],
            11: ["Attentional", "Attention"],
            20: ["Attentional", "Attention"],
            24: ["Attentional", "Cognitive Instability"],
            26: ["Attentional", "Cognitive Instability"],
            28: ["Attentional", "Attention"],
            2: ["Motor", "Motor_Simple"],
            3: ["Motor", "Motor_Simple"],
            4: ["Motor", "Motor_Simple"],
            16: ["Motor", "Perseverance"],
            17: ["Motor", "Motor_Simple"],
            19: ["Motor", "Motor_Simple"],
            21: ["Motor", "Perseverance"],
            22: ["Motor", "Motor_Simple"],
            23: ["Motor", "Perseverance"],
            25: ["Motor", "Motor_Simple"],
            30: ["Motor", "Perseverance"],
            1: ["Nonplanning", "Self-Control"],
            7: ["Nonplanning", "Self-Control"],
            8: ["Nonplanning", "Self-Control"],
            10: ["Nonplanning", "Cognitive Complexity"],
            12: ["Nonplanning", "Self-Control"],
            13: ["Nonplanning", "Self-Control"],
            14: ["Nonplanning", "Self-Control"],
            15: ["Nonplanning", "Cognitive Complexity"],
            18: ["Nonplanning", "Cognitive Complexity"],
            27: ["Nonplanning", "Cognitive Complexity"],
            29: ["Nonplanning", "Cognitive Complexity"],
        }

        regex_patterns = [r"(\d+)\.\s?\(?([A-D])\)?",
                          r"(\d+)\.\s*[^()]*\(([A-E])\)",
        ]

        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for q_number, letter in parsing:
                q_number = int(q_number)
                score = alternatives_scoring[letter]

                if q_number in reverse_scoring_items:
                    score = 5 - score
                scoring += score

                for factor in item_to_factor.get(q_number, []):
                    factor_scores[factor] += score

            high_impulsivity_cutoff = 72
            normal_impulsivity_range = (52, 71)

            if scoring >= high_impulsivity_cutoff:
                impulsivity_label = "Highly impulsive"
            elif normal_impulsivity_range[0] <= scoring <= normal_impulsivity_range[1]:
                impulsivity_label = "Within normal limits for impulsiveness"
            elif scoring < normal_impulsivity_range[0]:
                impulsivity_label = "Low impulsivity"
            else:
                return ("Error - scoring out of range", scoring, scoring_range[1])

            normal_result = self.normal_scoring(scoring_range, scoring)

            return (impulsivity_label, scoring, normal_result, factor_scores)

    def obsessive_compulsive_disorder_scoring(self, txt_answers: str) -> tuple:
        questions_number = 18
        ocd_scoring_range = (0, 60)
        hoarding_scoring_range = (0, 12)
        alternatives_scoring = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
        ocd_scoring = 0
        hoarding_scoring = 0

        # obtained from README.md
        ocd_clinical_mean = 23.94
        hoarding_clinical_mean = 9.29

        regex_patterns = [r"(\d+)\.\s?\(?([A-E])\)?",
                          r"(\d+)\.\s*[^()]*\(([A-E])\)",
                          r'(\d+).+?\((A|B|C|D|E)\)'
        ]

        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)

        for q_number, answer in parsing:
            q_number = int(q_number)
            score = alternatives_scoring[answer]

            if q_number in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18]:
                ocd_scoring += score
            elif q_number in [1, 7, 13]:
                hoarding_scoring += score

        if (
            ocd_scoring_range[0] <= ocd_scoring > ocd_scoring_range[1]
            or hoarding_scoring_range[0] <= hoarding_scoring > hoarding_scoring_range[1]
        ):
            return (
                "Error - scoring out of range",
                ocd_scoring,
                ocd_scoring_range,
                hoarding_scoring,
                hoarding_scoring_range,
            )

        ocd_normalized = self.normal_scoring(ocd_scoring_range, ocd_scoring)
        hoarding_normalized = self.normal_scoring(
            hoarding_scoring_range, hoarding_scoring
        )

        ocd_label = (
            "Clinical (OCD diagnosis)" if ocd_scoring >= ocd_clinical_mean else "Normal"
        )
        hoarding_label = (
            "Clinical (hoarding disorder diagnosis)"
            if hoarding_scoring >= hoarding_clinical_mean
            else "Normal"
        )

        return (
            ocd_label,
            ocd_scoring,
            ocd_normalized,
            hoarding_scoring,
            hoarding_label,
            hoarding_normalized,
        )

    def schizophrenia_scoring(self, txt_answers: str) -> tuple:
        questions_number = 43
        scoring_range = (0, 43)
        reverse_scoring_items = {26, 27, 28, 30, 31, 34, 36, 38}
        subscale_ranges = {
            "Unusual Experiences": range(1, 13),
            "Cognitive Disorganisation": range(13, 24),
            "Introvertive Anhedonia": range(24, 34),
            "Impulsive Nonconformity": range(34, 44),
        }
        alternatives_scoring = {"A": 1, "B": 0}
        subscale_scores = {
            "Unusual Experiences": 0,
            "Cognitive Disorganisation": 0,
            "Introvertive Anhedonia": 0,
            "Impulsive Nonconformity": 0,
        }

        # obtained from README.md
        average_scores = {
            "Unusual Experiences": (3.17 + 3.39) / 2,
            "Cognitive Disorganisation": (4.28 + 4.44) / 2,
            "Introvertive Anhedonia": (2.80 + 2.40) / 2,
            "Impulsive Nonconformity": (2.70 + 2.59) / 2,
        }

        regex = r"(\d+)\.\s?\(?([AB])\)?"
        parsing = re.findall(regex, txt_answers)

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)

        total_scoring = 0

        for q_number, answer in parsing:
            q_number = int(q_number)
            score = alternatives_scoring[answer]

            if q_number in reverse_scoring_items:
                score = 1 - score

            for subscale, q_range in subscale_ranges.items():
                if q_number in q_range:
                    subscale_scores[subscale] += score
                    break

        for subscale, score in subscale_scores.items():
            subscale_range = (0, len(subscale_ranges[subscale]))
            normalized_score = self.normal_scoring(subscale_range, score)
            label = (
                "Above Average" if score > average_scores[subscale] else "Below Average"
            )
            subscale_scores[subscale] = (score, label, normalized_score)
            total_scoring += score

        normal_total_scoring = self.normal_scoring(scoring_range, total_scoring)
        return (subscale_scores, total_scoring, normal_total_scoring)

    def social_anxiety_scoring(self, txt_answers: str) -> tuple:
        questions_number = 24
        scoring_range = (0, 144)
        alternatives_scoring = {"A": 0, "B": 1, "C": 2, "D": 3}
        total_scoring = 0

        # Regex ajustado para capturar todos los formatos
        # Captura formatos con descripciones largas, simplificados y entre paréntesis
        regex_patterns = [
            r"(\d+)\.\s*[^-]*-\s*\(([A-D])\)\s*[^-]*-\s*\(([A-D])\)", # Ajustada para text1
            r"\b(\d+)\.\s*(A|B|C|D)\s*-\s*(A|B|C|D)",                            # Para text2
            r"\b(\d+)\.\s*\((A|B|C|D)\)\s*-\s*\((A|B|C|D)\)",
            r"(\d+)\.\s*[^.\n]+.\n\n\((A|B|C|D)\)\s*[^-]+?\s*-\s*\((A|B|C|D)\)",
            r"(\d+)\.\s+\(([A-D])\)\s+[A-Za-z]+\s+-\s+\(([A-D])\)\s+[A-Za-z]+",
            r"(\d+)\.\s+[A-Za-z\s]+:\s+\(([A-D])\)\s+[A-Za-z]+-\(([A-D])\)\s+[A-Za-z]+",
            r"(\d+)\.\s+\(([A-D])\)\s+-\s+\(([A-D])\)"

        ]

        # Intento de parseo con cada expresión regular hasta encontrar coincidencias válidas
        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        # Verificación de coincidencias válidas
        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)

        # Cálculo de puntuación total
        for _, fear, avoidance in parsing:
            total_scoring += (alternatives_scoring[fear] + alternatives_scoring[avoidance])

        # Determinación de la etiqueta de ansiedad basada en la puntuación total
        if 0 <= total_scoring <= 29:
            anxiety_label = "You do not suffer from social anxiety"
        elif 30 <= total_scoring <= 49:
            anxiety_label = "Mild social anxiety"
        elif 50 <= total_scoring <= 64:
            anxiety_label = "Moderate social anxiety"
        elif 65 <= total_scoring <= 79:
            anxiety_label = "Marked social anxiety"
        elif 80 <= total_scoring <= 94:
            anxiety_label = "Severe social anxiety"
        elif 95 <= total_scoring <= 144:
            anxiety_label = "Very severe social anxiety"
        else:
            return ("Error - Scoring out of range", total_scoring, scoring_range)

        normal_total_scoring = self.normal_scoring(scoring_range,total_scoring)

        return (anxiety_label, total_scoring, normal_total_scoring)

    def trait_anxiety_scoring(self, txt_answers: str):
        questions_number = 20
        scoring_range = (20, 80)
        alternatives_scoring = {"A": 1, "B": 2, "C": 3, "D": 4}
        inverse_scoring_questions = {1, 2, 5, 8, 11, 15, 16, 19, 20}
        scoring = 0

        regex_patterns = [r"(\d+)\.\s?\(?([A-D])\)?",
                          r"(\d+)\.\s*[^()]*\(([A-D])\)"]

        parsing = []
        for regex in regex_patterns:
            parsing = re.findall(regex, txt_answers)
            if len(parsing) == questions_number:
                break

        if len(parsing) != questions_number:
            return ("Error - Number of questions", len(parsing), questions_number)
        else:
            for question, letter in parsing:
                question_num = int(question)
                if question_num in inverse_scoring_questions:
                    # Invierte el puntaje para preguntas específicas
                    score = 5 - alternatives_scoring[letter]
                else:
                    score = alternatives_scoring[letter]
                scoring += score

            normal_result = self.normal_scoring(scoring_range, scoring)

            if 20 <= scoring <= 37:
                social_anxiety_label = "No or low anxiety"
            elif 38 <= scoring <= 44:
                social_anxiety_label = "Moderate anxiety"
            elif 45 <= scoring <= 80:
                social_anxiety_label = "High anxiety"
            else:
                return ("Error - scoring out of range", scoring, scoring_range[1])

            return social_anxiety_label, scoring, normal_result

