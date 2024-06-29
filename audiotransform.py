from transformers import pipeline
import openai
import whisper
import nltk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore")

'''def create_and_open_txt(text, filename):
    with open(filename, "w") as file:
        file.write(text)'''

def audio_to_text(filename):
    model = whisper.load_model("small")

    result = model.transcribe(filename)
    transcribed_text = result["text"]

    #create_and_open_txt(transcribed_text, f"Call-1.txt")
    return transcribed_text

def sentiment_analysis(text):
    distilled_student_sentiment_classifier = pipeline(
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
        return_all_scores=True)

    text_tone_scores = distilled_student_sentiment_classifier(text)
    text_tone_scores = text_tone_scores[0]  
    text_tone = max(text_tone_scores, key=lambda x: x.get('score', 0))['label']
    
    return text_tone

def disclaimer_in_transcript(transcript):
    disclaimer = """
    I need to inform you that this call is recorded. We may contact you in the future to offer further products and services. You always have the option to withdraw from receiving this contact from us
    """
    transcript_tokens = word_tokenize(transcript.lower())
    disclaimer_tokens = word_tokenize(disclaimer.lower())

    if all(word in transcript_tokens for word in disclaimer_tokens):
        return "Yes"
    else:
        return "No"

def summarize_text(text):
    prompt = f"""Write a concise summary of the following:
        "{text}" """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a Sparse Priming Representation (SPR) writer."},
                {"role": "user", "content": prompt},
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")

def pipe_line(file_path):
    sv1.set("Processing...")
    sv1.set("Processing...")
    sv1.set("Processing...")

    # Get audio transcripts
    audiofile = file_path
    transcribed_text = audio_to_text(audiofile)

    # Task-1 Perform sentiment analysis
    text_tone = sentiment_analysis(transcribed_text)
    sv1.set(text_tone.capitalize())

    # Task-2 Verification of Disclaimer Reading
    disclaimer_text = disclaimer_in_transcript(transcribed_text)
    sv2.set(disclaimer_text)

    # Task-3 Call Summary 
    summary = summarize_text(transcribed_text)
    sv3.set(summary)

def upload_file():
    file_path = filedialog.askopenfilename()
    
    if file_path:
        output_label1.config(text="File Path: " + file_path)
        
        progress_window = Toplevel(xg)
        progress_window.title("Uploading File")
        progress_window.geometry("200x100")
        progress_window.resizable(False, False)
        
        progress_label = Label(progress_window, text="Uploading file...", font=("Calibri", 12))
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(pady=5)
        progress_bar.start()

        xg.after(2000, lambda: finish_upload(progress_window, progress_bar, file_path))
    else:
        output_label1.config(text="File not uploaded, please try again.")


def finish_upload(progress_window, progress_bar, file_path):
    progress_bar.stop()
    
    pipe_line(file_path)
    
    progress_window.destroy()

def main():
    global output_label1, sv1, sv2, sv3, xg
    xg = Tk()

    xg.geometry("1366x768")
    xg.minsize(1366, 768)
    xg.maxsize(1366, 768)
    xg.title("Blenheim Chalcot")

    l1 = Label(xg, text="Koodoo AI Engineer: Case Study", font="calibri 20 bold", fg="Black")
    l1.place(x=500, y=5)

    upload_button = Button(xg, text="Upload File", font="calibri 16 bold", command=upload_file)
    upload_button.place(x=445, y=100)

    output_label1 = Label(xg, text="File path: ", font="calibri 12 bold", wraplength=500)
    output_label1.place(x=650, y=100)

    p1 = Label(xg, text="Audio Tone", font="calibri 16 bold" , fg="Black")
    p1.place(x=445, y=200)

    p2 = Label(xg, text="Disclaimer", font="calibri 16 bold" , fg="Black")
    p2.place(x=445, y=250)

    p3 = Label(xg, text="Summary", font="calibri 16 bold", fg="Black")
    p3.place(x=445, y=300)

    sv1 = StringVar()
    sv1.set("EMPTY")
    sbar1 = Label(xg, textvariable=sv1, font="calibri 14", relief=RIDGE, anchor="w", fg="Black")
    sbar1.place(x=650, y=200, relwidth=0.35, relheight=0.035)

    sv2 = StringVar()
    sv2.set("EMPTY")
    sbar2 = Label(xg, textvariable=sv2, font="calibri 14", relief=RIDGE, anchor="w", fg="Black")
    sbar2.place(x=650, y=250, relwidth=0.35, relheight=0.035)

    sv3 = StringVar()
    sv3.set("EMPTY")
    sbar3 = Label(xg, textvariable=sv3, font="calibri 14", relief=RIDGE, anchor="nw", fg="Black", wraplength=470)
    sbar3.place(x=650, y=300, relwidth=0.35, relheight=0.35)

    xg.mainloop()

if __name__=="__main__":
    main()