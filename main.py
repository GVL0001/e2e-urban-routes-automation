import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, "//button[@class='button round']")
    comfort_button = (By.XPATH, "(//img[@alt='Comfort'])[1]")
    phone_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_field = (By.ID, "phone")
    phone_next_button = (By.XPATH, "(//button[@type='submit'])[1]")
    code_field = (By.ID, "code")
    code_confirm_button = (By.XPATH, "(//button[@type='submit'])[2]")
    payment_method_field = (By.XPATH, "(//div[text()='Método de pago'])[2]")
    add_card_button = (By.XPATH, "//div[@class='pp-plus-container']//img[1]")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH, "(//input[@id='code'])[2]")
    add_card_confirm_button = (By.XPATH, "(//button[@class='button full'])[4]")
    exit_button_in_payment_popup = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
    message_to_driver_field = (By.ID, "comment")
    blankets_and_tissues_button = (By.XPATH, "(//span[@class='slider round'])[1]")
    add_ice_cream_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    order_taxi_button = (By.XPATH, "(//button[@type='button']//span)[1]")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address): # Ingresar dirección "desde"
        self.driver.find_element(*self.from_field).send_keys(data.address_from)

    def set_to(self, to_address): # Ingresar dirección "hasta"
        self.driver.find_element(*self.to_field).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # Combinacion de pasos para ingresar las direcciones "desde" y "hasta"
    def set_route(self, address_from, address_to):
        self.driver.get(data.urban_routes_url)
        self.set_from(address_from)
        self.get_from()
        self.set_to(address_to)
        self.get_to()

    def click_request_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def click_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    def click_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def click_phone_next_button(self):
        self.driver.find_element(*self.phone_next_button).click()

    def set_verification_code(self):
        self.driver.find_element(*self.code_field).send_keys(retrieve_phone_code(self.driver))

    def click_confirm_button_in_verification_popup(self):
        self.driver.find_element(*self.code_confirm_button).click()

    def click_payment_method_field(self):
        self.driver.find_element(*self.payment_method_field).click()

    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number(self):
        self.driver.find_element(*self.card_number_field).send_keys(data.card_number)

    def set_card_code(self):
        self.driver.find_element(*self.card_code_field).send_keys(data.card_code)

    # Emula que el usuario presiona la tecla TAB
    def press_tab_key(self):
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)

    def click_add_card_confirm_button(self):
        self.driver.find_element(*self.add_card_confirm_button).click()

    def click_exit_button_in_payment_popup(self):
        self.driver.find_element(*self.exit_button_in_payment_popup).click()

    def set_message_to_driver(self):
        self.driver.find_element(*self.message_to_driver_field).send_keys(data.message_for_driver)

    def click_blankets_and_tissues_button(self):
        self.driver.find_element(*self.blankets_and_tissues_button).click()

    def click_add_ice_cream_button(self, num_clicks):
        add_ice_cream_button = self.driver.find_element(*self.add_ice_cream_button)
        for _ in range(num_clicks):
            add_ice_cream_button.click()

    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_taxi_button).click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome() # desired_capabilities = capabilities
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        # Ingresa y verifica la dirección
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        routes_page.click_request_taxi_button() # Presiona el botón pedir un taxi
        routes_page.click_comfort_button() # Selecciona la clase comfort
        routes_page.click_phone_button() # Presiona el campo de número de teléfono
        routes_page.set_phone_number(data.phone_number) # Ingresa el número de telefóno
        routes_page.click_phone_next_button() # Presiona el botón siguiente dentro del campo del número
        routes_page.set_verification_code() # Ingresa el código de verificación
        routes_page.click_confirm_button_in_verification_popup() # Presiona el botón de confirmación
        routes_page.click_payment_method_field() # Presiona el campo de método de pago
        routes_page.click_add_card_button() # Presiona el botón de agregar tarjeta
        routes_page.set_card_number() # Ingresa el número de tarjeta
        routes_page.set_card_code() # Ingresa el código de la tarjeta
        routes_page.press_tab_key() # Presiona la tecla TAB
        routes_page.click_add_card_confirm_button() # Presiona el botón de confirmación
        routes_page.click_exit_button_in_payment_popup() # Presiona el botón de salida
        routes_page.set_message_to_driver() # Ingresa el mensaje para el conductor
        routes_page.click_blankets_and_tissues_button() # Presiona el botón de mantas y pañuelos
        routes_page.click_add_ice_cream_button(2) # Presionar el botón de agregar helado n veces
        routes_page.click_order_taxi_button() # Presiona el botón de pedir taxi
        time.sleep(5) # Espera 5 segundos


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
