import pygame
import pygame.camera
import time
import timeit
import schedule
import threading
import cv2
import os
from datetime import timedelta, date
from datetime import datetime
from calendar import monthrange
def takePicture(cam_to_use):
    start = time.time()
    pygame.camera.init()
    if not hasattr(takePicture, "counter"):
        takePicture.counter = 0
    camlist = pygame.camera.list_cameras()
    if camlist:
        cam = pygame.camera.Camera(camlist[cam_to_use],(640,480))
        cam.start()
        time.sleep(1)
        img = cam.get_image()
        cam.stop()
        photo_name = "pictures\photo_" + str(takePicture.counter) + ".png"
        takePicture.counter += 1
        pygame.image.save(img ,photo_name)
        imq = img
        end = time.time()
    return (end - start)
    #Press the green button in the gutter to run the script.


# Define some colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)
green = ( 0, 255, 0)
red = ( 255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Timelapse")
carryOn = True

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font(None, 20)
img = font.render('click below to get started', True, white)
screen.blit(img, (20, 20))

font = pygame.font.Font(None, 20)
fonts = pygame.font.get_fonts()
font1 = pygame.font.Font(None, 72)
img1 = font1.render('Timelapse', True, red)



font2 = pygame.font.Font(None, 20)
img3 = font2.render('type how long do you want between photos:', True, white)
img4 = font2.render('type how long do you want to take photos for:', True, white)
img5 = font2.render('amount of photos:', True, white)
img6 = font2.render('cameras: (enter num of camera that you want to use below starting at 0)', True, white)
w, h = pygame.display.get_surface().get_size()
hours_photo = 'hh'
minutes_photo = 'mm'
seconds_photo = 'ss'
base_font = pygame.font.Font(None, 20)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
text_color_active = pygame.Color(50, 50, 50)
text_color_passive = pygame.Color(127, 200, 127)
text_color = text_color_passive

def button(screen, position, rectColor, txtColor, text,):
    font = pygame.font.Font(None, 60)
    text_render = font.render(text, 1, txtColor)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, rectColor, (x, y, w , h))
    return screen.blit(text_render, (x, y))
def InputText(user_text, active, orignal_text, max_len, position):
    x, y, w, h = position
    text_rect = pygame.Rect(x, y, w, h)
    if user_text == '':
        if not active:
            user_text = orignal_text
    if active:
        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_BACKSPACE:


                user_text = user_text[:-1]
                event.unicode = ''


            if len(user_text) < max_len :

                user_text += event.unicode

                if not user_text.isnumeric():
                    user_text = user_text[:-1]
                    event.unicode = ''



    if user_text == orignal_text:
        text_color = text_color_passive
    else:
        text_color = text_color_active
    if active:
        color = color_active
    else:
        color = color_passive

    pygame.draw.rect(screen, color, text_rect)

    text_surface = base_font.render(user_text, True, text_color)

    screen.blit(text_surface, (text_rect.x + 5, text_rect.y + 5))


    text_rect.w = max(100, text_surface.get_width() + 10)
    return user_text, active





def check_if_active(active, num_activated):
    for i in range(0, len(active)):
        active[i] = False
        if i == num_activated:
            active[i] = True
    return active

def find_total_photo(hours_amount, minutes_amount, seconds_amount, days_total_amount, hours_total_amount, minutes_total_amount):
    if not hours_amount.isnumeric():
        hours_amount = "0"
    if not minutes_amount.isnumeric():
        minutes_amount = "0"
    if not seconds_amount.isnumeric():
        seconds_amount = "0"
    seconds_amount = int(seconds_amount) + (int(minutes_amount) + (int(hours_amount)*60)) * 60
    if not days_total_amount.isnumeric():
        days_total_amount = "0"
    if not hours_total_amount.isnumeric():
        hours_total_amount = "0"
    if not minutes_total_amount.isnumeric():
        minutes_total_amount = "0"
    seconds_total_amount = (int(minutes_total_amount) + (int(hours_total_amount) + (int(days_total_amount) * 24)) * 60)*60
    if seconds_amount == 0:
        seconds_amount += 1
    return round(seconds_total_amount/seconds_amount)

