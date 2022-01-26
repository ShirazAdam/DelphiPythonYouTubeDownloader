#-------------------------------------------------------------------------------
# Name:        Main
# Purpose:
#
# Author:      Shiraz
#
# Created:     21/01/2022
# Copyright:   (c) Shiraz 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from delphivcl import *
from pytube import YouTube
from pytube import Stream
from tkinter import filedialog
from tkinter import messagebox

class MainForm(Form):

    def __init__(self, owner) -> None:
        self.Caption = "Delphi Python YouTube Downloader"
        self.SetBounds(10, 10, 600, 400)
        self.Position = "poScreenCenter"

        self.lblInstructions = Label(self)
        self.lblInstructions.SetProps(Parent = self, Caption = "Enter the URL below to download the video")
        self.lblInstructions.SetBounds(10, 10, 300, 24)

        self.txtEdit = Edit(self)
        self.txtEdit.SetProps(Parent = self)
        self.txtEdit.SetBounds(10, 30, 420, 20)
        self.txtEdit.Text = "https://www.youtube.com/watch?v=di3fLHgey8U"

        self.btnAnalyse = Button(self)
        self.btnAnalyse.SetProps(Parent = self, Caption = "Analyse")
        self.btnAnalyse.SetBounds(450, 30, 120, 25)
        self.btnAnalyse.OnClick = self.__on_btnAnalyse_Click

        self.txtEditSave = Edit(self)
        self.txtEditSave.SetProps(Parent = self)
        self.txtEditSave.SetBounds(10, 60, 420, 20)

        self.btnSave = Button(self)
        self.btnSave.SetProps(Parent = self, Caption = "Save to...")
        self.btnSave.SetBounds(450, 60, 120, 25)
        self.btnSave.OnClick = self.__on_btnSave_Click

        self.cmbBxVideos = ComboBox(self)
        self.cmbBxVideos.SetProps(Parent = self)
        self.cmbBxVideos.SetBounds(10, 95, 560, 25)

        self.btnDownload = Button(self)
        self.btnDownload.SetProps(Parent = self, Caption = "Download")
        self.btnDownload.SetBounds(10, 130, 560, 25)
        self.btnDownload.OnClick = self.__on_btnDownload_Click

        self.logOutput = Memo(self)
        self.logOutput.SetProps(Parent = self)
        self.logOutput.SetBounds(10, 170, 560, 180)

        self.OnClose = self.__on_form_close

    def __on_btnAnalyse_Click(self, sender) -> None:
            self.logOutput.Lines.Add("Now analysing link...")
            yt = YouTube(self.txtEdit.Text)
            yt.register_on_progress_callback(self.__on_download_Progress)
            streams = yt.streams.filter(file_extension = "mp4").order_by("resolution").desc()
            self.btnDownload.Caption = "Download '{a}'".format(a = yt.title)

            for stream in streams:
                ##self.cmbBxVideos.Items.Add(stream)##.itag, "Resolution: {a}, FPS: {b}, Title: {c}".format(a = stream, b = stream, c = yt.title))
                self.cmbBxVideos.Items.Add("Resolution: {a}, FPS: {b}".format(a = stream.resolution, b = stream.fps))
                ##self.cmbBxVideos.Items.Add(stream.itag, "Resolution: {a}, FPS: {b}, Title: {c}".format(a = stream.resolution, b = stream.fps, c = yt.title))

            self.logOutput.Lines.Add("Video to download is '{a}'".format(a = yt.title))
            self.logOutput.Lines.Add("Analysis complete")

    def __on_btnDownload_Click(self, sender) -> None:
        try:
            self.__download_video()
        except RuntimeError as error:
            self.logOutput.Lines.Add("Error with threading:" + error)


    def __download_video(self) -> None:
        self.logOutput.Lines.Add("Starting download...")

        try:
            ##stream = yt.streams.get_by_itag(22)
            ##stream.download()
            yt = YouTube(self.txtEdit.Text)
            yt.register_on_progress_callback(self.__on_download_Progress)
            video = yt.streams.filter(progressive = True, file_extension = "mp4").last()
            video.download(filename = self.txtEditSave.Text)
            self.logOutput.Lines.Add("Download complete for " + yt.title)
        except RuntimeError as error:
            self.logOutput.Lines.Add("Error with link: " + error)

    def __on_btnSave_Click(self, sender) -> None:
        filename = filedialog.asksaveasfilename(initialdir = "%USERPROFILE%", initialfile = self.ytTitle, title = "Save file...", filetypes = (("MPEG-4 Video files","*.m4v"),("MPEG-4 Video files","*.mp4"),("all files","*.*")), defaultextension = ".m4v")

        if not (filename.endswith(".m4v") or filename.endswith(".mp4")):
            filename += ".m4v"

        self.txtEditSave.Text = filename
        self.logOutput.Lines.Add(filename)

    def __on_download_Progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
        filesize = stream.filesize
        bytes_received = filesize - bytes_remaining
        self.__display_progress_bar(bytes_received, filesize)

    def __display_progress_bar(self, bytes_received : int, filesize : int) -> None:
        percent = round(100.0 * bytes_received / float(filesize), 1)
        self.logOutput.Lines.Add(str(percent) + "%")

    def __on_form_close(self, sender, action) -> None:
        action.Value = caFree

def main():
    Application.Initialize()
    Application.Title = "Hello Python from Delphi"
    Main = MainForm(Application)
    Main.Show()
    FreeConsole()
    Application.Run()
    Main.Destroy()

main()
