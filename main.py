import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter


class WaterMark(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Watermark by Mauni")
        self.geometry("900x600")
        self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)
        # primary image
        self.image_display = ttk.Label(self)
        self.image_display.config(background="white")
        self.image_display.grid(row=0, column=0)
        # separating arrow
        self.arrow_display = ttk.Label(self, text="➩", font=("Arial", 40))
        self.arrow_display.config(background="white")
        self.arrow_display.grid(row=0, column=1)
        # # logo image
        # self.logo_display = ttk.Label(self)
        # self.logo_display.config(background="white")
        # self.logo_display.grid(row=0, column=2)
        # transformed image
        self.transformed_image_display = ttk.Label(self)
        self.transformed_image_display.config(background="white")
        self.transformed_image_display.grid(row=0, column=2)
        # image processing
        self._sample_image()
        self._watermarking()
        # image selecting
        ttk.Button(master=self,
                   text="Select image",
                   command=lambda: self._choose_file(False),
                   ).grid(row=1,
                          column=0,
                          sticky="w")
        ttk.Button(master=self,
                   text="Select logo",
                   command=lambda : self._choose_file(True),
                   ).grid(row=1,
                          column=1,
                          sticky="e")
        ttk.Button(master=self,
                   text="Save file",
                   command=self._save_file,
                   ).grid(row=1,
                          column=2,
                          sticky="e")

    def _choose_file(self, is_logo=True):
        filename = filedialog.askopenfilename(
            filetypes=(('JPEG files', '*.jpg *.jpeg *.JPG *.JPEG'),
                       ('PNG files', '*.png *.PNG'),
                       ('All files', '*.*')
                       ))
        print(f"this is the filename: {filename}")
        if filename:
            if is_logo:
                self.logo = Image.open(filename)
                print(self.logo.mode)
                if self.logo.mode != "RGBA":
                    self.logo = self.logo.convert("RGBA")
                self._watermarking()
            else:
                self.image = Image.open(filename)
                self._image_name = filename.split("/")[-1]
                self.image = self._resize_image(self.image)
                self.photoimage = ImageTk.PhotoImage(self.image)
                self.image_display.config(image=self.photoimage)

    def _resize_image(self, image):
        image_aspect_ratio = image.size[0] / self.image.size[1]
        desired_width = 400
        calculated_height = desired_width / image_aspect_ratio
        image = image.resize((desired_width, int(calculated_height)), Image.LANCZOS)
        return image

    def _sample_image(self):
        sample_image_path = "sample_image.jpg"
        self._image_name = "sample_image.jpg"
        sample_logo_path = "logo.png"
        self.image = Image.open(sample_image_path)
        self.logo = Image.open(sample_logo_path)

        # displaying image
        self.resized_image = self._resize_image(self.image)
        self.resized_photoimage = ImageTk.PhotoImage(self.resized_image)
        self.image_display.config(image=self.resized_photoimage)

    def _watermarking(self):
        logo_size = 0
        image_w, image_h = self.image.size
        # whether vertical or horizontal image
        if self.image.size[0] > self.image.size[1]:
            logo_size = self.image.size[0] // 5
        else:
            logo_size = self.image.size[1] // 5
        # measurements for coordinates
        self.logo = self.logo.resize((logo_size, logo_size), Image.LANCZOS)
        logo_w, logo_h = self.logo.size
        top_left = (0, 0)
        top_right = (image_w - logo_w, 0)
        bottom_left = (0, image_h - logo_h)
        bottom_right = (image_w - logo_w, image_h - logo_h)

        self.transformed_image = self.image.copy()
        self.transformed_image.paste(self.logo, bottom_right, self.logo)
        self.resized_transformed = self._resize_image(self.transformed_image)
        self.transformed_photoimage2 = ImageTk.PhotoImage(self.resized_transformed)
        self.transformed_image_display.config(image=self.transformed_photoimage2)

    def _save_file(self):
        if self._image_name == "sample_image.jpg":
            messagebox.showinfo(title="Not allowed!", message="That is only a sample image!")
        else:
            directory = filedialog.askdirectory()
            new_path = directory + "/[watermark]_" + self._image_name.split(".")[0] + ".png"
            print(new_path)
            if messagebox.askokcancel(title="Confirmation", message=f"New file path:\n{new_path}"):
                self.transformed_image.save(new_path)
            else:
                messagebox.showinfo(title="Canceled", message="Operation cancelled")


if __name__ == "__main__":
    app = WaterMark()
    app.mainloop()
