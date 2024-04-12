import asyncio
from selenium import webdriver
from automation.chrome_factory import ChromeFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
 
import os

def create_instance(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-setuid-sandbox")  # Additional flag for Docker environment

    service = ChromeService(ChromeDriverManager().install())
    service.log_path = "chromedriver.log"
    service.verbose = True

    return webdriver.Chrome(service=service, options=chrome_options)

async def main():

    # Obtener el nombre de usuario y la contraseña del entorno
    username = os.getenv('YOULIKEHITS_USERNAME', 'default_username')  # El segundo argumento es un valor predeterminado opcional
    password = os.getenv('YOULIKEHITS_PASSWORD', 'default_password')

    browser = create_instance(True)
 
    login = 'https://www.youlikehits.com/login.php'
    url = 'https://www.youlikehits.com/websites.php'
    

    # Navegar a una página web
    browser.get(login)
    main_window_handle = browser.current_window_handle


    # Ingresa el nombre de usuario
    username_field = browser.find_element(By.ID, "username")
    username_field.send_keys(username)

    # Ingresa la contraseña
    password_field = browser.find_element(By.ID, "password")
    password_field.send_keys(password)  # Reemplaza "password" con tu contraseña real

    # Localizar y hacer clic en el botón de inicio de sesión
    login_button = browser.find_element(By.XPATH, "//input[@type='submit'][@value='Log in']")
    login_button.click()

    # Esperar 10 segundos
    await asyncio.sleep(5)

    browser.get(url)
    
 
    follow_button_not_found = 0
    # Variable para llevar el seguimiento de las combinaciones de número y puntos


    while True:  # Repetir indefinidamente
        # Ejecuta la lógica síncrona en un hilo y espera su resultado
        try:
            browser.switch_to.window(main_window_handle)

            #close_extra_Windows
            close_extra_windows(browser, main_window_handle)

            browser.switch_to.window(main_window_handle)

            max_retries = 5
            wait_time = 1  # Comienza con 1 segundo

            for attempt in range(max_retries):
                try:
                    follow_buttons = browser.find_elements(By.CLASS_NAME, 'followbutton')
                   
                    for button in follow_buttons:
                        button.click()

                        window_handles = browser.window_handles
                        browser.switch_to.window(window_handles[-1])

                        isValid = False

                        await asyncio.sleep(5)

                        try:
                            # Use XPath to search for the text anywhere in the document
                            element = browser.find_element(By.XPATH, "//*[contains(text(), concat('We couldn', \"'\", 't locate the website you', \"'\", 're attempting to visit.'))]")
                            print("Text found on the page.")
                        except NoSuchElementException:
                            print("Text not found on the page.")
                            isValid = True

                    
                        if isValid:

                            await asyncio.sleep(22)

                        close_extra_windows(browser, main_window_handle)
                        browser.switch_to.window(main_window_handle)
                        
                        # It's often a good idea to put a short delay between actions to avoid being flagged as a bot:
                        await asyncio.sleep(1)
                    
                        break  # Salir del ciclo de reintentos si tiene éxito
                except TimeoutException:
                    print(f"Timeout, reintento {attempt + 1} de {max_retries}")
                    await asyncio.sleep(wait_time)
                    wait_time *= 2  # Aumenta el tiempo de espera para el próximo reintento
                except Exception as e:
                    print(f"Error inesperado: {e}")
                    break  # Salir del ciclo en caso de error inesperado

            # Buscar el botón por la clase 'followbutton' y hacer clic en él

            browser.get(url)  
            await asyncio.sleep(1)

        except NoSuchElementException:
            print("No se encontró el botón.")
            # Verifica si el contador ha alcanzado 10
            if follow_button_not_found >= 5:
                print("Realizando refresh de la página debido a 5 intentos fallidos...")
                browser.get(url)  # Refresca la página
                follow_button_not_found = 0  # Reinicia el contador


        try:
            # Intenta encontrar el elemento que contiene los puntos
            points_element = browser.find_element(By.ID, "currentpoints")
            points = points_element.text  # Obtiene el texto del elemento, que son los puntos
            print("Cantidad de puntos:", points)

        except NoSuchElementException:
            # Maneja el caso en que el elemento no se encuentra
            print("El elemento que muestra los puntos no se encontró en la página.")
    
        # Espera un poco antes de volver a ejecutar para evitar saturación
        await asyncio.sleep(5)  # Espera 10 segundos antes de la próxima iteración


def close_extra_windows(browser, main_window_handle):
    # Itera sobre todas las ventanas abiertas
    for handle in browser.window_handles:
        # Cambia primero a la ventana que quieres evaluar
        browser.switch_to.window(handle)
        # Comprueba el título de la ventana actual
        window_title = browser.title
        if not window_title.startswith("Earn Points"):
        # Si el título de la ventana no comienza con "Earn Points", y no es la ventana principal, cierra esa ventana
            if handle != main_window_handle:
                browser.close()


if __name__ == "__main__":
    asyncio.run(main())