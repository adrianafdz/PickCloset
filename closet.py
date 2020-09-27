import os # para acceder a los archivos
import random

import tkinter as tk #build GUI
from PIL import Image, ImageTk #use images
from playsound import playsound 

WIND_TITLE="My Closet"
WIND_HEIGHT=650
WIND_WIDTH=400
IMG_WIDTH=250
IMG_HEIGHT=250

# imagenes BLUSAS
# todos los archivos en el folder, excepto los hidden
# "tops/nombre.ext"
ALL_BLOUSES=[str('tops/')+ file for file in os.listdir('tops/') if not file.startswith('.')]
ALL_BOTTOMS=[str('bottoms/')+ file for file in os.listdir('bottoms/') if not file.startswith('.')]

class Wardrobe:
	def __init__(self, root): #constructor
		self.root = root

		# get images
		self.top_images = ALL_BLOUSES
		self.bottom_images = ALL_BOTTOMS

		# first image to display
		self.top_image_path = self.top_images[0]
		self.bot_image_path = self.bottom_images[0]

		# crear 3 frames
		self.tops_frame = tk.Frame(self.root, bg="black", padx=50, pady=10)
		self.mid_frame = tk.Frame(self.root, bg="pink", pady=10, height=30)
		self.mid_frame.grid_propagate(0)
		self.bots_frame = tk.Frame(self.root, bg="black", padx=50, pady=10)

		# top image
		self.top_image_label=self.create_img(self.top_image_path, self.tops_frame)
		self.top_image_label.pack(side=tk.TOP)

		# bottom image
		self.bot_image_label=self.create_img(self.bot_image_path, self.bots_frame)
		self.bot_image_label.pack(side=tk.TOP)

		self.create_background();

	def create_background(self): 
		# change title
		self.root.title(WIND_TITLE)
		# change size and color
		self.root.geometry('{1}x{0}'.format(WIND_HEIGHT,WIND_WIDTH))

		self.create_buttons()

		# add frames
		self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
		self.mid_frame.pack(fill=tk.BOTH, expand=False)
		self.bots_frame.pack(fill=tk.BOTH, expand=tk.YES)

	def create_buttons(self):
		top_prev_button = tk.Button(self.tops_frame, text="Prev", command=self.get_prev_top)
		top_prev_button.pack(side=tk.LEFT, pady=5)

		top_next_button = tk.Button(self.tops_frame, text="Next", command=self.get_next_top)
		top_next_button.pack(side=tk.RIGHT, pady=5)

		outfit_button = tk.Button(self.mid_frame, text="Create outfit", command=self.create_outfit)
		outfit_button.pack(side=tk.TOP)

		bot_prev_button = tk.Button(self.bots_frame, text="Prev", command=self.get_prev_bottom)
		bot_prev_button.pack(side=tk.LEFT, pady=5)

		bot_next_button = tk.Button(self.bots_frame, text="Next", command=self.get_next_bottom)
		bot_next_button.pack(side=tk.RIGHT, pady=5)


	def create_img(self, image_path, frame):
		# open and resize image
		image_file = Image.open(image_path)
		image_resized = image_file.resize((IMG_HEIGHT,IMG_WIDTH), Image.ANTIALIAS)
		# turn into compatible image
		tk_photo = ImageTk.PhotoImage(image_resized)
		# create label (widget used to display text or image)
		image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
		# keep a reference
		image_label.image = tk_photo

		return image_label


	def update_image(self, new_image_path, image_label):
		# open and resize image
		image_file = Image.open(new_image_path)
		image_resized = image_file.resize((IMG_HEIGHT,IMG_WIDTH), Image.ANTIALIAS)
		# turn into compatible image
		tk_photo = ImageTk.PhotoImage(image_resized)

		# update label image 
		image_label.configure(image=tk_photo)
		# keep reference
		image_label.image = tk_photo


	# category : arreglo de tops o bottoms
	def _get_next_item(self, curr_item, category, increment=True):
		curr_index=category.index(curr_item)
		final_index = len(category) - 1
		next_index = 0

		if increment and curr_index==final_index:
			# return to first item
			next_index=0
		elif not increment and curr_index==0:
			# go to last item
			next_index=final_index
		else:
			incrementor = 1 if increment else -1
			next_index=curr_index+incrementor

		#new path
		next_image=category[next_index]

		# update the label
		if curr_item in self.top_images:
			image_label = self.top_image_label
			self.top_image_path = next_image
		elif curr_item in self.bottom_images:
			image_label = self.bot_image_label
			self.bot_image_path = next_image

		self.update_image(next_image, image_label)


	def get_next_top(self):
		self._get_next_item(self.top_image_path, self.top_images, increment=True)
	
	def get_prev_top(self):
		self._get_next_item(self.top_image_path, self.top_images, increment=False)

	def get_prev_bottom(self):
		self._get_next_item(self.bot_image_path, self.bottom_images, increment=False)

	def get_next_bottom(self):
		self._get_next_item(self.bot_image_path, self.bottom_images, increment=True)

	def create_outfit(self):
		new_top = random.randint(0, len(self.top_images)-1)
		new_bot = random.randint(0, len(self.bottom_images)-1)

		# get paths
		next_image_top = self.top_images[new_top]
		next_image_bot = self.bottom_images[new_bot]
		# update paths
		self.top_image_path = next_image_top
		self.bot_image_path = next_image_bot
		# get labels
		t_image_label = self.top_image_label
		b_image_label = self.bot_image_label
		# update labels
		self.update_image(next_image_top, t_image_label)
		self.update_image(next_image_bot, b_image_label)


root=tk.Tk() # window
app=Wardrobe(root)
root.mainloop()