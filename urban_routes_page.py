import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils import retrieve_phone_code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, "//button[@class='button round']")
    comfort_button = (By.XPATH, "(//div[text()='Comfort'])[1]")
    comfort_button_container = (By.XPATH, "//div[@class='tcard active']")
    phone_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_field = (By.ID, "phone")
    phone_next_button = (By.XPATH, "(//button[@type='submit'])[1]")
    code_field = (By.ID, "code")
    code_confirm_button = (By.XPATH, "(//button[@type='submit'])[2]")
    payment_method_field = (By.XPATH, "(//div[text()='Método de pago'])[2]")
    add_card_button = (By.XPATH, "//div[@class='pp-plus-container']//img[1]")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH, "(//input[@id='code'])[2]")
    add_card_confirm_button = (By.XPATH, "//button[text()='Agregar']")
    exit_button_in_payment_popup = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
    payment_method_selected = (By.CLASS_NAME, 'pp-value-text')
    message_to_driver_field = (By.ID, "comment")
    blankets_and_tissues_button = (By.XPATH, "(//span[@class='slider round'])[1]")
    blankets_and_tissues_checkbox = (By.CSS_SELECTOR, ".switch input.switch-input")
    add_ice_cream_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    ice_cream_counter = (By.XPATH, "(//div[@class='counter']//div)[2]")
    order_taxi_button = (By.XPATH, "(//button[@type='button']//span)[1]")
    waiting_popup_header = (By.CLASS_NAME, "order-header-title")
    order_countdown_timer = (By.CLASS_NAME, "order-header-time")

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

    def get_blankets_and_tissues_button_state(self):
        checkbox = self.driver.find_element(*self.blankets_and_tissues_checkbox)
        return checkbox.is_selected()

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

    def get_waiting_popup_header(self):
        return self.driver.find_element(*self.waiting_popup_header).text
