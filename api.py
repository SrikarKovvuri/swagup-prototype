import requests
from typing import Dict, List, Union
from marshmallow import Schema, fields

class ColorSchema(Schema):
    """
    Marshmallow schema for color information.
    """
    name = fields.Str(required=True)
    hex_code = fields.Str(required=True)
    rgb = fields.List(fields.Int(), required=True)

class DesignSchema(Schema):
    """
    Marshmallow schema for design information.
    """
    designer_id = fields.Str(required=True)
    design_name = fields.Str(required=True)
    design_description = fields.Str(required=True)
    categories = fields.List(fields.Str(), required=True)
    tags = fields.List(fields.Str(), required=True)
    price = fields.Float(required=True)

class ImageSchema(Schema):
    """
    Marshmallow schema for image upload.
    """
    image = fields.Str(required=True)

class AddressSchema(Schema):
    """
    Marshmallow schema for shipping address.
    """
    recipient_name = fields.Str(required=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    country = fields.Str(required=True)
    zip_code = fields.Str(required=True)


class SwagUpApiClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        """
        Initializes the SwagUpApiClient with the base URL and API key.

        Args:
            base_url (str): The base URL of the SwagUp API.
            api_key (str): The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key

    def _handle_response(self, response: requests.Response) -> Dict[str, Union[str, int]]:
        """
        Handles the API response and raises appropriate exceptions for HTTP errors.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            dict: The JSON data from the response.

        Raises:
            ValueError: If the response indicates a bad request, unauthorized access, or resource not found.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            # Handle specific HTTP errors
            if response.status_code == 400:
                raise ValueError("Bad request. Please check your input.")
            elif response.status_code == 401:
                raise ValueError("Unauthorized. Please check your API key.")
            elif response.status_code == 404:
                raise ValueError("Resource not found.")
            else:
                raise ValueError(f"Request failed with status code: {response.status_code}")

    def create_design(self, designer_id: str, design_name: str, design_description: str, categories: List[str], tags: List[str], price: float) -> Dict[str, Union[str, int]]:
        """
        Creates a new design.

        Endpoint: POST /designs

        Args:
            designer_id (str): The ID of the designer associated with the design.
            design_name (str): The name of the design.
            design_description (str): The description of the design.
            categories (list[str]): The categories the design falls under.
            tags (list[str]): The tags associated with the design.
            price (float): The price of the design.

        Returns:
            dict: The response JSON containing the details of the created design.
        """
        url = f"{self.base_url}/designs"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {
            "designerId": designer_id,
            "designName": design_name,
            "designDescription": design_description,
            "categories": categories,
            "tags": tags,
            "price": price
        }

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def upload_image(self, image: str) -> Dict[str, Union[str, int]]:
        """
        Uploads an image for customization.

        Endpoint: POST /images

        Args:
            image (file): The image file to upload.

        Returns:
            dict: The response JSON containing the details of the uploaded image.
        """
        url = f"{self.base_url}/images"
        headers = {"X-SwagUp-API-Key": self.api_key}
        files = {"image": image}

        response = requests.post(url, headers=headers, files=files)
        return self._handle_response(response)

    def get_design_details(self, design_id: str) -> Dict[str, Union[str, int]]:
        """
        Retrieves the details of a design.

        Endpoint: GET /designs/{designId}

        Args:
            design_id (str): The ID of the design to fetch details for.

        Returns:
            dict: The response JSON containing the details of the design.
        """
        url = f"{self.base_url}/designs/{design_id}"
        headers = {"X-SwagUp-API-Key": self.api_key}

        response = requests.get(url, headers=headers)
        return self._handle_response(response)

    def choose_logo_color(self, color: Dict[str, Union[str, List[int]]], design_id: str) -> Dict[str, Union[str, int]]:
        """
        Selects the color for the logo.

        Endpoint: POST /logo-color

        Args:
            color (dict): The color information including name, hex code, and RGB values.
            design_id (str): The ID of the design to set the logo color for.

        Returns:
            dict: The response JSON containing the updated design details.
        """
        url = f"{self.base_url}/logo-color"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {
            "color": color,
            "designId": design_id
        }

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def select_size_and_quantity(self, design_id: str, items: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[str, int]]:
        """
        Selects the sizes and quantities for an order.

        Endpoint: POST /orders/sizes-quantity

        Args:
            design_id (str): The ID of the design to set sizes and quantities for.
            items (list[dict]): The list of items with size and quantity information.

        Returns:
            dict: The response JSON containing the updated design details.
        """
        url = f"{self.base_url}/orders/sizes-quantity"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {
            "designId": design_id,
            "items": items
        }

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def set_shipping_destination(self, design_id: str, address: Dict[str, str]) -> Dict[str, Union[str, int]]:
        """
        Sets the shipping destination for an order.

        Endpoint: POST /orders/shipping

        Args:
            design_id (str): The ID of the design to set the shipping destination for.
            address (dict): The address information including recipient name, street, city, state, country, and ZIP.

        Returns:
            dict: The response JSON containing the updated design details.
        """
        url = f"{self.base_url}/orders/shipping"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {
            "designId": design_id,
            "address": address
        }

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def manage_payment_methods(self, payment_method: Dict[str, str]) -> Dict[str, Union[str, int]]:
        """
        Adds a payment method.

        Endpoint: POST /payment-methods

        Args:
            payment_method (dict): The payment method details.

        Returns:
            dict: The response JSON containing the details of the added payment method.
        """
        url = f"{self.base_url}/payment-methods"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {"paymentMethod": payment_method}

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def place_order(self, design_id: str, payment_method_id: str) -> Dict[str, Union[str, int]]:
        """
        Places an order.

        Endpoint: POST /orders

        Args:
            design_id (str): The ID of the design for the order.
            payment_method_id (str): The ID of the payment method to use for the order.

        Returns:
            dict: The response JSON containing the details of the placed order.
        """
        url = f"{self.base_url}/orders"
        headers = {"X-SwagUp-API-Key": self.api_key}
        payload = {
            "designId": design_id,
            "paymentMethodId": payment_method_id
        }

        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)

    def track_order(self, order_id: str) -> Dict[str, Union[str, int]]:
        """
        Tracks an order.

        Endpoint: GET /orders/{orderId}

        Args:
            order_id (str): The ID of the order to track.

        Returns:
            dict: The response JSON containing the details of the tracked order.
        """
        url = f"{self.base_url}/orders/{order_id}"
        headers = {"X-SwagUp-API-Key": self.api_key}

        response = requests.get(url, headers=headers)
        return self._handle_response(response)

    def cancel_order(self, order_id: str) -> Dict[str, Union[str, int]]:
        """
        Cancels an order.

        Endpoint: DELETE /orders/{orderId}

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response JSON containing the details of the cancelled order.
        """
        url = f"{self.base_url}/orders/{order_id}"
        headers = {"X-SwagUp-API-Key": self.api_key}

        response = requests.delete(url, headers=headers)
        return self._handle_response(response)
