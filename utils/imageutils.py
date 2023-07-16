import constants
import pyautogui
from utils.pauseutils import Pauseutils
import array


class ImageUtils:

    @staticmethod
    def test_image(images):
        image_found = ''
        for image in images:
            if pyautogui.locateCenterOnScreen(constants.FOLDER_IMG + image) != None:
                image_found = image
                break
        return image_found

    @staticmethod
    def boucle_test_image(images):
        nb_try = 0
        found = False
        image = ''
        while nb_try <= constants.NB_TRY_MAX and not found:
            image = ImageUtils.test_image(images)
            if image != '':
                found = True
            else:
                Pauseutils.mpause()
                nb_try += 1
        return image

    @staticmethod
    def get_actual_page():
        if ImageUtils.test_image([constants.IMG_INVENTORY]):
            page_actuel = constants.ACCUEIL
        elif ImageUtils.test_image([constants.IMG_BTN_ACCUEIL]):
            page_actuel = constants.MINE
        else:
            page_actuel = constants.LOGIN

        return page_actuel

    @staticmethod
    def click_image(image):
        pyautogui.leftClick(pyautogui.locateCenterOnScreen(constants.FOLDER_IMG + image))

    @staticmethod
    # Return True si OK | False si KO
    def click_btn(images):
        image_to_click = ImageUtils.boucle_test_image(images)
        if image_to_click != '':
            ImageUtils.click_image(image_to_click)
            return True
        return False