def find_between(hours_amount, minutes_amount, seconds_amount, Days):
    if not hours_amount.isnumeric():
        hours_amount = "0"
    if not minutes_amount.isnumeric():
        minutes_amount = "0"
    if not seconds_amount.isnumeric() or seconds_amount == "0":
        seconds_amount = "1"
    if Days:
        return (int(seconds_amount) + (int(minutes_amount) + (int(hours_amount) * 24)) * 60)
    return (int(seconds_amount) + (int(minutes_amount) + (int(hours_amount) * 60)) * 60)

class Capture(object):
    def __init__(self, Cam_want):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)


        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[Cam_want], self.size)
        self.cam.start()


        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

            # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (w/2, h/2))
        pygame.display.flip()



def run_continuously(interval=1):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

change = False
next_button = False
photo_page = False

clicked_on_text = False
active_change = [False, False, False, False, False, False, False]

hours_photo = "hh"
minutes_photo = "mm"
seconds_photo = "ss"
hour_position = (w/6.3, h/3.2, 30, 19)
minute_position = (w/4.2, h/3.2, 30, 19)
second_position = (w/3.2, h/3.2, 30, 19)
hour_rect = pygame.Rect(hour_position)
minute_rect = pygame.Rect(minute_position)
second_rect = pygame.Rect(second_position)

days_total = "dd"
hours_total = "hh"
minutes_total = "mm"
day_position_total = (w/1.67, h/3.2, 30, 19)
hour_position_total = (w/1.48, h/3.2, 30, 19)
minute_position_total = (w/1.33, h/3.2, 30, 19)
day_rect_total = pygame.Rect(day_position_total)
hour_rect_total = pygame.Rect(hour_position_total)
minute_rect_total = pygame.Rect(minute_position_total)
n1 = screen.blit(img3, (w/17.1, h/3.7))
b1 = screen.blit(img3, (w/17.1, h/3.7))
start_photos = screen.blit(img3, (w/17.1, h/3.7))
final_button = screen.blit(img3, (w/17.1, h/3.7))
amount_photos = "0"

cam_want = "0"
cam_chosen = 0
cam_position = (w/2.7, h/1.6, 15, 19)
cam_rect = pygame.Rect(cam_position)

pygame.camera.init()
start = timeit.default_timer()
time_taken = 0

seconds_between = 0
minutes_time_total = 0
not_called = False
set_up = False
warning = False
next = False
alive = True
done = False

video_made = True
image_folder = 'pictures'
video_name = 'timelapse/timelapse.avi'

