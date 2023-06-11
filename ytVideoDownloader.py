from pytube import YouTube
from tkinter import *
import customtkinter

url = "https://www.youtube.com/watch?v=YLslsZuEaNE&ab_channel=KhaiLoOn"
# video_resolution_list = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p"]

class VideoDetailsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.default_label = customtkinter.CTkLabel(self, text="Search for a video...")
        self.default_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def display_video_details(self):
        self.default_label.destroy()

        #Video title
        self.video_title_label = customtkinter.CTkLabel(self, text="Title: "+self.youtube_object.title)
        self.video_title_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        #Channel name
        self.channel_name_label = customtkinter.CTkLabel(self, text="Channel: "+self.youtube_object.author)
        self.channel_name_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        #Audio only checkbox
        self.audio_only_var = customtkinter.BooleanVar(value=False)


        #Select video resolution
        self.resolution_select_var = customtkinter.StringVar(value=self.resolution_select_list[0])
        self.resolution_select_menu = customtkinter.CTkOptionMenu(self, values=self.resolution_select_list, variable=self.resolution_select_var)
        self.resolution_select_menu.place(relx=0.5, rely=0.6, anchor=CENTER)

        #Download button
        self.download_button = customtkinter.CTkButton(self, text="Download 📥", fg_color="red", command=self.download)
        self.download_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    #Check for available resolutions for searched video
    def available_resolutions(self):
        self.resolution_select_list = []

        for stream in self.youtube_object.streams.order_by("subtype"):
            size = " ("+str(stream.filesize_mb)+" MB)"
            if stream.type == "video":
                self.resolution_select_list.append(stream.resolution+"/"+stream.subtype+size)
            else:
                self.resolution_select_list.append("Audio/"+stream.subtype+size)
            # print(stream.resolution)

    #download video stream to savePath
    def download(self):
        print("Downloading...")
        path = app.savePath_entry_var.get()
        link = app.link_entry.get()
        print("Link: ", link)
        print("Path: ", path)
        [resolution, subtype] = self.resolution_select_var.get().split("/")
        subtype = subtype.split(" ")[0]
        # youtubeVideo = self.video_stream_list.get_by_resolution(self.resolution_select_var.get())
        #filtering audio and video using subtype
        if resolution == "Audio":
            youtubeVideo = self.youtube_object.streams.filter(type=resolution, subtype=subtype).first()
        else:
            youtubeVideo = self.youtube_object.streams.filter(res=resolution, subtype=subtype).first()

        print(youtubeVideo)
        try:
            # file_name = resolution + default_file_name + ".mp4"
            savedPath = youtubeVideo.download(path, None, youtubeVideo.resolution+" ")
            print("Download completed")
            print("Saved as: ", savedPath)
        except:
            print("Download error")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #App variables
        self.title("UJtube")
        self.geometry("900x600")
        
        #Switch for theme
        self.theme_switch_var = customtkinter.StringVar(value="dark")
        self.theme_switch = customtkinter.CTkSwitch(self,text="⚫/⚪", command=self.switch_theme, variable=self.theme_switch_var, onvalue="light", offvalue="dark")
        self.theme_switch.place(relx=0.9, rely=0.1)

        #Textbox for url
        self.link_entry = customtkinter.CTkEntry(self, placeholder_text="Enter YouTube video url...")
        self.link_entry.place(relx=0.5, rely=0.1, anchor=CENTER)

        #Search buton
        self.search_button = customtkinter.CTkButton(self, text="🔎", command=self.search)
        self.search_button.place(relx=0.8, rely=0.1, anchor=CENTER)

        #Download path textbox
        self.savePath_entry_var = customtkinter.StringVar(value="C:/Users/sambh/Downloads")
        self.savePath_entry = customtkinter.CTkEntry(self, textvariable=self.savePath_entry_var)
        self.savePath_entry.place(relx=0.5, rely=0.2, anchor=CENTER)

    #Switch theme function
    def switch_theme(self):
        customtkinter.set_appearance_mode(self.theme_switch_var.get())

    #Search and display video details
    def search(self):
        link = self.link_entry.get()
        print("Link: ", link)
        try:
            youtubeObject = YouTube(link)
        except:
            print("Connection error")
        print("Video title: ", youtubeObject.title)

        #Searched video details frame
        self.searched_video_frame = VideoDetailsFrame(master=self)
        self.searched_video_frame.place(relx=0.5, rely=0.5,anchor=CENTER)
        self.searched_video_frame.youtube_object = youtubeObject   
        self.searched_video_frame.available_resolutions()
        self.searched_video_frame.display_video_details()
        print(*self.searched_video_frame.youtube_object.streams, sep="\n")
        print(self.searched_video_frame.resolution_select_list)

app = App()
app.mainloop()




# print("\t\t\tTitle: ",youtubeObject.title)
# print("Author: ",youtubeObject.author)
# print(youtubeObject.description)
# print("Views: ",youtubeObject.views/1000,"k")
# print("Avg rating: ",youtubeObject.rating)
# print("Length: ",youtubeObject.length)
# print("Published: ",youtubeObject.publish_date)
# print("Keywords: ",youtubeObject.keywords)
# print("Metada: ",youtubeObject.metadata)

