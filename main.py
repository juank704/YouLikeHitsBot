import asyncio
from automation.chrome_factory import ChromeFactory
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os

async def main():

    # Obtener el nombre de usuario y la contraseña del entorno
    username = os.getenv('YOULIKEHITS_USERNAME', 'default_username')  # El segundo argumento es un valor predeterminado opcional
    password = os.getenv('YOULIKEHITS_PASSWORD', 'default_password')

    browser = ChromeFactory.create_instance(True)
    login = 'https://www.youlikehits.com/login.php'
    url = 'https://www.youlikehits.com/youtubenew2.php'
    

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
    await asyncio.sleep(10)

    browser.get(url)
    
    acc = 0
    follow_button_not_found = 0
    # Variable para llevar el seguimiento de las combinaciones de número y puntos
    combinations_tracker = {}

    while True:  # Repetir indefinidamente
        # Ejecuta la lógica síncrona en un hilo y espera su resultado
        try:
            browser.switch_to.window(main_window_handle)

            #close_extra_Windows
            close_extra_windows(browser, main_window_handle)

            browser.switch_to.window(main_window_handle)

            font_element = browser.find_element(By.XPATH, "//font[contains(., 'Timer')]")
            # Extrae el texto completo del elemento
            full_text = font_element.text

            try:
                # Intenta extraer el número después de '/'
                number_after_slash = full_text.split('/')[-1].strip()
                # Intenta convertir el texto a número para asegurarse de que es un número válido
                number = int(number_after_slash)
            except (ValueError, IndexError):
                # Si ocurre un error en la extracción o conversión, establece el número a 1 por defecto
                number = 1


            print("Número obtenido:", number)

              # Verifica si 'number' es igual a 1
            if number == 1:
                # Incrementa el acumulador
                acc += number
                # Si el acumulador llega a 30, realiza el "refresh" y reinicia el acumulador
                if acc >= 5:
                    print("Realizando refresh de la página...")
                    browser.get(url)
                    acc = 0  # Reinicia el acumulador después del "refresh"
            else:
                # Si 'number' no es 1, el acumulador se reinicia a 0
                acc = 0
                


        # Buscar el botón por la clase 'followbutton' y hacer clic en él
            follow_button = browser.find_element(By.CLASS_NAME, 'followbutton')
            follow_button.click()
        except NoSuchElementException:
            print("No se encontró el botón.")
            # Verifica si el contador ha alcanzado 10
            if follow_button_not_found >= 5:
                print("Realizando refresh de la página debido a 5 intentos fallidos...")
                browser.get(url)  # Refresca la página
                follow_button_not_found = 0  # Reinicia el contador

        except StaleElementReferenceException:
            print("El elemento ya no está adjunto al DOM.")


        try:
            # Intenta encontrar el elemento que contiene los puntos
            points_element = browser.find_element(By.ID, "currentpoints")
            points = points_element.text  # Obtiene el texto del elemento, que son los puntos
            print("Cantidad de puntos:", points)

            combination = f"{number}-{points}"
            if combination in combinations_tracker:
                combinations_tracker[combination] += 1
                if combinations_tracker[combination] >= 5:
                    print("Combinación repetida 5 veces. Realizando refresh...")
                    browser.get(url)
                    combinations_tracker = {}  # Reinicia el seguimiento
            else:
                combinations_tracker[combination] = 1

        except NoSuchElementException:
            # Maneja el caso en que el elemento no se encuentra
            print("El elemento que muestra los puntos no se encontró en la página.")
    
        # Espera un poco antes de volver a ejecutar para evitar saturación
        await asyncio.sleep(number)  # Espera 10 segundos antes de la próxima iteración


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