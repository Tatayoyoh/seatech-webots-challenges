from controller import Camera

CAMERA_SAMPLING_PERIOD = 50
CAMERA_RECOGNITION_SAMPLING_PERIOD = 100

class EpuckCamera(Camera):
    def __init__(self):
        super().__init__('camera')
        self.enable(CAMERA_SAMPLING_PERIOD)
        self.recognitionEnable(CAMERA_RECOGNITION_SAMPLING_PERIOD)
        self.__tracked_name = None
        self.__recognized_object = None

    @property
    def recognized_object(self):
        return self.__recognized_object

    def track_object(self, object_name):
        self.__tracked_name = object_name

    def is_tracked_object_on_left(self):
        obj = self.__recognized_object
        if not obj:
            return None

        obj_centos_pos = obj.get_position_on_image()[0] + int(obj.get_size_on_image()[0]/2)
        if obj_centos_pos < int(self.getWidth()/2):
            return True
        else:
            return False

    def is_tracked_object_on_right(self):
        return self.is_tracked_object_on_left() == False

    def is_tracked_object_present(self):
        objs = self.getRecognitionObjects()
        for obj in objs:
            if self.__tracked_name == obj.get_model().decode("utf-8"):
                self.__recognized_object = obj
                return True
        return False
        