while carryOn:


    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False


        screen.fill((0, 150, 150))
        if not change and not next:
            b1 = button(screen, (w/2.5, h/1.25), red, white,"Start")
            screen.blit(img, (w/3.1, h/2.8))
            screen.blit(img1, (w/3.2, h/3.6))
        if change:


            screen.blit(img3, (w/17.1, h/3.7))
            screen.blit(img4, (w/2, h/3.7))
            screen.blit(img5, (w/3.5, h/2.5))
            screen.blit(img6, (w/12.1, h/1.85))
            hours_photo, active_change[0]  = InputText(hours_photo, active_change[0], "hh", 2, hour_position)
            minutes_photo, active_change[1]  = InputText(minutes_photo, active_change[1], "mm", 2, minute_position)
            seconds_photo, active_change[2]  = InputText(seconds_photo, active_change[2], "ss", 2, second_position)

            days_total, active_change[3] = InputText(days_total, active_change[3], "dd", 2, day_position_total)
            hours_total, active_change[4] = InputText(hours_total, active_change[4], "hh", 2, hour_position_total)
            minutes_total, active_change[5] = InputText(minutes_total, active_change[5], "mm", 2, minute_position_total)

            cam_want, active_change[6] = InputText(cam_want, active_change[6], '', 1, cam_position)

            amount_photos = find_total_photo(hours_photo, minutes_photo, seconds_photo, days_total, hours_total, minutes_total)
            cameras = pygame.camera.list_cameras()
            text_surface = base_font.render(str(amount_photos), True, (255,255,255))
            camera_list = base_font.render(str(cameras), True, (255, 255, 255))
            if not cam_want.isnumeric():
                cam_chosen = 0
            else:
                cam_chosen = int(cam_want)
            if amount_photos > 0 and cam_chosen < len(cameras):
                next_button = True
            else:
                next_button = False

            screen.blit(text_surface, (w/2.2, h/2.47))
            screen.blit(camera_list, (w / 6, h / 1.7))
            pygame.display.update()

        if next_button:
            n1 = button(screen, (w/2.5, h/1.25), green, black, "Start taking photos")
        if photo_page:
            if not set_up:
                set_up = True
                c = Capture(int(cam_want))
            start_photos = button(screen, (w / 9, h / 6), green, white, "Start Taking photos")
            c.get_and_flip()
        if warning:
            if not days_total.isnumeric():
                days_total = "0"
            if not hours_total.isnumeric():
                hours_total = "0"
            if not minutes_total.isnumeric():
                minutes_total = "0"
            words = base_font.render("After clicking ok bellow it will start taking photos", True, (255, 255, 255))
            words1 = base_font.render("this window will say not responding but it will still take photos", True, (255, 255, 255))
            words2 = base_font.render("it will finish at:", True, (255, 255, 255))
            done_date = datetime.now() + timedelta(days=int(days_total))
            done_date = done_date + timedelta(hours=int(hours_total))
            done_date = done_date + timedelta(minutes= int(int(minutes_total) + (1.6/60 * amount_photos)))
            done_date = done_date + timedelta(seconds =  (int(int(minutes_total) + (1.6/60 * amount_photos)) - int(minutes_total) + (1.6/60 * amount_photos))*60)
            done_date_str = done_date.strftime("%m/%d/%Y, %I:%M:%S %p")
            date_words = base_font.render(done_date_str, True, (255, 255, 255))
            screen.blit(words, (w / 9, h / 3))
            screen.blit(words1, (w / 9, h / 2.7))
            screen.blit(words2, (w / 9, h / 2.3))
            screen.blit(date_words, (w / 9, h / 2.1))
            final_button = button(screen, (w/2.5, h/1.25), green, white, "ok")
            if alive:
                alive = False
                del c
        if not_called:
            time_took = takePicture(int(cam_want))
            not_called = False
            done = True
            stop_run_continuously = run_continuously()
            schedule.every((seconds_between)).until(timedelta(minutes =  (minutes_time_total + (round(time_took, 1)/60 * amount_photos)))).seconds.do(takePicture, cam_to_use=int(cam_want))
            time.sleep(minutes_time_total * 60 + (round(time_took, 1) * amount_photos))
            stop_run_continuously.set()
        if done:
            if video_made:
                video_made = False
                images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
                frame = cv2.imread(os.path.join(image_folder, images[0]))
                height, width, layers = frame.shape

                video = cv2.VideoWriter(video_name, 0, 4, (width, height))

                for image in images:
                    video.write(cv2.imread(os.path.join(image_folder, image)))
                cv2.destroyAllWindows()
                video.release()
            location = base_font.render("the pictures will be at Timelapse \ pictures", True, (255, 255, 255))
            location_timelapse = base_font.render("the video will be at Timelapse \ timelapse", True, (255, 255, 255))
            message = base_font.render("make sure to move or delete the photos and video from the folders before doing it agian", True, (255, 255, 255))
            screen.blit(location, (w / 9, h / 3))
            screen.blit(location_timelapse, (w / 9, h / 2.7))
            screen.blit(message, (w / 9, h / 2.3))
    if event.type == pygame.MOUSEBUTTONDOWN:

        clicked_on_text = False
        if hour_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 0)
            if  hours_photo == "hh":
                hours_photo = ''
        if minute_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 1)
            if  minutes_photo == "mm":
                minutes_photo = ''
        if second_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 2)
            if  seconds_photo == "ss":
                seconds_photo = ''
        if day_rect_total.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 3)
            if days_total == "dd":
                days_total = ''
        if hour_rect_total.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 4)
            if hours_total == "hh":
                hours_total = ''
        if minute_rect_total.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 5)
            if minutes_total == "mm":
                minutes_total = ''
        if cam_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_on_text = True
            active_change = check_if_active(active_change, 6)
        if not clicked_on_text:
            active_change = check_if_active(active_change, -1)
        if b1.collidepoint(pygame.mouse.get_pos()) and not change and not next:
            change = True
        if start_photos.collidepoint(pygame.mouse.get_pos()) and photo_page:
            photo_page = False
            warning = True
        if final_button.collidepoint(pygame.mouse.get_pos()) and warning:
            warning = False
            not_called = True
        if n1.collidepoint(pygame.mouse.get_pos()) and next_button:
            seconds_between = find_between(hours_photo, minutes_photo, seconds_photo, False)
            minutes_time_total = find_between(days_total, hours_total, minutes_total, True)

            next_button = False
            next = True
            photo_page = True
            change = False


    pygame.display.flip()

    clock.tick(60)


pygame.quit()

