import tkinter as tk
import random
import time

paragraphs = [
    "The sun dipped below the horizon, casting a golden hue over the small coastal town. As the waves gently lapped against the shore, the calm evening air carried the faint melody of a guitar, creating a peaceful atmosphere. Families gathered around campfires, sharing stories and laughter, while children played along the sandy beach, their joyful shrieks mingling with the sounds of the ocean.",
    "In the heart of the bustling city, amidst the incessant hum of traffic and the vibrant chatter of pedestrians, stood an old bookstore. Its shelves, laden with books of all ages and genres, held stories waiting to be told. The musty aroma of aged paper filled the air, inviting passersby to step in and lose themselves in a world crafted by words. Each corner of the store was a treasure trove of knowledge, history, and endless imagination.",
    "As the storm approached, the once clear sky turned a menacing shade of grey. Thunder rumbled in the distance, sending vibrations through the ground. Lightning flashed, briefly illuminating the landscape, revealing trees swaying violently in the wind. The air grew thick with anticipation, and the first raindrops began to fall, slowly at first, then quickly becoming a torrential downpour that drummed loudly on rooftops.",
    "The festival was a kaleidoscope of colors, sounds, and aromas. Street vendors lined the pathways, offering exotic foods and handmade crafts. Performers in bright costumes danced to rhythmic beats, captivating the audience with their fluid movements. Children ran around with painted faces, and the air was filled with the sweet scent of blooming flowers and spicy street food, creating a lively and enchanting atmosphere.",
    "Amidst the serene beauty of the mountain range, a narrow trail wound its way up the steep slopes. Hikers, equipped with backpacks and walking sticks, ascended the path, their eyes fixed on the summit. The air was crisp and fresh, occasionally pierced by the call of a distant bird. With each step, the view expanded, revealing sprawling forests and rugged terrain below, bathed in the soft light of the morning sun.",
    "The library was a haven of silence and study. Rows of desks were occupied by students and researchers, their heads bowed over books and laptops. The soft rustling of pages and the occasional click of a keyboard were the only sounds that disturbed the quiet. Large windows let in natural light, illuminating the rows of bookshelves that held volumes of academic journals, classic literature, and modern novels.",
    "At the edge of the lake, the water was still, mirroring the clear blue sky and fluffy white clouds above. Ducks glided gracefully across the surface, occasionally dipping their heads underwater. Families picnicked on the grassy banks, enjoying the warm sun and gentle breeze. Children laughed as they chased each other, occasionally stopping to throw stones into the water, watching the ripples expand and fade.",
    "The art gallery was a quiet space filled with the soft footsteps of visitors who moved from one exhibit to another. The walls were adorned with paintings and sculptures from various eras, each piece telling its own story. The lighting was carefully arranged to highlight the colors and textures of the artworks, drawing viewers into the depths of the artists’ imaginations.",
    "As night fell, the city skyline came alive with lights. Skyscrapers glowed against the darkening sky, their windows shimmering like stars. The streets buzzed with activity as people made their way to restaurants, theaters, and bars. The night was vibrant with the promise of adventures and stories yet to unfold, as the city embraced the darkness with a display of dazzling lights.",
    "The conference room buzzed with the low murmur of conversations as professionals from around the world gathered. Charts and graphs were displayed on screens, illustrating points of discussion. Participants exchanged ideas and debated strategies, their voices occasionally rising in passion. The atmosphere was charged with the energy of collaboration and the potential for new partnerships and innovations."
]

current_paragraph = ""
start_time = None
timer_id = None
paused_time = 0


def update_timer():
    global start_time, timer_id, paused_time
    if start_time:
        elapsed_time = time.time() - start_time
        minutes = elapsed_time / 60
        num_words = len(typing_area.get("1.0", "end-1c").strip().split())
        wpm = (num_words / minutes) if minutes > 0 else 0
        timer_label.config(text=f"Time: {elapsed_time:.2f} sec, WPM: {wpm:.2f}")
        timer_id = root.after(1000, update_timer)
    else:
        timer_label.config(text="Timer stopped.")


