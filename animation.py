class Animation():
    def __init__(self, images, delay=1, is_loop=False):
        self.images = images
        self.img_index = 0
        self.delay = self.timer = delay
        self.is_loop = is_loop
        self.expired = False

    def update(self, dt):
        if not self.expired:
            if self.timer <= 0:
                self.inc_image()
                self.timer = self.delay
            self.timer -= dt

    def inc_image(self):
        if not self.expired:
            self.img_index += 1
            if self.img_index >= len(self.images):
                if self.is_loop:
                    self.img_index = 0
                else:
                    self.expired = True

    def get_image(self):
        if self.expired:
            return self.images[-1]
        else:
            return self.images[self.img_index]


