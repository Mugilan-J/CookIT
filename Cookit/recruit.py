import os
import google.generativeai as genai
import PyPDF2

# Configure Gemini API
genai.configure(api_key="AIzaSyB3wWo9ek9OdBrkqzZZPy-8ih0lWBU-JWc")


class ArtificialRecruiter:
    def __init__(self):
        self.resume_text = ""
        self.role = ""
        self.questions = []
        self.score = 0
        self.feedback = []

    def upload_resume(self):
        file_path = input("Please upload your resume (PDF format): ").strip()
        if not os.path.exists(file_path):
            print("File not found. Please try again.")
            return

        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                self.resume_text = " ".join(page.extract_text() for page in reader.pages)
                print("Resume uploaded and text extracted successfully!")
        except Exception as e:
            print("Error reading resume:", e)
            return

        self.role = input("Enter the role you are applying for: ").strip()
        self.generate_questions()

    def generate_questions(self):
        print("\nGenerating interview questions...")
        try:
            prompt = f"Generate 20 unique interview questions for the role: {self.role}"
            response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(prompt)
            self.questions = response.content.split("\n") if hasattr(response, "content") else []

            if not self.questions:
                print("No questions generated. Please try again.")
        except Exception as e:
            print("Error generating questions:", e)

    def conduct_interview(self):
        if not self.questions:
            print("No questions available for the interview.")
            return

        print("\nStarting the virtual interview...\n")
        for i, question in enumerate(self.questions, start=1):
            print(f"Question {i}: {question}")
            answer = input("Your Answer: ").strip().lower()
            self.evaluate_answer(answer, question)

    def evaluate_answer(self, answer, question):
        # Example scoring logic
        correct_keywords = ["html", "css", "javascript"]  # Replace with relevant keywords per role
        if any(keyword in answer for keyword in correct_keywords):
            print("Correct Answer!")
            self.score += 10
        else:
            print("Incorrect Answer.")
            self.score -= 5
            self.feedback.append(
                f"Question: {question}\nExpected: Mention keywords like {', '.join(correct_keywords)}\n"
            )

    def final_evaluation(self):
        print("\nFinal Evaluation")
        print(f"Your Score: {self.score}")
        if self.score > 50:  # Example threshold for passing
            print("Result: Recruited!")
        else:
            print("Result: Not Recruited.")

        print("\nFeedback:")
        if self.feedback:
            for item in self.feedback:
                print(item)
        else:
            print("Great job! No specific feedback.")

    def run(self):
        print("Welcome to Artificial Recruiter!")
        self.upload_resume()
        self.conduct_interview()
        self.final_evaluation()


if __name__ == "__main__":
    recruiter = ArtificialRecruiter()
    recruiter.run()
