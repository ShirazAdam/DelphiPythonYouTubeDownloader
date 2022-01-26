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
import os

class MainForm(Form):
    def __init__(self, owner) -> None:
        self.StreamID : str = "Stream ID:"
        self.ITag : int = 0
        self.YT : YouTube()

        self.Caption = "Delphi Python YouTube Downloader"
        self.SetBounds(10, 10, 600, 400)
        self.Position = "poScreenCenter"

        self.lblInstructions = Label(self)
        self.lblInstructions.SetProps(Parent = self, Caption = "Enter the URL below to download the video")
        self.lblInstructions.SetBounds(10, 10, 300, 24)

        self.txtEditUrl = Edit(self)
        self.txtEditUrl.SetProps(Parent = self)
        self.txtEditUrl.SetBounds(10, 30, 420, 20)
        self.txtEditUrl.Text = ""

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
        self.cmbBxVideos.OnChange = self.__on_cmbBxVideos_Change

        self.btnDownload = Button(self)
        self.btnDownload.SetProps(Parent = self, Caption = "Download")
        self.btnDownload.SetBounds(10, 130, 560, 25)
        self.btnDownload.OnClick = self.__on_btnDownload_Click

        self.logOutput = Memo(self)
        self.logOutput.SetProps(Parent = self)
        self.logOutput.SetBounds(10, 170, 560, 180)
        self.logOutput.Lines.Add("Please note that this software has been design for use on Windows only")

        self.OnClose = self.__on_form_close

    def __on_btnAnalyse_Click(self, sender) -> None:
        self.logOutput.Lines.Add("Now analysing link...")
        self.YT = YouTube(self.txtEditUrl.Text)
        self.YT.register_on_progress_callback(self.__on_download_Progress)
        streams = self.YT.streams.filter(file_extension = "mp4").order_by("resolution").desc()
        self.btnDownload.Caption = "Download '{a}'".format(a = self.YT.title)

        for stream in streams:
            self.cmbBxVideos.Items.Add("Resolution: {a}, FPS: {b}, {d} {c}".format(a = stream.resolution, b = stream.fps, c = stream.itag, d = self.StreamID))

        self.logOutput.Lines.Add("Video to download is '{a}'".format(a = self.YT.title))
        self.logOutput.Lines.Add("Analysis complete")

    def __on_cmbBxVideos_Change(self, sender) -> None:
        searchString = self.StreamID
        itagList = self.cmbBxVideos.Text.split(searchString)
        itag = itagList[1].replace(searchString, "").strip()
        self.logOutput.Lines.Add("Stream selected: {}".format(itag))
        self.ITag = itag

    def __on_btnDownload_Click(self, sender) -> None:
        isValid : bool = os.path.isfile(self.txtEditSave.Text)
        isStreamSelected : bool = self.cmbBxVideos.Text.strip()

        if isValid and isStreamSelected:
            self.__download_video()
        elif not isValid:
            self.logOutput.Lines.Add("Please save file to a valid location")
        elif not isStreamSelected:
            self.logOutput.Lines.Add("Please select a stream to download")
        else:
            self.logOutput.Lines.Add("Hmm...")

    def __download_video(self) -> None:
        self.logOutput.Lines.Add("Starting download for '{a} ({b})'...".format(a = self.YT.title, b = self.ITag))

        try:
            video = self.YT.streams.get_by_itag(self.ITag)
            video.download(filename = self.txtEditSave.Text)
            self.logOutput.Lines.Add("Download complete for '{a}'".format(a = self.YT.title))
        except RuntimeError as error:
            self.logOutput.Lines.Add("Error downloading: " + error)

    def __on_btnSave_Click(self, sender) -> None:
        filename = filedialog.asksaveasfilename(initialdir = "%USERPROFILE%", initialfile = self.YT.title, title = "Save file '{a}'".format(a = self.YT.title), filetypes = (("MPEG-4 Video files","*.m4v"),("MPEG-4 Video files","*.mp4"),("all files","*.*")), defaultextension = ".m4v")

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
    Application.Title = "Hello Python from DelphiVCL"
    Main = MainForm(Application)
    Main.Show()
    FreeConsole()
    Application.Run()
    Main.Destroy()

main()
