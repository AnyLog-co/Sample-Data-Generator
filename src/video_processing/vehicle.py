import os
class VideoProcessing:
    def __init__(self, model_file:str, label_file:str, video:str, exception:bool=False):
        """
        Declare file params + echeck if they exist
        :params:
            self.status:bool
            self.exception:bool - whether to print exceptions
            self.model_file:str - model file
            self.label_file:str - label file
            self.video_file:str - video to analyze
            self.obj_count:int - number of people
            self.confidence:int - confidence
        """
        self.status = True
        self.exception = exception
        self.obj_count = 0
        self.confidence = 0
        self.model_file = os.path.expanduser(os.path.expandvars(model_file))
        self.label_file = os.path.expanduser(os.path.expandvars(label_file))
        self.video_file = os.path.expanduser(os.path.expandvars(video))

        if not os.path.isfile(self.model_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {model_file}")
        if os.path.isfile(self.label_file):
            self.__read_label_file()
        elif not os.path.isfile(self.label_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {label_file}")
        if os.path.isfile(self.video_file):
            self.__read_video()
        elif not os.path.isfile(self.video_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate video filfe {video}")
