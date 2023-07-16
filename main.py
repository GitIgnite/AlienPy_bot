import sys

import pyautogui
import webbrowser
from selenium import webdriver
from pynput import keyboard
import time
import constants
from utils.imageutils import ImageUtils
from utils.pauseutils import Pauseutils


def main() :
    # get initial window sizex
    driver = webdriver.Firefox(executable_path='./drivers/geckodriver.exe')
    print(driver.get_window_size())
    #
    driver.set_window_size(1200, 700)
    # print(driver.get_window_size())
    #
    driver.get(constants.URL)
    time.sleep(5)
    run_bot()

def run_bot():

    while 1:
        try:
            image_detected = ''
            # Si on se trouve sur la page de login, on se connecte
            if ImageUtils.get_actual_page() == constants.LOGIN:
                print("Page Login")
                step(['login.png'])
                # TODO : Mettre en place la connexion avec google
            if ImageUtils.get_actual_page() == constants.ACCUEIL:
                print("Page Accueil")
                step(['mineAccueil.png'])
            if ImageUtils.get_actual_page() == constants.MINE:
                print("Page Mine")
                image_detected = ImageUtils.test_image(['mineSecondaire.png', 'claimMine.png'])
                step([image_detected])

            try:
                if image_detected == 'mineSecondaire.png':
                    step_with_exception(['claim.png'])

                step_with_exception(['captcha.png', 'captcha2.png'])
                step(['buster.png', 'buster2.png'])

                if ImageUtils.test_image(['spam.png']):
                    raise RuntimeError("Page Automated query")
                else:
                    nb_try_captcha = 0
                    while ImageUtils.boucle_test_image(['approve.png', 'approve2.png', 'valideCaptcha.png']) == '' and nb_try_captcha <= 20:
                        ImageUtils.click_image('retrybuster.png')
                        time.sleep(1)
                        step(['buster.png', 'buster2.png'])
                    if nb_try_captcha > 20:
                        raise RuntimeError("Un problème est survenu au niveau du captcha")
                    else:
                        # TODO : bouger la souris
                        step_with_exception(['approve.png', 'approve2.png'])

                step_with_exception(['miningHub.png'])
                time.sleep(390)
            except RuntimeError as err:
                print(err)
                Pauseutils.epause()
                # TODO : faire F5 pour actualiser la page et retourner au login
                continue
        except Exception as err:
            print("Erreur du programme")
            sys.exit()


def step(images):
    ImageUtils.click_btn(images)
    Pauseutils.gpause()


def step_with_exception(images):
    etat_step_ok = ImageUtils.click_btn(images)
    if not etat_step_ok:
        raise RuntimeError("Erreur au niveau de l'image : " + images[0])
    Pauseutils.gpause()


main()