def on_text_change(event=None):
    global start_time
    user_text = typing_area.get("1.0", "end-1c")
    if user_text.endswith("\n"):
        user_text = user_text[:-1]

    if start_time is None and user_text:  # Start the timer on the first character typed
        start_time = time.time()
        update_timer()

    # Update only if all characters are correct so far
    if user_text == current_paragraph[:len(user_text)]:
        if len(user_text) == len(current_paragraph):
            root.after_cancel(timer_id)  # Stop updating the timer
            time_taken = time.time() - start_time
            minutes = time_taken / 60
            num_words = len(user_text.split())
            wpm = num_words / minutes
            result_label.config(text=f"All correct! WPM: {wpm:.2f}", fg="green")
            timer_label.config(text=f"Time: {time_taken:.2f} sec, Final WPM: {wpm:.2f}")
        else:
            result_label.config(text="Correct so far...", fg="green")
    else:
        result_label.config(text="Error detected! Keep trying.", fg="red")

def display_random_paragraph():
    global current_paragraph, start_time, timer_id
    current_paragraph = random.choice(paragraphs)
    typing_area.delete("1.0", tk.END)
    start_time = None  # Reset start time
    if timer_id:
        root.after_cancel(timer_id)  # Cancel the previous timer updates

    # Clear the canvas and create new text
    canvas.delete("all")
    canvas.create_text(
        10, 10,
        anchor="nw",
        text=current_paragraph,
        font="Helvetica 14",
        width=480,
        fill="black"  # Ensure the text color is black (or any color you prefer)
    )
    timer_label.config(text="Start typing...")
    result_label.config(text="Start typing...", fg="black")


def setup_text_modified_event(text_widget):
    """ Set up an event trigger on text modification in a Tkinter Text widget """
    def _on_change(event):
        text_widget.edit_modified(False)  # immediately reset the modified flag
        on_text_change(event)

    text_widget.bind("<<Modified>>", _on_change)


def toggle_timer():
    global timer_id, start_time, paused_time
    if timer_id:
        # Pausing the timer
        root.after_cancel(timer_id)
        paused_time = time.time() - start_time  # Store the paused duration
        num_words = len(typing_area.get("1.0", "end-1c").strip().split())
        minutes = paused_time / 60
        wpm = (num_words / minutes) if minutes > 0 else 0
        timer_label.config(text=f"Paused at {paused_time:.2f} sec, WPM: {wpm:.2f}")
        button_end.config(text="Resume Test")
        timer_id = None
    else:
        # Resuming the timer
        if paused_time is not None:
            start_time = time.time() - paused_time  # Adjust start_time to account for the paused duration
            update_timer()
            timer_label.config(text=f"Resuming at {paused_time:.2f} sec, WPM: {wpm:.2f}")
            button_end.config(text="Pause Test")


# Set up the main window
root = tk.Tk()
root.title("Typing Speed Test")

# Setup the Canvas
canvas = tk.Canvas(root, width=500, height=200)
canvas.pack(pady=20)

# Typing area
typing_area = tk.Text(root, height=8, width=60, font="Helvetica 14", wrap="word")
typing_area.pack(pady=(5, 20))
setup_text_modified_event(typing_area)

# Button to change the paragraph
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
new_paragraph_button = tk.Button(button_frame, text="New Paragraph", command=display_random_paragraph)
new_paragraph_button.pack(side=tk.LEFT)

button_end = tk.Button(button_frame, text="Pause Test", command=toggle_timer)
button_end.pack(side=tk.RIGHT)

# Timer and WPM label
timer_label = tk.Label(root, text="Ready to type...", font="Helvetica 14")
timer_label.pack()

# Result label
result_label = tk.Label(root, text="Start typing...", font="Helvetica 14")
result_label.pack()

# Initially display a random paragraph
display_random_paragraph()

root.mainloop()
